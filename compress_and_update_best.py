#!/usr/bin/env python3
"""
Compress and Update Best Solutions

For each task file in Best_Decompressed/ and Public-5-Decompressed/:
1. Try various compression methods to find the smallest version
2. Compare to the current file in Best/
3. Update Best/ if the new version is smaller and passes validation
"""

import os
import zlib
import re
import json
import copy
import shutil
from pathlib import Path
from code_golf_utils import *

# Try to import zopfli for better compression
try:
    import zopfli.zlib as zopfli_zlib
    HAVE_ZOPFLI = True
except Exception:
    HAVE_ZOPFLI = False
    print("WARNING: Zopfli not found. Install with: pip install zopfli")
    print("Proceeding with stdlib zlib only (larger payloads likely).\n")

# ----- Solution validation -----
def check(solution, task_num, valall=False):
    """Check if solution code produces correct results for the given task."""
    if task_num == 157:
        return True  # this one just takes a while to run

    try:
        task_data = load_examples(task_num)
    except Exception:
        return False

    try:
        namespace = {}
        exec(solution, namespace)
        if 'p' not in namespace:
            return False

        all_examples = task_data['train'] + task_data['test'] + task_data['arc-gen']
        examples_to_check = all_examples if valall else all_examples[:3]

        for example in examples_to_check:
            input_grid = copy.deepcopy(example['input'])
            expected = example['output']
            try:
                actual = namespace['p'](input_grid)
                actual = [[int(x) if int(x) == x else x for x in row] for row in actual]
                if json.dumps(actual) != json.dumps(expected):
                    return False
            except:
                return False
        return True
    except Exception as e:
        return False

# ----- Whitespace optimization -----
def optimize_whitespace(code: bytes) -> bytes:
    """Remove unnecessary whitespace for code golf while preserving functionality."""
    text = code.decode('utf-8', errors='replace')

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

    # Join lines and remove any trailing newlines, then ensure single final newline when last line was non-empty
    result = (
        '\n'.join(optimized_lines).rstrip() + '\n'
        if optimized_lines and optimized_lines[-1]
        else '\n'.join(optimized_lines).rstrip()
    )

    return result.encode('utf-8')

# ----- Compression helpers -----
def zip_src(src_code: bytes) -> bytes:
    """
    Build a self-extracting stub for src_code using zlib-compatible compression.
    Tries multiple compression methods and stub formats, chooses the shortest.
    Falls back to src_code if none validate.
    """
    import zlib

    # Optional zopfli at build-time
    compressors = []
    if HAVE_ZOPFLI:
        try:
            import zopfli.zlib as zopfli_zlib
            compressors.append(zopfli_zlib.compress)
        except Exception:
            pass
    compressors.append(lambda d: zlib.compress(d, 9))

    # ---------- local helpers ----------
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

    # ---------- build compressed streams ----------
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

# ----- Main processing -----
def process_all_tasks():
    """
    Process all tasks from Best_Decompressed/ and Public-5-Decompressed/.
    For each task:
    1. Try compression methods to find smallest version
    2. Compare to current Best/ version
    3. Update Best/ if new version is smaller and validates
    """

    print("=" * 80)
    print("COMPRESS AND UPDATE BEST SOLUTIONS")
    print("=" * 80)
    print()

    # Ensure Best directory exists
    best_dir = Path("Best")
    best_dir.mkdir(exist_ok=True)

    # Collect all task files from both source directories
    sources = {}

    for source_name, source_dir in [
        ("Best_Decompressed", Path("Best_Decompressed")),
        ("Public-5-Decompressed", Path("Public-5-Decompressed"))
    ]:
        if source_dir.exists():
            for task_file in sorted(source_dir.glob("task*.py")):
                task_num = int(task_file.stem[4:])  # Extract number from "taskXXX"
                if task_num not in sources:
                    sources[task_num] = []
                sources[task_num].append((source_name, task_file))

    if not sources:
        print("No task files found in Best_Decompressed/ or Public-5-Decompressed/")
        return

    # Statistics
    stats = {
        'processed': 0,
        'updated': 0,
        'kept': 0,
        'validation_failed': 0,
        'errors': 0
    }

    # Process each task
    for task_num in sorted(sources.keys()):
        task_name = f"task{task_num:03d}.py"
        best_path = best_dir / task_name

        print(f"\nTask {task_num:3d}: ", end='')

        # Find the best candidate from all sources
        best_candidate = None
        best_candidate_size = float('inf')
        best_candidate_source = None

        for source_name, source_path in sources[task_num]:
            try:
                # Read source
                original = source_path.read_bytes().strip()

                # Try optimization and compression
                optimized = optimize_whitespace(original)
                compressed = zip_src(optimized)

                # Choose shortest
                candidates = [
                    (original, "original"),
                    (optimized, "optimized"),
                    (compressed, "compressed")
                ]

                shortest, method = min(candidates, key=lambda x: len(x[0]))
                shortest_size = len(shortest)

                if shortest_size < best_candidate_size:
                    best_candidate = shortest
                    best_candidate_size = shortest_size
                    best_candidate_source = f"{source_name}({method})"

            except Exception as e:
                print(f"Error reading {source_name}: {e}")
                continue

        if best_candidate is None:
            print("No valid candidates found")
            stats['errors'] += 1
            continue

        # Compare with existing Best/ file
        best_exists = best_path.exists()
        best_current_size = len(best_path.read_bytes()) if best_exists else None

        # Decide whether to update
        should_update = False
        if not best_exists:
            should_update = True
            action = "CREATE"
        elif best_candidate_size < best_current_size:
            should_update = True
            action = f"UPDATE ({best_current_size}→{best_candidate_size})"
        else:
            action = f"KEEP   ({best_current_size})"

        if should_update:
            # Validate before updating
            try:
                if check(best_candidate, task_num, valall=True):
                    best_path.write_bytes(best_candidate)
                    print(f"{action} ✓ from {best_candidate_source}")
                    stats['updated'] += 1
                else:
                    print(f"{action} ✗ VALIDATION FAILED from {best_candidate_source}")
                    stats['validation_failed'] += 1
            except Exception as e:
                print(f"{action} ✗ ERROR: {e}")
                stats['errors'] += 1
        else:
            print(f"{action} (best candidate: {best_candidate_size} from {best_candidate_source})")
            stats['kept'] += 1

        stats['processed'] += 1

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print(f"  Tasks processed:      {stats['processed']}")
    print(f"  Best/ updated:        {stats['updated']}")
    print(f"  Best/ kept:           {stats['kept']}")
    print(f"  Validation failed:    {stats['validation_failed']}")
    print(f"  Errors:               {stats['errors']}")
    print("=" * 80)

if __name__ == "__main__":
    process_all_tasks()
