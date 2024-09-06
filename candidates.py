from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# User-agents list
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
]

def get_random_user_agent():
    return random.choice(user_agents)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if needed
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Optionally add a random user-agent if you want to rotate user agents
    user_agent = get_random_user_agent()
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login_to_linkedin(driver):
    try:
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        driver.find_element(By.ID, "username").send_keys("shan57409@gmail.com")
        driver.find_element(By.ID, "password").send_keys("Showkiipaa009")
        driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        WebDriverWait(driver, 20).until(
            EC.url_changes("https://www.linkedin.com/login")
        )
    except TimeoutException:
        print("TimeoutException: Unable to login, check the login page or credentials.")
        driver.quit()
    except NoSuchElementException as e:
        print(f"NoSuchElementException: {e}")
        driver.quit()
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        driver.quit()

def scrape_profiles(driver):
    try:
        driver.get("https://www.linkedin.com/search/results/people/")

        # Debugging: Print the page source to check if the page loaded correctly
        print(driver.page_source)

        # Wait for the profiles to be loaded
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.entity-result__title-text'))
        )
        profiles = driver.find_elements(By.CSS_SELECTOR, '.entity-result__title-text')
        profile_data = [profile.text for profile in profiles]
        return profile_data
    except TimeoutException:
        print("TimeoutException: Timed out waiting for page to load or element to be present.")
        print("Page URL:", driver.current_url)
        print("Current page source length:", len(driver.page_source))
        return []
    except NoSuchElementException as e:
        print(f"NoSuchElementException: {e}")
        return []
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        return []

def main():
    driver = setup_driver()
    try:
        login_to_linkedin(driver)
        profile_data = scrape_profiles(driver)
        if profile_data:
            print("Profiles scraped:")
            for profile in profile_data:
                print(profile)
        else:
            print("No profiles found.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
