import os
import zlib
import zopfli.zlib
import re

def optimize_whitespace(code):
    """Remove unnecessary whitespace for code golf while preserving functionality."""
    if isinstance(code, bytes):
        text = code.decode('utf-8', errors='replace')
    else:
        text = code

    # Remove multiple consecutive blank lines (keep max 1)
    text = re.sub(r'\n\s*\n(\s*\n)*', '\n\n', text)

    # Remove trailing whitespace from each line
    lines = text.split('\n')
    lines = [line.rstrip() for line in lines]

    # Remove multiple spaces that aren't needed (but preserve indentation)
    optimized_lines = []
    for line in lines:
        if line.strip():  # Non-empty line
            # Find leading whitespace
            leading_match = re.match(r'^\s*', line)
            leading = leading_match.group() if leading_match else ''
            content = line[len(leading):]

            # Replace multiple spaces with single spaces in content (but not in strings)
            # Simple approach: only compress spaces outside of quotes
            in_string = False
            quote_char = None
            result = []
            i = 0
            while i < len(content):
                char = content[i]
                if not in_string and char in ['"', "'"]:
                    in_string = True
                    quote_char = char
                    result.append(char)
                elif in_string and char == quote_char and (i == 0 or content[i-1] != '\\'):
                    in_string = False
                    quote_char = None
                    result.append(char)
                elif not in_string and char == ' ':
                    # Compress multiple spaces to single space
                    if result and result[-1] != ' ':
                        result.append(' ')
                else:
                    result.append(char)
                i += 1

            optimized_lines.append(leading + ''.join(result))
        else:
            optimized_lines.append('')  # Keep empty lines as-is

    # Join lines and remove any trailing newlines, then ensure single final newline
    result = '\n'.join(optimized_lines).rstrip() + '\n' if optimized_lines and optimized_lines[-1] else '\n'.join(optimized_lines).rstrip()

    return result.encode('utf-8') if isinstance(code, bytes) else result

def zip_src(src_code: bytes) -> bytes:
    """
    Build a self-extracting stub for src_code using zlib-compatible compression.
    Tries:
      A) '#coding:L1\\nimport zlib\\nexec(zlib.decompress(bytes("…","L1")))' 
      B) '#coding:L1\\nexec(__import__("zlib").decompress(bytes("…","L1")))' 
      C) 'exec(__import__("zlib").decompress(b"…"))'
    Chooses the shortest candidate that compiles and round-trips via exec().
    Falls back to src_code if none validate.
    """
    import zlib

    # Optional zopfli at build-time; no warning here (GUI can warn separately)
    compressors = []
    try:
        import zopfli.zlib as zopfli_zlib
        compressors.append(zopfli_zlib.compress)
    except Exception:
        pass
    compressors.append(lambda d: zlib.compress(d, 9))

    # ---------- local helpers (self-contained) ----------
    def _sanitize_str_for_bytes_l1(data: bytes) -> bytes:
        # For embedding in bytes('…','L1'): escape NUL, CR, backslash; keep others raw
        out = bytearray()
        for b in data:
            if b == 0:           out += b"\\x00"
            elif b == 13:        out += b"\\r"
            elif b == 92:        out += b"\\\\"
            else:                out.append(b)
        return bytes(out)

    def _sanitize_bytes_literal(data: bytes) -> bytes:
        # For b'…' / b"…": escape non-printables; keep LF; escape CR and backslash
        out = bytearray()
        for b in data:
            if b == 10:                 # '\n'
                out.append(10)
            elif b == 13:               # '\r'
                out += b"\\r"
            elif b == 92:               # '\\'
                out += b"\\\\"
            elif 32 <= b <= 126 and b not in (9, 11, 12):
                out.append(b)
            else:
                out += f"\\x{b:02x}".encode()
        return bytes(out)

    def _best_str_delim(payload: bytes) -> bytes:
        # Prefer triple quotes if payload contains newline
        if b"\n" in payload: return b'"""'
        return b"'" if b'"' in payload else b'"'

    def _best_bytes_delim(payload: bytes) -> bytes:
        if b"\n" in payload: return b'"""'
        dq = payload.count(b'"'); sq = payload.count(b"'")
        if dq and not sq: return b"'"
        if sq and not dq: return b'"'
        return b'"'

    # ---------- build compressed streams with tiny source probes ----------
    compressed_streams = []
    for compress in compressors:
        for trailing in (b"", b"\n"):
            s = src_code + trailing
            c = compress(s)
            while c and c[-1] == 34:   # avoid trailing '"'
                s += b"#"
                c = compress(s)
            compressed_streams.append(c)

    # ---------- assemble candidate stubs ----------
    candidates = []
    SUFFIX = b',"L1")))'  # closes bytes(...),"L1") then decompress(...) then exec(...)

    for comp in compressed_streams:
        # A) import zlib + bytes('…','L1')
        s_payload = _sanitize_str_for_bytes_l1(comp)
        s_delim = _best_str_delim(s_payload)
        code_A = (
            b"#coding:L1\nimport zlib\nexec(zlib.decompress(bytes("
            + s_delim + s_payload + s_delim + SUFFIX
        )

        # B) __import__('zlib') + bytes('…','L1')
        code_B = (
            b"#coding:L1\nexec(__import__('zlib').decompress(bytes("
            + s_delim + s_payload + s_delim + SUFFIX
        )

        # C) __import__('zlib') + b'…'
        b_payload = _sanitize_bytes_literal(comp)
        b_delim = _best_bytes_delim(b_payload)
        # If single/double quotes, escape that quote inside the payload
        if b_delim != b'"""':
            q = b_delim[:1]
            if q in b_payload:
                b_payload = b_payload.replace(q, b"\\" + q)
        code_C = (
            b"exec(__import__('zlib').decompress(b"
            + b_delim + b_payload + b_delim + b"))"
        )

        # Validate that each candidate parses and executes (round-trip check)
        for cand in (code_A, code_B, code_C):
            try:
                compile(cand, "<stub>", "exec")
                exec(cand, {})
                candidates.append(cand)
            except Exception:
                pass

    return min(candidates, key=len) if candidates else src_code

