# Pseudocode
options = ["encrypt", "get_pk"]

class Oracle:
    def __init__(self):
        self.A, self.b, self.q, self.s, self.e = Kyber512()
        self.N = self.A.shape[1]
        self.b = list(self.b)
        self.b = [[int(x)] for x in self.b]
        set_modulus(self.q)
        self.r = new_vector([random.randint(0, 1) for _ in range(self.N)])

    def encrypt(self, m):
        if m not in {0, 1}:
            raise ValueError("Message must be 0 or 1.")
        
        u = multiply(transpose(self.A), self.r)
        v = dotproduct(self.b, self.r) + (self.q // 2) * m

        return (u, v)
    
    def encrypt_string(self, binary_string):
        return [self.encrypt(int(bit)) for bit in binary_string]

    def query(self, query_type, *args):
        if query_type == 'encrypt':
            print(self.encrypt_string(*args))
            return "🥒 Encrypted String 🥒"
        elif query_type == 'get_pk':
            print((self.A, self.b))
            return "📝 Wrote public key 📝"
        else:
            raise ValueError("Unknown query type.")

if __name__ == "__main__":
    oracle = Oracle()
    print("Welcome to", end="")
    logo_art = r"""
        _       __          ________ _     
        | |      \ \        / /  ____( )    
        | |     __\ \  /\  / /| |__  |/ ___ 
        | |    / _ \ \/  \/ / |  __|   / __|
        | |___| (_) \  /\  /  | |____  \__ \
        |______\___/ \/  \/   |______| |___/
    """
    print(logo_art)

    print("Tools in-stock:")
    for o in options:
        print(" " + o)

    while True:
        option = input("What tool would you like to add to your cart?: ")
        if option not in options:
            print("Invalid option")
            continue

        binary_string = ""
        if option=='encrypt':
            binary_string = input("Enter the purchase code associated with this tool in binary: ").replace(" ", "")

        res = oracle.query(option, binary_string)
        print("res: ", res)