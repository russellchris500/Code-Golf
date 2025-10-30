import re, ast, zlib, pathlib, codecs

# --- patterns (liberal: match any ...decompress(...bytes(...)) etc.) ---
PAT_BYTES_L1 = re.compile(
    r"""decompress\s*\(\s*bytes\s*\(\s*
        (?P<lit>(?P<q>['"]{3}|['"]).*?(?P=q))      # string literal
        \s*,\s*(?P<enc>['"][^'"]+['"])\s*\)\s*\)   # encoding literal
    """,
    re.S | re.I | re.X,
)

PAT_B_LIT = re.compile(
    r"""decompress\s*\(\s*
        (?P<lit>b(?P<q>['"]{3}|['"]).*?(?P=q))     # bytes literal
        \s*\)
    """,
    re.S | re.X,
)

PAT_CODECS = re.compile(
    r"""decompress\s*\(\s*
        (?:__import__\(['"]codecs['"]\)\.|codecs\.)decode
        \s*\(\s*(?P<lit>(?P<q>['"]{3}|['"]).*?(?P=q))
        \s*,\s*(?P<enc>['"][^'"]+['"])\s*\)\s*\)
    """,
    re.S | re.I | re.X,
)

def _ast_eval_literal(text_literal: str):
    """Safely evaluate a Python string/bytes literal to its runtime value."""
    return ast.literal_eval(text_literal)

def extract_src_from_stub_text(text_latin1: str) -> bytes:
    # Case 1: bytes("…","L1"/"latin1"/"latin-1")
    m = PAT_BYTES_L1.search(text_latin1)
    if m:
        lit = m.group("lit")   # includes quotes
        enc = ast.literal_eval(m.group("enc")).lower()
        if enc in ("l1", "latin1", "latin-1"):
            # Evaluate the string literal so escapes (\\x00, \\r, etc.) become real chars
            s = _ast_eval_literal(lit)            # -> Python str
            comp = s.encode("latin-1")            # 1:1 to original bytes
            return zlib.decompress(comp)

    # Case 2: decompress(b"...")
    m = PAT_B_LIT.search(text_latin1)
    if m:
        b_lit = m.group("lit")  # includes the leading b and quotes
        comp = _ast_eval_literal(b_lit)  # -> bytes (escapes handled)
        return zlib.decompress(comp)

    # Case 3: decompress(codecs.decode("…","latin1"))
    m = PAT_CODECS.search(text_latin1)
    if m:
        lit = m.group("lit")     # string literal
        enc = ast.literal_eval(m.group("enc")).lower()
        s = _ast_eval_literal(lit)            # str with escapes resolved
        # codecs.decode expects bytes; for latin-1 this is a 1:1 mapping from str
        comp = codecs.decode(s.encode("latin-1"), enc)
        return zlib.decompress(comp)

    # Case 4: no compression present → return as-is
    if "decompress(" not in text_latin1:
        return text_latin1.encode("latin-1")  # preserve bytes faithfully

    raise ValueError("No recognizable zlib payload pattern found.")

def decompress_task_file(input_path: pathlib.Path, output_dir: pathlib.Path = pathlib.Path("Best_Decompressed")):
    """Decompress a single task file and write to output directory"""
    m = re.search(r'task(\d+)\.py$', input_path.name)
    if not m:
        raise ValueError(f"Invalid task filename: {input_path.name}")
    task_num = m.group(1)

    # IMPORTANT: read as latin-1 to avoid corrupting payload bytes
    text = input_path.read_text(encoding="latin-1")
    try:
        src_bytes = extract_src_from_stub_text(text)
    except Exception as e:
        # Bubble up with filename context
        raise RuntimeError(f"{input_path.name}: {e}")

    output_dir.mkdir(exist_ok=True)
    out = output_dir / f"task{task_num}.py"
    # Most sources are UTF-8; if not, latin-1 round-trip is safe
    try:
        out.write_text(src_bytes.decode("utf-8"), encoding="utf-8")
    except UnicodeDecodeError:
        out.write_text(src_bytes.decode("latin-1"), encoding="latin-1")
    return out

if __name__ == "__main__":
    best_dir = pathlib.Path("Best-Updated-2")
    output_dir = pathlib.Path("Best_Decompressed")
    if not best_dir.exists():
        print(f"Directory {best_dir} not found"); raise SystemExit(1)

    processed = 0
    for task_file in sorted(best_dir.glob("task*.py")):
        try:
            outp = decompress_task_file(task_file, output_dir)
            print(f"Processed {task_file.name} -> {outp}")
            processed += 1
        except Exception as e:
            print(f"Error processing {task_file.name}: {e}")

    print(f"Successfully processed {processed} files")
