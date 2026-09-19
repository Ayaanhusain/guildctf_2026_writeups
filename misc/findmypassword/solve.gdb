# solve.gdb — GuildCTF 2026 "findmypassword"
#
# Usage:
#   chmod +x basic_rev
#   gdb -q -x solve.gdb ./basic_rev
#
# Or interactively step-by-step:
#   gdb -q ./basic_rev
#   (gdb) start
#   (gdb) source solve.gdb
#
# The binary contains two global arrays, enc_arr and xor_arr, plus an
# integer pass_length. The password is recovered by XORing the two
# arrays element-wise and printing each byte as a character.

start

# Print the password length (stored as a 32-bit int variable).
printf "pass_length = "
p *(int*)&pass_length

# Dump the first 45 bytes of each array so we can inspect them if needed.
printf "\nenc_arr:\n"
x/45bx &enc_arr

printf "\nxor_arr:\n"
x/45bx &xor_arr

# Recover the password: enc_arr[i] XOR xor_arr[i], printed as characters.
# The arrays are actually arrays of 32-bit integers, so we cast to (int*)
# and index element-wise.
printf "\nRecovered password:\n"
set $i = 0
while $i < 45
    printf "%c", ((int*)&enc_arr)[$i] ^ ((int*)&xor_arr)[$i]
    set $i = $i + 1
end
printf "\n"

quit
