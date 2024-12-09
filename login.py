import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sio2.staszic.waw.pl"
LOGIN_URL = f"{BASE_URL}/c/kolko-informatyczne-archiwum/login/"  # Replace with the actual login URL if different
START_URL = f"{BASE_URL}/c/matex_k19_a4_js/p/"
USERNAME = "Michal_par"  # Replace with your username
PASSWORD = "Rupapupa11"  # Replace with your password
options = {
    'no-images': None  # Optionally disable images
    # 'no-javascript': None,  # Optionally disable JS
}

def login():
    # Start a session
    session = requests.Session()
    
    # Get login page to fetch any necessary CSRF token or cookies
    login_page = session.get(LOGIN_URL)
    if login_page.status_code != 200:
        print("Failed to load login page.")
        return

    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    # Extract CSRF token if needed
    csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})
    csrf_token = csrf_token['value'] if csrf_token else None

    # Prepare login payload
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    if csrf_token:
        payload["csrfmiddlewaretoken"] = csrf_token

    # Post login request
    headers = {
        "Referer": LOGIN_URL
    }
    login_response = session.post(LOGIN_URL, data=payload, headers=headers)
    if login_response.status_code != 200 or "logout" not in login_response.text:
        print("Login failed.")
        return

    print("Login successful.")
    return session

