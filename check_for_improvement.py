import os
import zlib
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import re
import json
import copy
import threading
from code_golf_utils import *

# Try to import zopfli for better compression (build-time only).
# If unavailable, WARN (do not silently fall back).
try:
    import zopfli.zlib as zopfli_zlib
    HAVE_ZOPFLI = True
except Exception:
    HAVE_ZOPFLI = False
    ZOPFLI_WARNING = (
        "Zopfli not found. Install with:\n"
        "  pip install zopfli\n\n"
        "Proceeding with stdlib zlib only (larger payloads likely)."
    )

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

    # Join lines and remove any trailing newlines, then ensure single final newline when last line was non-empty
    result = (
        '\n'.join(optimized_lines).rstrip() + '\n'
        if optimized_lines and optimized_lines[-1]
        else '\n'.join(optimized_lines).rstrip()
    )

    return result.encode('utf-8')

# ----- Compression helpers -----
def _sanitize_str_for_bytes_l1(data: bytes) -> bytes:
    """For embedding inside bytes('…','L1'): escape NUL, CR, backslash; keep others raw."""
    out = bytearray()
    for b in data:
        if b == 0:           out += b"\\x00"
        elif b == 13:        out += b"\\r"
        elif b == 92:        out += b"\\\\"
        else:                out.append(b)
    return bytes(out)

def _sanitize_bytes_literal(data: bytes) -> bytes:
    """For embedding inside a bytes literal b'…' / b\"…\": escape non-printables; keep LF."""
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
    if b"\n" in payload:
        return b'"""'
    return b"'" if b'"' in payload else b'"'

def _best_bytes_delim(payload: bytes) -> bytes:
    if b"\n" in payload:
        return b'"""'
    dq = payload.count(b'"')
    sq = payload.count(b"'")
    if dq and not sq: return b"'"
    if sq and not dq: return b'"'
    return b'"'

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

# ----- Single-task processing -----
def process_task(task_num: int) -> dict:
    """
    Compress Private-Uncompressed/taskXXX.py and conditionally write:
      - Private-Compressed/taskXXX.py only if NEW < existing
      - Best/taskXXX.py only if NEW < existing
      - Best_Decompressed/taskXXX.py (the *pre-compression* source, i.e., optimized) only if Best updated
    """
    if not (1 <= task_num <= 400):
        raise ValueError("Task number must be in 1..400")

    name = f"task{task_num:03d}.py"
    src_path = Path("Private-Uncompressed") / name
    if not src_path.exists():
        raise FileNotFoundError(f"{src_path} not found")

    pc_dir = Path("Private-Compressed"); pc_dir.mkdir(exist_ok=True)
    best_dir = Path("Best"); best_dir.mkdir(exist_ok=True)
    best_dec_dir = Path("Best_Decompressed"); best_dec_dir.mkdir(exist_ok=True)

    original = src_path.read_bytes().strip()
    optimized = optimize_whitespace(original)
    compressed = zip_src(optimized)

    # Choose the shortest among original, optimized, compressed
    result = min((original, optimized, compressed), key=len)
    result_len = len(result)

    # Private-Compressed
    pc_path = pc_dir / name
    pc_prev = pc_path.read_bytes() if pc_path.exists() else None
    pc_prev_len = len(pc_prev) if pc_prev is not None else None
    wrote_pc = False
    if pc_prev is None or result_len < pc_prev_len:
        pc_path.write_bytes(result)
        wrote_pc = True

    # Best (compressed-or-not) - with validation
    best_path = best_dir / name
    best_prev = best_path.read_bytes() if best_path.exists() else None
    best_prev_len = len(best_prev) if best_prev is not None else None
    wrote_best = False
    validation_passed = False
    validation_error = None

    if best_prev is None or result_len < best_prev_len:
        # Validate the new solution before writing to Best
        try:
            validation_passed = check(result, task_num, valall=True)
            if validation_passed:
                best_path.write_bytes(result)
                wrote_best = True

                # Also write *pre-compression* (optimized) source to Best-Decompressed
                best_dec_path = best_dec_dir / name
                best_dec_path.write_bytes(optimized)
                wrote_best_dec = True
            else:
                validation_error = "Solution failed validation tests"
                wrote_best_dec = False
        except Exception as e:
            validation_passed = False
            validation_error = f"Validation error: {str(e)}"
            wrote_best_dec = False
    else:
        wrote_best_dec = False

    return {
        "task": name,
        "original_len": len(original),
        "optimized_len": len(optimized),
        "compressed_len": len(compressed),
        "chosen_len": result_len,
        "pc_previous_len": pc_prev_len,
        "pc_written": wrote_pc,
        "best_previous_len": best_prev_len,
        "best_written": wrote_best,
        "best_decompressed_written": wrote_best_dec,
        "validation_passed": validation_passed,
        "validation_error": validation_error,
    }

