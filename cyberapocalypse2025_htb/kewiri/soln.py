# SOLVED:
from pwn import *
from sage.all import *

HOST = "94.237.57.230"
PORT = 37513

conn = remote(HOST, PORT)

def my_recvline(n):
    for _ in range(n):
        print(conn.recvline().decode(), end='')

my_recvline(2)
prime_p = int(conn.recvline().decode().strip().split(' ')[-1])
print("PRIME p::: ", prime_p)

print(conn.recvuntil(b'>').decode())
conn.sendline(str(prime_p.bit_length()).encode())

facts = [ (2, 2),(5,1),
(635599, 1),
(2533393, 1),
(4122411947, 1),
(175521834973, 1),
(206740999513, 1),
(1994957217983, 1),
(215264178543783483824207, 1),
(10254137552818335844980930258636403, 1)]

print(conn.recvuntil(b'>').decode())
# my_recvline(1)

formatted_str = str(facts[0][0]) + ','
for i in range(len(facts) - 1):
    formatted_str += str(facts[i][1]) + "_" + str(facts[i+1][0]) + ','
formatted_str += str(facts[-1][1])
conn.sendline(formatted_str.encode())
my_recvline(1)

p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
F = GF(p)  # Finite field F_p

for _ in range(17):
    third = conn.recvuntil(b'>', drop=True).decode().strip()
    # print(third.split(' '))
    g = int(third.split(' ')[-1][:-1])
    # print("GENERATOR:: ", g)

    # SAGEMATH SCRIPT
    # ******************************************************************

    g = F(g)   # Convert g to an element of F_p

    # Compute p-1 and its factorization
    order = p - 1
    # factors = factor(order)

    # Check if g is a generator
    is_generator = all(g**(order // q) != 1 for q, _ in facts)

    # print(is_generator == True)

    # ******************************************************************
    conn.sendline(str(int(is_generator)).encode())

my_recvline(1)
a = int(conn.recvline().decode().strip().split(' ')[-1])
b = int(conn.recvline().decode().strip().split(' ')[-1])
print("a AND b :: ", a, b)
print(conn.recvuntil(b'>').decode())

E = EllipticCurve(F, [a, b])

# order_E = E.cardinality()
order_E = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
print("ORDER OF E: ", order_E)

conn.sendline(str(order_E).encode())
# my_recvline(1)

print(conn.recvuntil(b'>').decode())

# F_3 = GF(pow(p, 3))
# E_3 = EllipticCurve(F_3, [a, b])
# order_E_3 = p**3 + 3*p
order_E_3 = 9547468349770605965573984760817208987986240857800275642666264260062210623470017904319931275058250264223830562439645572562493214488086970563135688265933076141657703804791593446020774169988605421998202682898213433784381043211278976059744771523119218399190407965593665262490269084642700982261912090274007278407746985341700600062580644280196871035164

fact_3 = [(2, 2),
 (7, 2),
 (order_E, 1),
 (2296163171090566549378609985715193912396821929882292947886890025295122370435191839352044293887595879123562797851002485690372901374381417938210071827839043175382685244226599901222328480132064138736290361668527861560801378793266019,
  1)]
factorization_str = "_".join(f"{factor},{exp}" for factor, exp in fact_3)
# print("Factorization string for order :: ", factorization_str)

conn.sendline(factorization_str.encode())
my_recvline(1)

# 6th finall challenge
print(conn.recvuntil(b':').decode())
G_x = int(conn.recvline().decode().strip().split(' ')[-1])
print(conn.recvuntil(b':').decode())
A_x = int(conn.recvline().decode().strip().split(' ')[-1])
def is_on_curve(x_coord):
    """
    Check if there exists a y such that (x,y) is on the curve
    y^2 = x^3 + ax + b
    """

    rhs = x_coord^3 + a*x_coord + b
    try:
        # Check if rhs is a quadratic residue
        y = sqrt(rhs)
        return True
    except:
        return False

print("G_x and A_x: ", G_x, A_x)
print()
print("ARE ON CRUVE?: ", is_on_curve(G_x), is_on_curve(A_x))

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

G = E.lift_x(ZZ(G_x))
A = E.lift_x(ZZ(A_x))

print()
d = SmartAttack(G, A, ZZ(p))
print("SMART attack d: ", d)
print(conn.recvuntil(b'>').decode())
conn.sendline(str(d).encode())

my_recvline(2)
# FLAG IS: HTB{Welcome_to_CA_2k25!Here_is_your_anomalous_flag_for_this_challenge_and_good_luck_with_the_rest:)_97639b5b26cd3d761d5eaa0daa358fbe}