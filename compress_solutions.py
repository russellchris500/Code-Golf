import os
import zlib
import zopfli.zlib

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
    os.makedirs('Private-Compressed', exist_ok=True)

    stats = {'processed': 0, 'improved': 0, 'total_saved': 0}

    for i in range(1, 401):
        src_path = f'Private-Uncompressed/task{i:03d}.py'
        dst_path = f'Private-Compressed/task{i:03d}.py'

        if not os.path.exists(src_path):
            continue

        stats['processed'] += 1

        # Read and strip whitespace
        with open(src_path, 'rb') as f:
            original = f.read().strip()

        # Try zlib compression
        try:
            compressed = zip_src(original)

            # Use whichever is smaller
            if len(compressed) < len(original):
                final_content = compressed
                improvement = len(original) - len(compressed)
                stats['improved'] += 1
                stats['total_saved'] += improvement
                print(f"Task {i:03d}: {len(original)} -> {len(compressed)} (-{improvement})")
            else:
                final_content = original
                print(f"Task {i:03d}: {len(original)} (no improvement)")

        except Exception as e:
            # If compression fails, use original
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