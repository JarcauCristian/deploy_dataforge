import argparse
import requests

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--address", type=str, help="Hostname for UI.")

args = parser.parse_args()


def main():
    keycloak_url = "https://localhost:30442"
    
    data = {
        "username": "admin",
        "password": "sup3r_s3cr3t_password",
        "client_id": "admin-cli",
        "grant_type": "password"
    }
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    token_response = requests.post(f"{keycloak_url}/auth/realms/master/protocol/openid-connect/token", headers=headers, data=data)

    if token_response.status_code != 200:
        exit(1)
    
    token = token_response.json()['access_token']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    url = f"{keycloak_url}/auth/admin/realms"

    payload = {
        "realm": "react-keycloak",
        "enabled": True
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 201:
        exit(1)
    
    payload = {
        "clientId": "reactClient",
        "enabled": True,
        "redirectUris": [
            "https://localhost:31491" if args.address is None else args.host
        ],
        "publicClient": False,
    }

    url = f"{keycloak_url}/auth/admin/realms/react-keycloak/clients"

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code not in [201, 204]:
        exit(1)

    url = f"{keycloak_url}/auth/admin/realms/react-keycloak/clients"

    response = requests.get(url, headers=headers, params={"clientId": "reactClient"})
    clients = response.json()

    client_uuid = next((client['id'] for client in clients if client['clientId'] == "reactClient"), None)

    if not client_uuid:
        exit(1)
    
    role_url = f"{keycloak_url}/auth/admin/realms/react-keycloak/clients/{client_uuid}/roles"
    role_data = {
        "name": "data-producer",
    }

    response = requests.post(role_url, json=role_data, headers=headers)

    if response.status_code not in [201, 204]:
        exit(1)

    role_data = {
        "name": "data-scientist",
    }

    response = requests.post(role_url, json=role_data, headers=headers)

    if response.status_code not in [201, 204]:
        exit(1)

    user_data = {
        "username": "tokenUser",
        "enabled": True,
        "firstName": "New",
        "lastName": "User",
        "email": "newuser@example.com",
        "credentials": [
            {
                "type": "password",
                "value": "token",
                "temporary": False  # Set to True if you want the user to update the password at first login
            }
        ],
        "attributes": {
            "customAttribute": "customValue"  # Example of adding a custom attribute
        }
    }

    response = requests.post(url, json=user_data, headers=headers)

    if response.status_code != 201:
        exit(1)

if __name__ == '__main__':
    main()
