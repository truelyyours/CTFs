from pwn import *
from z3 import *

HOST = "connect.umbccd.net"
PORT = 25185


conn = remote(HOST, PORT)
# Helper functions
def custom_recvline():
    print(conn.recvline().decode().strip())
def custom_recvuntil(delim):
    print(conn.recvuntil(delim).decode().strip())


def get_abn(outputs):
    "Recover the a, b and N values given some consecutive outputs"
    a = Int('a')
    b = Int('b')
    N = Int('N')

    s = [Int(f's{i}') for i in range(len(outputs))]

    solver = Solver()

    # Set known outputs
    for i, val in enumerate(outputs):
        solver.add(s[i] == val)

    # Add recurrence relation constraints
    for i in range(1, len(outputs)):
        solver.add(s[i] == (a * s[i-1] + b) % N)

    # Optionally: set bounds for N, a, b
    solver.add(N > 1)
    solver.add(a > 0, b >= 0)

    if solver.check() == sat:
        model = solver.model()
        a_val = model[a].as_long()
        b_val = model[b].as_long()
        N_val = model[N].as_long()
    print(f"Recovered a = {a_val}, b = {b_val}, N = {N_val}")
    return (a_val, b_val, N_val)

def get_admin_password(a, b, N, outputs):
    """Return the initial state i.e. admin password here given a, b, N and some outputs"""
    init = Int('init')

    # Build recurrence
    solver = Solver()

    state = init
    for i, val in enumerate(outputs):
        state = (a * state + b) % N
        solver.add(state == val)

    if solver.check() == sat:
        model = solver.model()
        init_val = model[init].as_long()
        print(f"Recovered initial seed: {init_val}")
        return init_val

def recv_menu1():
    "Recv the initial and after login menu"
    for _ in range(7):
        custom_recvline()

def recv_menu3():
    """Recv the handle notes menu"""
    for _ in range(5):
        custom_recvline()

def send_choice(choice):
    """Send the choice to server"""
    custom_recvuntil(b'> ')
    conn.sendline(choice.encode())

def send_name(name):
    """Send the name and get it's password. 
    Return the password."""
    custom_recvuntil(b'name: ')
    conn.sendline(name.encode())
    custom_recvuntil(b' is: ')
    passwd = int(conn.recvline().decode().strip())
    custom_recvline()
    return passwd

# collection of all the output numbers
opt = []
custom_recvline()
recv_menu1()
# get 5 consecutive ouputs
for i in range(5):
    send_choice('1')
    passwd = send_name(str(i))
    opt.append(passwd)
    recv_menu1()

a, b, N = get_abn(opt)
# Now lets get the initial state
admin_passwd = get_admin_password(a, b, N, opt)
 
print("Admin password is: ", admin_passwd)

# Login as admin
send_choice('2')
custom_recvuntil(b'name: ')
conn.sendline(b'admin')
custom_recvuntil(b'password: ')
conn.send(str(admin_passwd) + '\n')
custom_recvline()
custom_recvline()

recv_menu1()
send_choice('3')
custom_recvline()
custom_recvline()
# custom_recvline()
# custom_recvline()

# DawgCTF{PRNGs_d0nt_m4k3_f0r_g00d_p455w0rd5}


