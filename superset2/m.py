from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import zipfile

# Set up the Firefox web driver
driver = webdriver.Firefox()

# Navigate to the Box.com login page and enter your login credentials
driver.get("https://www.box.com/login")
driver.find_element_by_id("login-email").send_keys("your_email")
driver.find_element_by_id("login-password").send_keys("your_password")
driver.find_element_by_name("login").click()

# Define the root folder URL and navigate to it
root_folder_url = "https://www.box.com/files/0"
driver.get(root_folder_url)

# Define the download directory
download_dir = "/path/to/download/directory"

# Define a function to download a folder and its contents recursively
def download_folder(driver, folder_url, download_dir):
    # Navigate to the folder URL
    driver.get(folder_url)

    # Wait for the folder contents to load
    time.sleep(2)

    # Get the folder name and create a subdirectory for it
    folder_name = driver.find_element_by_css_selector("span.breadcrumbs-item-text").text
    subdirectory = os.path.join(download_dir, folder_name)
    os.makedirs(subdirectory, exist_ok=True)

    # Download all files in the folder
    file_links = driver.find_elements_by_css_selector("a.item-name-link")
    for file_link in file_links:
        file_url = file_link.get_attribute("href")
        file_name = file_link.text
        file_path = os.path.join(subdirectory, file_name)
        driver.get(file_url)
        download_link = driver.find_element_by_css_selector("a.download-file-link")
        download_link.click()
        while not os.path.exists(file_path):
            time.sleep(1)

    # Download all subfolders and their contents
    folder_links = driver.find_elements_by_css_selector("a.item-name-link.folder")
    for folder_link in folder_links:
        folder_url = folder_link.get_attribute("href")
        download_folder(driver, folder_url, subdirectory)

# Call the function to download the root folder and its contents
download_folder(driver, root_folder_url, download_dir)

# Close the web driver
driver.quit()
