import sympy
from math import gcd, isqrt
import random

n = 610870240865234529907743614451858801440155492757079465096710603276200472290332312307451743490652760649679857285194802523705355655732590457358769052210759328095574632949925216971079564253285551079681286819576086292966982023640170817829686489069479455782174911021436314674483460806303999075272232571864598274720703485318203442053573948268875433041811318199331
e = 65537
ct = 269502667676232352065057019549198430447003590244768780011937512108750638388052071680107935792375411406856203708540602606052505183332456367255459084740242095067533827164103921553415851493514793496968994176547304138220110710286537331520492430193350534011015869917837578280239839478693713969444834925766299298505300587378553503027879397491554035163970710898956

# 1) small prime factors
print("[*] Trial division...")
small = sympy.factorint(n, limit=10**6)
print("small factors:", small)
if small and any(v > 0 for v in small.values()):
    pass

# 2) Pollard p-1
def pollard_pm1(n, B=100000):
    a = 2
    for p in sympy.primerange(2, B):
        a = pow(a, p, n)
        if p % 1000 == 0:
            g = gcd(a-1, n)
            if 1 < g < n:
                return g
    g = gcd(a-1, n)
    if 1 < g < n:
        return g
    return None

print("[*] Pollard p-1...")
g = pollard_pm1(n, 100000)
if g:
    print("found factor:", g)
    p, q = g, n // g
else:
    print("p-1 failed")

# 3) Pollard rho
def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x = random.randint(2, n-1)
        y = x
        c = random.randint(1, n-1)
        d = 1
        while d == 1:
            x = (x*x + c) % n
            y = (y*y + c) % n
            y = (y*y + c) % n
            d = gcd(abs(x-y), n)
        if d != n:
            return d

print("[*] Pollard rho...")
try:
    g = pollard_rho(n)
    print("found factor:", g)
except Exception as ex:
    print("rho failed:", ex)
