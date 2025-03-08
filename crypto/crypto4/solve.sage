# Sage code for the lattice attack

# Given parameters (from the challenge output):
a = Integer(10213605335725869902199980943719559376078628344855139518695966294719573727981927244963105128635490914256580609241170785118512847758809339974175050307467513)
b = Integer(12226132017457881660841089359898059192854266582734983086780718452790707778384380923987519151891666439949218431538364623553026728617906929652414303678393771)
n = Integer(12340305166878273300795406894482315943207820146367671832805850102046679320850362513916978404952722625260673688257802170159773812457930952612322418140710389)

# Truncated outputs:
# y1 = Integer("0xe78777e4ea55952f1be574b1297d6ce94db078893351bbf894d1706fbbc924bd5", 16)
# y2 = Integer("0x26ba6329f1253cac77ce14a86eb81fd7d7ebcce967234434b21753a4da1d39045", 16)
y1 = 1675577917693456139806880850092035553492575806076436406333683430085767598328789
y2 = 280275299261674057130228261432114147207022361818272597608064721508436161040453

T = 2^252  # The unknown lower bits are in [0, T)

# Recall: flag1 = y1*T + r  and  flag2 = y2*T + r2, with 0 <= r,r2 < T.
# The LCG gives flag2 = a*flag1 + b (mod n). Hence there exists an integer k such that:
#   a*(y1*T + r) + b = y2*T + r2 + k*n.
# Rearranging, define:
C = a * y1 * T + b - y2 * T
# so that our equation becomes:
#    a*r - k*n = -C + r2,  with |r2| < T.
# In other words, we have:
#    |a*r - k*n + C| < T.
#
# Our goal is to recover the small unknown r (with 0 <= r < T).
# We embed the relation in a 3-dimensional lattice with basis:
B = Matrix(ZZ, [
    [T,   0,  0],
    [0,   T,  0],
    [a,  -n,  T]
])
print("Lattice basis B:")
print(B)

# Compute the LLL-reduced basis:
B_lll = B.LLL()
print("\nLLL-reduced basis:")
print(B_lll)

# We now search for a short vector (r_candidate, k_candidate, v3) in the lattice
# that will give us a good candidate for r.
# We want v3, after subtracting C, to be less than T in absolute value.
bound = 6  # search range for combination coefficients
candidate = None

# Enumerate all linear combinations of the LLL basis vectors with coefficients in [-bound, bound].
for coeffs in CartesianProduct([srange(-bound, bound+1)]*3):
    # Build the combination vector:
    vec = sum([ coeffs[i] * B_lll.row(i) for i in range(3) ])
    r_candidate = vec[0]
    # We require 0 <= r < T:
    if r_candidate < 0 or r_candidate >= T:
        continue
    # Let e_val be the third coordinate offset by C:
    e_val = vec[2] - C
    if abs(e_val) < T:
        candidate = (r_candidate, vec[1], e_val)
        break

if candidate is None:
    print("No candidate found in the search range.")
else:
    r_rec, k_rec, error = candidate
    print("\nRecovered candidate values:")
    print("r =", r_rec)
    print("k =", k_rec)
    print("|a*r - k*n + C| =", abs(error))
    
    # Reconstruct flag1 = y1*T + r:
    flag1 = y1 * T + r_rec
    # Invert one LCG step to recover the original flag:
    inv_a = inverse(a, n)
    flag_num = ((flag1 - b) * inv_a) % n
    # Convert the number to bytes:
    flag_bytes = flag_num.to_bytes((flag_num.nbits() + 7) // 8, 'big')
    print("\nRecovered flag (bytes):")
    print(flag_bytes)
