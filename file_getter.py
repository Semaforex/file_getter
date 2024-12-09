import os
import requests
from bs4 import BeautifulSoup
import pdfkit
from get_page_with_imgs import get_page_with_img
from login import login

BASE_URL = "https://sio2.staszic.waw.pl"
LOGIN_URL = f"{BASE_URL}/login/"  # Replace with the actual login URL if different
START_URL = f"{BASE_URL}/c/matex_k19_a4_js/p/"
USERNAME = "Michal_par"  # Replace with your username
PASSWORD = "Rupapupa11"  # Replace with your password
options = {
    'no-images': None  # Optionally disable images
    # 'no-javascript': None,  # Optionally disable JS
}

def login_and_save_pages():
    session = login()

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
        response = session.get(task_url)
        
        if "application/pdf" in content_type:
            # Save as PDF
            file_name = os.path.join("pdfs", file_name_base  + ".pdf")
            with open(file_name, 'wb') as pdf_file:
                pdf_file.write(task_response.content)
            print(f"Saved PDF: {file_name}")
        else:
            # Convert and save as PDF with "try-" prefix
            # try_file_name = os.path.join("pdfs", "try-" + file_name_base + ".pdf")
            # soup = BeautifulSoup(response.text, 'html.parser')
            # img_tags = soup.find_all('img')
            # for img in img_tags:
            #     img_url = img.get('src')
            #     if not img_url:
            #         continue
            #     img_name = img_url.split('/')[-1]
            #     img['src'] = f'images/{img_name}'
            # for img in img_tags:
            #     img_url = img.get('src')
            #     if not img_url:
            #         continue
            #     img_url = task_url + img_url
            #     img_name = img_url.split('/')[-1]
            #     img_path = os.path.join("pdfs", img_name)

            get_page_with_img(session, task_url)

        
            try:
                with open(os.path.join("pdfs", file_name_base + ".html"), 'w', encoding='utf-8') as txt_file:
                    txt_file.write(response.text)
                pdfkit.from_string(response.text, try_file_name, options=options)
            except:
                pass

if __name__ == "__main__":
    login_and_save_pages()
