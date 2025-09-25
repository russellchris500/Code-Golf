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

def zip_src(src_code):
    """Apply zlib compression with proper escaping for exec()"""
    compressed_options = []

    for compress in [zopfli.zlib.compress, lambda data: zlib.compress(data, 9)]:
        for trailing in [b"", b""]:
            src = src_code + trailing
            while (compressed := compress(src))[-1] == ord('"'):
                src += b"#"

            def sanitize(b_in):
                b_out = bytearray()
                for b in b_in:
                    if b == 0:
                        b_out += b" "
                    elif b == ord("'"):
                        b_out += b"\\'"
                    elif b == ord("\\"):
                        b_out += b"\\\\"
                    else:
                        b_out.append(b)
                return b"" + b_out

            compressed = sanitize(compressed)
            delim = b'"'
            if ord("'") in compressed:
                delim = b'"""'
            elif ord('"') in compressed:
                delim = b"'"

            code = b'#coding:L1\nimport zlib\nexec(zlib.decompress(bytes(' + delim + compressed + delim + b',"L1")))'

            try:
                with open("tmp.py", "wb") as f:
                    f.write(code)
                with open("tmp.py", "rb") as f:
                    x = f.read()
                exec(x, {})
                compressed_options.append(code)
            except:
                pass

    return min(compressed_options, key=lambda x: len(x)) if compressed_options else src_code

def compress_solutions():
    """Compress all solution files, keeping the smallest version"""
    # os.makedirs('Private-Compressed', exist_ok=True)

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

        # Try zlib compression
        try:
            compressed = zip_src(optimized)

            # Use whichever is smaller: original, optimized, or compressed
            best_content = min([original, optimized, compressed], key=len)
            if best_content == compressed:
                final_content = compressed
                improvement = len(original) - len(compressed)
                stats['improved'] += 1
                stats['total_saved'] += improvement
                print(f"Task {i:03d}: {len(original)} -> opt {len(optimized)} -> comp {len(compressed)} (-{improvement})")
            elif best_content == optimized:
                final_content = optimized
                improvement = len(original) - len(optimized)
                if improvement > 0:
                    stats['improved'] += 1
                    stats['total_saved'] += improvement
                print(f"Task {i:03d}: {len(original)} -> opt {len(optimized)} (-{improvement})")
            else:
                final_content = original
                print(f"Task {i:03d}: {len(original)} (no improvement)")

        except Exception as e:
            # If compression fails, try optimized or use original
            if len(optimized) < len(original):
                final_content = optimized
                improvement = len(original) - len(optimized)
                stats['improved'] += 1
                stats['total_saved'] += improvement
                print(f"Task {i:03d}: {len(original)} -> opt {len(optimized)} (-{improvement}) (compression failed: {e})")
            else:
                final_content = original
                print(f"Task {i:03d}: {len(original)} (compression failed: {e})")

        # Write the smaller version
        with open(dst_path, 'wb') as f:
            f.write(final_content)

    print(f"\nProcessed {stats['processed']} files")
    print(f"Improved {stats['improved']} files")
    print(f"Total bytes saved: {stats['total_saved']}")

    return stats

if __name__ == "__main__":
    compress_solutions()