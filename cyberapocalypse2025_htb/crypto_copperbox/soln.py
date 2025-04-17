from sage.all import *
# import sys

# Parameters (example values, replace with actual values)

p = 0x31337313373133731337313373133731337313373133731337313373133732ad
a = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
b = 0xdeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0de

hint1 = 77759147870011250959067600299812670660963056658309113392093130
hint2 = 50608194198883881938583003429122755064581079722494357415324546

h1_high = 77759147870011250959067600299812670660963056658309113392093130  # Given hint1 from output.txt
h2_high = 50608194198883881938583003429122755064581079722494357415324546  # Given hint2 from output.txt

H1 = h1_high << 48
H2 = h2_high << 48
trunc = 48

# Define the polynomial ring
P = PolynomialRing(Zmod(p), names=('l1', 'l2'))
l1, l2 = P.gens()
# Equation from the relation between h1 and h2
num = a*(H1 + l1) - a - 1
den = a*(a+1)*(H1 + l1 - 1) - 1
pol = (H2 + l2) * den - num

# Construct a lattice basis
m = 4  # Degree of polynomial multiples
t = 2  # Dimension for LLL
X = 2^48  # Bound for l1
Y = 2^48  # Bound for l2

polys = []
for i in range(m + 1):
    for j in range(m + 1):
        polys.append((l1^j * l2^i) * pol)

# Build the lattice matrix
M = []
for poly in polys:
    row = []
    for coeff in poly.coefficients():
        row.append(coeff)
    M.append(row)

M = matrix(ZZ, M)
M = M.LLL()

# Check for small vectors (potential solutions)
for row in M:
    if row[0] == 0:
        continue  # Trivial solution
    # Reconstruct polynomial from row coefficients
    hx = sum(c * l1^i * l2^j for (i,j), c in zip(poly.monomials(), row))
    # Solve hx(l1, l2) = 0 over integers (small roots)
    # Here we use resultants or factorization (simplified)
    # In practice, use specialized tools or heuristic checks
    l1_val = l1_vars_from_hx(hx)  # Placeholder: extract l1, l2
    l2_val = l2_vars_from_hx(hx)
    if abs(l1_val) < X and abs(l2_val) < Y:
        h1 = (H1 + l1_val) % p
        h2 = (H2 + l2_val) % p
        # Recover x0 from h1
        x0 = (b * (1 - h1*(a + 1)) * inverse_mod(a*(a*h1 - 1), p)) % p
        # flag = int(x0).to_bytes(30, 'big')[:len_flag]
        print(x0)
        break

# # Function to map monomial exponents to column indices
# def monomial_to_index(exponents, max_degree):
#     index = 0
#     for i, exp in enumerate(exponents):
#         index += exp * (max_degree + 1)**i
#     return index

# # Function to construct the lattice basis
# def construct_lattice(pol, p, mm, tt, max_degree):
#     PR = pol.parent()
#     x, y = PR.gens()
#     polynomials = []
#     for k in range(mm):
#         for i in range(k, mm):
#             for j in range(max_degree + 1):
#                 poly = x**j * p**(mm - i) * pol**i
#                 polynomials.append(poly)
#     for k in range(tt):
#         for i in range(k, tt):
#             poly = y**k * pol**i
#             polynomials.append(poly)
#     return polynomials

# # Function to build the matrix from polynomials
# def build_matrix(polynomials, max_degree):
#     num_polys = len(polynomials)
#     num_monomials = (max_degree + 1)**2  # For two variables
#     MAT = matrix(ZZ, num_polys, num_monomials)
#     for row_idx, poly in enumerate(polynomials):
#         for monomial, coeff in poly.dict().items():
#             col_idx = monomial_to_index(monomial, max_degree)
#             MAT[row_idx, col_idx] = coeff
#     return MAT

# # Parameters for the attack
# mm = 4  # Adjust as needed
# tt = 2  # Adjust as needed
# max_degree = 2  # Adjust based on the polynomial degree

# # Construct the lattice basis
# polynomials = construct_lattice(pol, p, mm, tt, max_degree)

# # Build the matrix
# MAT = build_matrix(polynomials, max_degree)

# # LLL reduction
# MAT = MAT.LLL()

