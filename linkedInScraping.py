from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Initialize WebDriver (make sure to have the correct path to your WebDriver executable)
driver_path = 'C:\\chromedriver-win64\\chromedriver.exe'


def filter_keywords(prompt):
    # Simple example of keyword filtering (could be improved with NLP techniques)
    keywords = [word for word in prompt.split() if len(word) > 3]  # Filter words longer than 3 characters
    return keywords


def check_login_success(driver):
    try:
        current_url = driver.current_url
        print(f"Current URL: {current_url}")

        # Check for post-login element (update selector based on LinkedIn's layout)
        driver.find_element(By.CSS_SELECTOR, '.global-nav__me')  # Example selector, adjust if needed
        return True
    except Exception as e:
        print(f"Login check failed: {e}")
        return False


def get_candidate_details(keywords):
    chrome_service = Service(driver_path)
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--disable-gpu')  # Necessary for headless mode

    try:
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get('https://www.linkedin.com/login')

        # Log in to LinkedIn
        username = driver.find_element(By.ID, 'username')
        password = driver.find_element(By.ID, 'password')
        username.send_keys(os.getenv('LINKEDIN_USERNAME', 'shan57409@gmail.com'))  # Default value for testing
        password.send_keys(os.getenv('LINKEDIN_PASSWORD', 'Showkiipaa009'))  # Default value for testing
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        if not check_login_success(driver):
            print("Login failed or is not successful.")
            driver.quit()
            return []

        print(keywords)
        candidate_details = []
        for keyword in keywords:
            search_url = f'https://www.linkedin.com/search/results/all/?keywords={keyword}&origin=GLOBAL_SEARCH_HEADER'
            driver.get(search_url)
            time.sleep(5)
            print(driver)
            names = driver.find_elements(By.CSS_SELECTOR, 'span.actor-name')
            headlines = driver.find_elements(By.CSS_SELECTOR, 'p.subline-level-1')

            for name, headline in zip(names, headlines):
                candidate_details.append({
                    'name': name.text,
                    'headline': headline.text
                })

        driver.quit()
        return candidate_details

    except Exception as e:
        print(f"Error occurred: {e}")
        return []


@app.route('/post-candidates', methods=['POST'])
def get_candidates():
    data = request.get_json()
    prompt = data.get('prompt', '')

    # Filter keywords from the prompt
    keywords = filter_keywords(prompt)

    # Scrape candidate details from LinkedIn
    candidate_details = get_candidate_details(keywords)

    return jsonify({'candidates': candidate_details})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
