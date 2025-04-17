import requests

# IP address of the host running the Docker container (replace with the actual IP or domain)
host_ip = 'https://challs.polygl0ts.ch:9222'  # Replace <host_ip> with the IP of your host machine
secret_endpoint = '/secret'

def test_secret_access():
    try:
        # Attempt to access the /secret endpoint from an external IP (not 127.0.0.1)
        response = requests.get(f'{host_ip}{secret_endpoint}')
        
        if response.status_code == 200:
            print(f"Successfully accessed /secret: {response.text}")
        elif response.status_code == 403:
            print("Access denied as expected (403 Forbidden).")
        else:
            print(f"Unexpected response: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {host_ip}{secret_endpoint}: {e}")

if __name__ == "__main__":
    test_secret_access()
