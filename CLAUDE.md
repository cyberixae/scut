# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

`scut` is a CLI text-column extraction tool. It reads stdin, parses structured text (e.g. whitespace-separated CLI output), and emits CSV. Example: `echo "a b c" | python3 src/scut.py "1-3"` outputs a CSV row with auto-generated headers (a, b, c…).

## Commands

Run all tests (doctests embedded in each module):
```bash
python3 -m doctest src/lib.py
python3 -m doctest src/model.py
python3 -m doctest src/parse.py
python3 -m doctest src/process.py
python3 -m doctest src/output.py
python3 -m doctest src/util.py
```

Run a single module's tests verbosely:
```bash
python3 -m doctest src/lib.py -v
```

Run the tool:
```bash
echo "col1 col2 col3" | python3 src/scut.py "1-3"
```

## Architecture

Pure Python, no external dependencies. The pipeline is:

```
stdin → parse.py → process.py → lib.py → output.py → stdout
```

- **model.py** — TypedDict definitions for all operation types (`Pick`, `Concat`, `PickRange`, `ConcatRange`, `Split`, `Blend`). The canonical data representation between stages.
- **parse.py** — Converts a user spec string (e.g. `"1-12"`, `"[split: :1-3,5]"`) into model objects.
- **process.py** — Converts model objects into callable functions backed by `lib.py`.
- **lib.py** — Core text-processing primitives: `split_at_any_of`, `split_around_any_of`, `pick`, `concat`, `pick_range`, `concat_range`, `blend`.
- **output.py** — Formats results as CSV (default) or JSON; auto-generates column headers (`a`, `b`, `c`…).
- **util.py** — `Flow` and `Pipe` classes for functional composition; used throughout to build transform chains.
- **scut.py** — Entry point; wires parse → process → lib → output.

All business logic is tested via inline doctests in the module that defines each function. When adding a function, add a doctest alongside it.