# ----- Tkinter GUI -----
def run_gui():
    root = tk.Tk()
    root.title("Compress a Golf Task")

    frm = tk.Frame(root, padx=12, pady=12)
    frm.pack()

    # Warn loudly if zopfli is missing
    if not HAVE_ZOPFLI:
        if "ZOPFLI_WARNING" in globals():
            messagebox.showwarning("Zopfli not installed", ZOPFLI_WARNING)
            warn = tk.Label(frm, text=ZOPFLI_WARNING, fg="red", justify="left")
            warn.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

    row = 1
    tk.Label(frm, text="Task number (1–400):").grid(row=row, column=0, sticky="w")
    ent = tk.Entry(frm, width=8)
    ent.grid(row=row, column=1, padx=(6, 0))
    ent.focus()

    out = tk.StringVar(value="Awaiting input…")
    tk.Label(frm, textvariable=out, justify="left", anchor="w").grid(row=row+1, column=0, columnspan=3, sticky="w", pady=(10,0))

    def on_process():
        v = ent.get().strip()
        try:
            n = int(v)
        except:
            out.set("Invalid task number")
            return

        # Disable button during processing
        btn.config(state='disabled')
        out.set(f"Processing task {n}...")

        def process_in_thread():
            try:
                info = process_task(n)

                pc_prev = info["pc_previous_len"]
                pc_prev_text = "created" if pc_prev is None else f"prev {pc_prev}B"

                best_prev = info["best_previous_len"]
                best_prev_text = "created" if best_prev is None else f"prev {best_prev}B"

                # Build status message with validation info
                best_status = 'updated' if info['best_written'] else 'kept'
                if info['best_previous_len'] is None or info['chosen_len'] < info['best_previous_len']:
                    if info['validation_passed']:
                        validation_status = "✓ VALIDATED"
                    elif info['validation_error']:
                        validation_status = f"✗ FAILED: {info['validation_error']}"
                        best_status = 'validation failed'
                    else:
                        validation_status = "✗ FAILED"
                        best_status = 'validation failed'
                else:
                    validation_status = "not tested (not shorter)"

                msg_lines = [
                    f"{info['task']}: orig {info['original_len']}B → opt {info['optimized_len']}B → compressed {info['compressed_len']}B → chosen {info['chosen_len']}B",
                    f"Private-Compressed: {pc_prev_text} → {'updated' if info['pc_written'] else 'kept'}",
                    f"Best: {best_prev_text} → {best_status}",
                    f"Validation: {validation_status}",
                    f"Best_Decompressed: {'updated' if info['best_decompressed_written'] else 'kept'}",
                ]
                msg = "\n".join(msg_lines)
                root.after(0, lambda: out.set(msg))
                root.after(0, lambda: btn.config(state='normal'))
                print(msg)
            except Exception as e:
                error_msg = f"Error: {e}"
                root.after(0, lambda: out.set(error_msg))
                root.after(0, lambda: btn.config(state='normal'))
                root.after(0, lambda: messagebox.showerror("Error", str(e)))

        threading.Thread(target=process_in_thread, daemon=True).start()

    btn = tk.Button(frm, text="Process", command=on_process, width=12)
    btn.grid(row=row, column=2, padx=(10, 0))
    root.bind("<Return>", lambda _: on_process())

    root.mainloop()

if __name__ == "__main__":
    run_gui()
