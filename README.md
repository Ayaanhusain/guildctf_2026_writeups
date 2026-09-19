# GuildCTF 2026 Writeups

**Ayaan Husain** — MA26B003 — ma26b003@smail.iitm.ac.in

Solve scripts for the challenges I fully solved in GuildCTF 2026.

**Total score: 2048** — 11 challenges solved across Binary Exploitation, Cryptography, and Miscellaneous.

---

## Challenges

### Binary Exploitation (Pwn)

| Challenge | Points | Solve Script |
|---|---|---|
| GOT a name? | 100 | [pwn/got_a_name/solve.py](pwn/got_a_name/solve.py) |
| I like Buffets | 100 | [pwn/i_like_buffets/solve.py](pwn/i_like_buffets/solve.py) |
| what's yo name | 100 | [pwn/whats_yo_name/solve.py](pwn/whats_yo_name/solve.py) |
| what's yo name returns | 323 | [pwn/whats_yo_name_returns/solve.py](pwn/whats_yo_name_returns/solve.py) |
| what's yo name returns again | 723 | [pwn/whats_yo_name_returns_again/solve.py](pwn/whats_yo_name_returns_again/solve.py) |

### Cryptography

| Challenge | Points | Solve Script |
|---|---|---|
| R my SA | 100 | [crypto/r_my_sa/solve.py](crypto/r_my_sa/solve.py) |
| Monty Python's Flying Casino | 660 | [crypto/flying_casino/solve.py](crypto/flying_casino/solve.py) |

### Miscellaneous

| Challenge | Points | Solve Script |
|---|---|---|
| EAassyy Stufff | 20 | [misc/eaassyy_stufff/solve.txt](misc/eaassyy_stufff/solve.txt) |
| It's definitely normal | 50 | [misc/its_definitely_normal/solve.py](misc/its_definitely_normal/solve.py) |
| findmypassword | 100 | [misc/findmypassword/solve.gdb](misc/findmypassword/solve.gdb) |

---

## How to Run

### Pwn challenges and the Casino challenge

These scripts connect to a remote challenge instance. Pass the host and port as arguments:

```bash
cd pwn/got_a_name
python3 solve.py <HOST> <PORT>
