#!/usr/bin/env python3
"""
GuildCTF 2026 — "It's definitely normal"
Category: Miscellaneous
Challenge Flag: exploiitm{00H_SP3C14l_ch4R4cT3R2}

The transcript.txt file contains invisible Unicode characters
(U+200B ZERO WIDTH SPACE) scattered throughout the text. There is only
one type of invisible character, so this is not a 0/1 bit stream.

Instead, the *gap length* between consecutive ZWSPs encodes the flag.
Each gap (counted in ordinary characters between two ZWSPs, plus the
gap from the start of the file to the first ZWSP) is an ASCII code.

Usage:
    python3 solve.py
"""

with open('transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

ZW = '\u200b'

# Collect the index of every zero-width space in the file.
positions = [i for i, c in enumerate(text) if c == ZW]
print(f"[*] Found {len(positions)} zero-width spaces")

# Build the list of gaps. Include the gap from the start of the file to
# the first ZWSP, otherwise the first character of the flag is missing.
gaps = [positions[0]] + [
    positions[i + 1] - positions[i] - 1
    for i in range(len(positions) - 1)
]
print(f"[*] Gaps between ZWSPs: {gaps}")

# Each gap is an ASCII code. Convert to characters.
flag = ''.join(chr(g) for g in gaps)
print(f"[+] Flag: {flag}")
