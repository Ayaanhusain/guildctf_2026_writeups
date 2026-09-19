from pwn import *
import re, random, sys

context.log_level = 'error'

HOST = '10.21.232.223'
PORT = 42264

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

# Sign
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

# Claim
p.sendline(b'5')
p.recvuntil(b'claim: ')
p.sendline(str(wallet).encode())
p.recvuntil(b'code: ')
p.sendline(code)
out = p.recvall(timeout=10)
print(out.decode(errors='replace'))
