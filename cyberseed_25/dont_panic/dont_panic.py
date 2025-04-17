import functools

def hidden_key():
    return 22

encoded_flag = [69, 93, 79, 59, 78, 89, 68, 68, 59, 36, 47, 32, 33]

def check_flag(user_input):
    key = hidden_key()
    decoded_flag = ''.join(chr(c ^ key) for c in encoded_flag)
    return user_input == decoded_flag

user_input = input("Enter the flag: ")

if check_flag(user_input):
    print("Correct! You found the flag.")
else:
    print("Try again!")