def compress_solutions():
    """Compress all solution files, writing to Best/ only if the new candidate is strictly shorter."""
    os.makedirs('Best', exist_ok=True)

    stats = {'processed': 0, 'improved': 0, 'total_saved': 0}

    for i in range(1, 401):
        src_path = f'Best_Decompressed/task{i:03d}.py'
        dst_path = f'Best/task{i:03d}.py'

        if not os.path.exists(src_path):
            continue

        stats['processed'] += 1

        # Read and strip whitespace
        with open(src_path, 'rb') as f:
            original = f.read().strip()

        # Optimize whitespace
        optimized = optimize_whitespace(original)

        try:
            # Try zlib compression
            compressed = zip_src(optimized)

            # Pick the smallest among original, optimized, compressed
            best_content = min([original, optimized, compressed], key=len)
            best_len = len(best_content)
            orig_len = len(original)

            # Compare against what's already in Best/
            if os.path.exists(dst_path):
                with open(dst_path, 'rb') as f:
                    existing = f.read()
                existing_len = len(existing)
            else:
                existing = None
                existing_len = None

            # Only overwrite if strictly shorter (or create if missing)
            if existing is None or best_len < existing_len:
                with open(dst_path, 'wb') as f:
                    f.write(best_content)

                improvement = orig_len - best_len
                if improvement > 0:
                    stats['improved'] += 1
                    stats['total_saved'] += improvement

                if existing is None:
                    print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} -> comp {len(compressed)} | wrote (created) {best_len}")
                else:
                    print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} -> comp {len(compressed)} | updated Best ({existing_len} -> {best_len})")
            else:
                print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} -> comp {len(compressed)} | kept Best ({existing_len} <= {best_len})")

        except Exception as e:
            # If compression fails, consider original vs optimized, but still only write if strictly shorter than existing
            best_content = min([original, optimized], key=len)
            best_len = len(best_content)
            orig_len = len(original)

            if os.path.exists(dst_path):
                with open(dst_path, 'rb') as f:
                    existing = f.read()
                existing_len = len(existing)
            else:
                existing = None
                existing_len = None

            if existing is None or best_len < existing_len:
                with open(dst_path, 'wb') as f:
                    f.write(best_content)

                improvement = orig_len - best_len
                if improvement > 0:
                    stats['improved'] += 1
                    stats['total_saved'] += improvement

                if existing is None:
                    print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} (compression failed: {e}) | wrote (created) {best_len}")
                else:
                    print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} (compression failed: {e}) | updated Best ({existing_len} -> {best_len})")
            else:
                print(f"Task {i:03d}: {orig_len} -> opt {len(optimized)} (compression failed: {e}) | kept Best ({existing_len} <= {best_len})")

    print(f"\nProcessed {stats['processed']} files")
    print(f"Improved {stats['improved']} files")
    print(f"Total bytes saved: {stats['total_saved']}")

    return stats

if __name__ == "__main__":
    compress_solutions()