import os
import requests
from bs4 import BeautifulSoup

def get_page_with_img(session, task_url):
    response = session.get(task_url)
    if response.status_code != 200:
        print(f"Failed to fetch task page: {task_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    navbar = soup.find('header', id='oioioi-navbar')
    if navbar:
        navbar.decompose()
    new_soup_str = str(soup)
    
    img_tags = soup.find_all('img')
    for img in img_tags:
        img_url = img.get('src')
        print(img_url)
        if not img_url:
            continue
        current_url = response.url
        img_url = requests.compat.urljoin(current_url, img_url)
        img_name = img_url.split('/')[-1]
        img_path = os.path.join("pdfs", task_url.split('/')[-2], img_name)

        img_response = session.get(img_url)
        if img_response.status_code != 200:
            print(f"Failed to fetch image: {img_url}")
            continue
        
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        with open(img_path, 'wb') as img_file:        
            img_file.write(img_response.content)
        print(f"Saved image: {img_path}")
        new_soup_str = new_soup_str.replace(f'src="{str(img.get('src'))}"', f'src="{str(os.path.join(task_url.split('/')[-2], img_name))}"')
    with open(os.path.join("pdfs", task_url.split('/')[-2] + ".html"), 'w') as html_file:
        html_file.write(new_soup_str)