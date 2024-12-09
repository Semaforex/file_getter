import os
import requests
from bs4 import BeautifulSoup
import pdfkit

BASE_URL = "https://sio2.staszic.waw.pl"
LOGIN_URL = f"{BASE_URL}/login/"  # Replace with the actual login URL if different
START_URL = f"{BASE_URL}/c/matex_k19_a4_js/p/"
USERNAME = "Michal_par"  # Replace with your username
PASSWORD = "Rupapupa11"  # Replace with your password
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

def login_and_save_pages():
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

    # Create a directory to store PDFs
    os.makedirs("pdfs", exist_ok=True)

    # Fetch the main page
    response = session.get(START_URL)
    if response.status_code != 200:
        print("Failed to fetch the main page.")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all task links
    task_links = soup.find_all("a", href=True)
    task_links = [link['href'] for link in task_links if "/c/matex_k19_a4_js/p/" in link['href']]
    
    for link in set(task_links):  # Remove duplicate links
        task_url = f"{BASE_URL}{link}"
        print(f"Visiting: {task_url}")
        
        # Fetch task page
        task_response = session.get(task_url)
        if task_response.status_code != 200:
            print(f"Failed to fetch task page: {task_url}")
            continue
        
        # Check if content is a PDF
        content_type = task_response.headers.get('Content-Type', '')
        file_name_base = link.split('/')[-2]
        
        if "application/pdf" in content_type:
            # Save as PDF
            file_name = os.path.join("pdfs", file_name_base + ".pdf")
            with open(file_name, 'wb') as pdf_file:
                pdf_file.write(task_response.content)
            print(f"Saved PDF: {file_name}")
        else:
            # Convert and save as PDF with "try-" prefix
            try_file_name = os.path.join("pdfs", "try-" + file_name_base + ".pdf")
            pdfkit.from_url(task_url, try_file_name, configuration=config)

if __name__ == "__main__":
    login_and_save_pages()
