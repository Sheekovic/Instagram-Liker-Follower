import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from faker import Faker
import time

# Function to create a SQLite database connection and create a table
def create_database():
    connection = sqlite3.connect('fake_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fake_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    connection.commit()
    return connection, cursor

# Function to insert fake data into the database
def insert_into_database(connection, cursor, email, username, password):
    cursor.execute('''
        INSERT INTO fake_data (email, username, password)
        VALUES (?, ?, ?)
    ''', (email, username, password))
    connection.commit()


def generate_random_data():
    fake = Faker()
    email = fake.email().split('@')[0] + '@gmail.com'
    username = fake.user_name()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return email, username, password


def open_chrome_and_fill_form(link):
    # Create Chrome options
    chrome_options = Options()

    # Uncomment the line below if you want to run Chrome in headless mode (without a visible browser window)
    # chrome_options.add_argument('--headless')

    # Create a SQLite database and table
    connection, cursor = create_database()

    while True:
        # Create a Chrome webdriver instance with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the specified link
            driver.get(link)

            # Pause for 5 seconds to allow the page to load
            time.sleep(5)

            try:
                # Find and click the like button
                like_button_xpath = "//button[@class='flex justify-center items-center gap-2 rounded-full bg-gradient-to-br from-[#FFEFBE] to-[#dbc172] py-3 px-4 text-black']"
                like_button = driver.find_element(By.XPATH, like_button_xpath)
                like_button.click()

                # Pause for 5 seconds to allow the page to load after clicking the like button
                time.sleep(2)

                # Find and click the "Register here" button
                register_button_xpath = "//button[@class='text-sm text-primary-500 underline']"
                register_button = driver.find_element(By.XPATH, register_button_xpath)
                register_button.click()

                # Pause for 5 seconds to allow the registration form to load
                time.sleep(2)

                # Generate random data
                email, username, password = generate_random_data()

                # Fill out the registration form
                email_input = driver.find_element(By.ID, "email-input")
                username_input = driver.find_element(By.ID, "username-input")
                password_input = driver.find_element(By.ID, "password-input")

                email_input.send_keys(email)
                username_input.send_keys(username)
                password_input.send_keys(password)

                time.sleep(2)

                # Find and click the "Create account" button
                create_account_button = driver.find_element(By.ID, "submit")
                create_account_button.click()

                # Pause for 5 seconds to observe the filled form (you can adjust the time as needed)
                time.sleep(2)

                # Find and click the like button again
                likes_button_xpath = "//button[@class='flex justify-center items-center gap-2 rounded-full bg-gradient-to-br from-[#FFEFBE] to-[#dbc172] py-3 px-4 text-black']"
                likes_button = driver.find_element(By.XPATH, likes_button_xpath)
                likes_button.click()

                # Pause for 5 seconds to allow the page to load after clicking the like button
                time.sleep(2)

                # Insert data into the database
                insert_into_database(connection, cursor, email, username, password)

            except ElementClickInterceptedException as e:
                print(f"ElementClickInterceptedException: {e}")
                print("Continuing with the script...")

            except NoSuchElementException:
                print("Error: Unable to find the specified parent element, like button, or registration form.")

        finally:
            # Close the browser window
            driver.quit()

if __name__ == "__main__":
    # Replace 'https://example.com' with the link you want to open
    target_link = 'https://renderz.app/team-of-the-year/vote/GxebbSVgXlcwTuD'
    
    open_chrome_and_fill_form(target_link)
