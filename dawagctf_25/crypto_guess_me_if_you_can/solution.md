# Guess Me If You Can
Check out the note-taking app I created! I heard users are really bad at picking passwords, so I made a really really secure number generator to give users passwords! Good luck trying to break it now.

nc connect.umbccd.net 25185

# Solution

It is evident from the `server.py` code that it s a simple LCG. So we use `Z3` to guess the `a`, `b`, and `N` values.
```
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
```

Then we also obtain the initial state i.e. admin's password.
```
def get_seed(a, b, N, outputs):
    """Return the initial seed given a, b, N and some outputs"""
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
```

After this, we simply login as admin and selection option 3 of manage notes where we'll find the flag.

## Flag
DawgCTF{PRNGs_d0nt_m4k3_f0r_g00d_p455w0rd5}

