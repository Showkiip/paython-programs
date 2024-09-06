import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector

# Parameters
search_query = 'site:linkedin.com/in/ AND "python developer" AND "London"'
file_name = 'results_file.csv'
linkedin_username = 'shan57409@gmail.com'
linkedin_password = 'Showkiipaa009'

# Initialize WebDriver
service = Service('C:\\chromedriver-win64\\chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.linkedin.com')

# Login to LinkedIn
try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'session_key'))
    )
    username.send_keys(linkedin_username)

    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'session_password'))
    )
    password.send_keys(linkedin_password)

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
    )
    sign_in_button.click()
except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit()

# Perform Google search
driver.get('https://www.google.com')
try:
    search_query_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_query_element.send_keys(search_query + Keys.RETURN)
except Exception as e:
    print(f"Error during search: {e}")
    driver.quit()
    exit()

# Extract LinkedIn URLs
try:
    linkedin_urls = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'iUh30'))
    )
    linkedin_urls = [url.text for url in linkedin_urls]
except Exception as e:
    print(f"Error extracting LinkedIn URLs: {e}")
    driver.quit()
    exit()

# Open CSV file for writing
with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])

    # For each LinkedIn URL, extract data
    for linkedin_url in linkedin_urls:
        driver.get(linkedin_url)
        sleep(10)

        sel = Selector(text=driver.page_source)

        name = sel.xpath('//h1/text()').get(default='No results').strip()
        job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').get(default='No results').strip()
        company = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__company-name")]/text()').get(default='No results').strip()
        college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__school-name")]/text()').get(default='No results').strip()
        location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').get(default='No results').strip()
        linkedin_url = driver.current_url

        # Print the output to the terminal
        print('\n')
        print(f'Name: {name}')
        print(f'Job Title: {job_title}')
        print(f'Company: {company}')
        print(f'College: {college}')
        print(f'Location: {location}')
        print(f'URL: {linkedin_url}')
        print('\n')

        # Write to CSV file
        writer.writerow([name, job_title, company, college, location, linkedin_url])

# Quit the driver
driver.quit()
