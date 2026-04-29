# scut

A command-line tool for parsing arbitrary text into CSV.

## Motivation

`cut` can only remove bytes — it cannot reorder or duplicate fields. csvkit can reorder and duplicate columns, but requires CSV input; it has no facility for parsing arbitrary delimited text. The traditional answer for turning raw CLI output or other unstructured text into CSV is a throwaway perl or awk script. scut is the tool you would reach for instead.

## Usage

```sh
echo "a b c d e" | scut "1-3"
```

The spec argument describes how to split the input and which fields to extract. The default split is on any whitespace. A custom delimiter can be specified with bracket syntax:

```sh
echo "a:b:c:d:e" | scut "[split:::1-3]"
```

Output is CSV with auto-generated column headers.

## Status

The core library (`lib.py`) supports chained and nested splits — picking fields from a first split and then re-splitting individual fields further. The spec language in `parse.py` does not yet have syntax for expressing this.