# # Reconstruct polynomials from reduced rows
# found = False
# for row in MAT:
#     if row.is_zero():
#         continue
#     # Reconstruct the polynomial from the row
#     poly_dict = {}
#     for col_idx in range(MAT.ncols()):
#         coeff = row[col_idx]
#         if coeff != 0:
#             # Reverse the monomial_to_index mapping
#             exp1 = col_idx % (max_degree + 1)
#             exp2 = col_idx // (max_degree + 1)
#             poly_dict[(exp1, exp2)] = coeff
#     hx = P(poly_dict)
#     # Find small roots
#     bounds = (2**48, 2**48)
#     for l1_candidate in range(-bounds[0], bounds[0] + 1):
#         for l2_candidate in range(-bounds[1], bounds[1] + 1):
#             if hx(l1=l1_candidate, l2=l2_candidate) == 0:
#                 l1, l2 = l1_candidate, l2_candidate
#                 h1 = (H1 + l1) % p
#                 h2 = (H2 + l2) % p
                
#                 # Compute x0 from h1
#                 numerator = b * (1 - h1 * (a + 1)) % p
#                 denominator = a * (a * h1 - 1) % p
#                 x0 = numerator * inverse_mod(denominator, p) % p
                
#                 # Convert x0 to bytes and extract the flag
#                 x0_bytes = int(x0).to_bytes(30, 'big')
#                 # flag = x0_bytes[:len(flag_part)]  # Adjust based on flag length
#                 print(x0_bytes)
#                 found = True
#                 break
#         if found:
#             break
#     if found:
#         break

# if not found:
#     print("Attack failed")


# # Convert to a system with lower degrees if possible
# # We need to construct a polynomial in l1 and l2 and find small roots
# # This is a simplified approach, actual implementation may need more steps

# # Load coppersmith implementation for multivariate (if available)
# # Alternatively, use the defund implementation or similar

# def multivariate_coppersmith_attack(pol, p, bounds, max_coeff=2^20):
#     PR = pol.parent()
#     x, y = PR.gens()
#     degree = pol.degree()
#     mm = 4  # Adjust as needed
#     tt = 2  # Adjust as needed
#     XX = bounds[0]
#     YY = bounds[1]
    
#     # Ensure polynomial is monic
#     pol = pol / pol.coefficients()[0]
    
#     # Construct lattice basis
#     polynomials = []
#     for k in range(mm):
#         for i in range(k, mm):
#             for j in range(degree + 1):
#                 poly = x**j * p**(mm - i) * pol**i
#                 polynomials.append(poly)
#     for k in range(tt):
#         for i in range(k, tt):
#             poly = y**(k) * pol**i
#             polynomials.append(poly)
    
#     # LLL reduction
#     MAT = matrix(ZZ, len(polynomials), (x.degree() + 1)*(y.degree() + 1))
#     # print("SOME? ", poly.dict().items())
#     for row_idx, poly in enumerate(polynomials):
#         for col_idx, coeff in poly.dict().items():
#             print("SOME: ", row_idx, col_idx)
#             MAT[row_idx, col_idx] = coeff
    
#     MAT = MAT.LLL()
    
#     # Reconstruct polynomials from reduced rows
#     found = False
#     for row in MAT:
#         if row.is_zero():
#             continue
#         hx = PR(row)
#         roots = hx.small_roots(X=XX, Y=YY)
#         if roots:
#             return roots
#     return None

# # Run the attack
# bounds = (2^48, 2^48)
# roots = multivariate_coppersmith_attack(pol, p, bounds)

# if roots:
#     l1, l2 = roots[0]
#     h1 = (H1 + int(l1)) % p
#     h2 = (H2 + int(l2)) % p
    
#     # Compute x0 from h1
#     numerator = b * (1 - h1 * (a + 1)) % p
#     denominator = a * (a * h1 - 1) % p
#     x0 = numerator * inverse_mod(denominator, p) % p
    
#     # Convert x0 to bytes and extract the flag
#     x0_bytes = int(x0).to_bytes(30, 'big')
#     # flag = x0_bytes[:len(flag_part)]  # Adjust based on flag length
#     print(x0_bytes)
# else:
#     print("Attack failed")