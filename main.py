import random
import sqlite3
import string
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from faker import Faker
import time

# List of domains
domains = [
    "1secmail.com",
    "1secmail.org",
    "1secmail.net",
    "icznn.com",
    "ezztt.com",
    "vjuum.com",
    "laafd.com",
    "txcct.com"
]

user_agents = [
    # Chrome user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.43",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/84.0.4316.90",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.43",
    # Firefox user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/92.0",
    # Safari user agents
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    # Edge user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.43",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.43",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.43",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.43",
    # Opera user agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/84.0.4316.90",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/84.0.4316.90",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/84.0.4316.90",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 OPR/84.0.4316.90",
]

def create_database(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS insta_accs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            fullname TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    connection.commit()
    return connection, cursor  # Return the connection and cursor objects




def initialize_database():
    connection = sqlite3.connect('temp_emails.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS temp_emails (
                      id INTEGER PRIMARY KEY,
                      email TEXT NOT NULL UNIQUE,
                      used INTEGER DEFAULT 0)''')
    connection.commit()
    connection.close()


def insert_email_into_database(email):
    connection = sqlite3.connect('temp_emails.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temp_emails (email) VALUES (?)", (email,))
    connection.commit()
    connection.close()

def fetch_unused_email_from_database():
    connection = sqlite3.connect('temp_emails.db')
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM temp_emails WHERE used = 0 LIMIT 1")
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None

def mark_email_as_used(email):
    connection = sqlite3.connect('temp_emails.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE temp_emails SET used = 1 WHERE email = ?", (email,))
    connection.commit()
    connection.close()

def generate_random_username(length):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_temp_email(domain):
    username_length = random.randint(6, 12)
    username = generate_random_username(username_length)
    return f"{username}@{domain}"

def save_temp_emails(domains):
    domain = random.choice(domains)
    email = generate_temp_email(domain)
    insert_email_into_database(email)
    return email

def fetch_last_message(username, domain):
    api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
    response = requests.get(api_url)
    if response.status_code == 200:
        messages = response.json()
        if messages:
            last_message = messages[-1]  # Get the last message
            subject = last_message.get('subject', 'No subject')  # Get the subject of the last message
            return subject
        else:
            print("No messages found.")
            return None
    else:
        print(f"Failed to fetch messages. Status code: {response.status_code}")
        return None

# Function to insert fake data into the database
def insert_into_database(connection, cursor, email, username, password):
    cursor.execute('''
        INSERT INTO insta_accs (email, username, password)
        VALUES (?, ?, ?)
    ''', (email, username, password))
    connection.commit()

# Function to fetch an email from the database
def fetch_email_from_database(cursor):
    cursor.execute("SELECT email FROM temp_emails WHERE used = 0 LIMIT 1")
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        print("No unused email found in the database.")
        return None

# Modify the open_chrome_and_fill_form() function to accept a cursor for the temp_emails database
def open_chrome_and_fill_form(link, temp_emails_cursor, filename, domains):
    # Create Chrome options
    chrome_options = Options()

    initialize_database()
    

    # Uncomment the line below if you want to run Chrome in headless mode (without a visible browser window)
    # chrome_options.add_argument('--headless')
    # Rotate user agents
    user_agent = random.choice(user_agents)
    print(user_agent)
    chrome_options.add_argument(f'user-agent={user_agent}')


    # Create a SQLite database and table
    connection, cursor = create_database(filename)

    while True:
        # Create a Chrome webdriver instance with the specified options
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Navigate to the specified link
            driver.get(link)

            # Pause for 5 seconds to allow the page to load
            time.sleep(random.uniform(5, 10))

            try:
                # Find and click the like button
                like_button_xpath = "//a[@class='x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37 xjypj1w x3nfvp2']"
                like_button = driver.find_element(By.XPATH, like_button_xpath)
                like_button.click()

                # Pause for 5 seconds to allow the registration form to load
                time.sleep(random.uniform(2, 4))

                # Fetch email from the database
                email = fetch_email_from_database(temp_emails_cursor)
                print(email)
                if email:
                    # Generate random username and password
                    fake = Faker()
                    full_name = fake.name()
                    parts = full_name.split()
                    first_name = parts[0]
                    last_name = parts[-1]
                    initials = first_name[0] + last_name[0]
                    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                    username = initials.lower() + random_chars
                    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

                    # Split the email into username and domain
                    mailname, maildomain = email.split('@')
                    print("Username:", mailname)
                    print("Domain:", maildomain)

                    # Fill out the registration form
                    email_input = driver.find_element(By.NAME, "emailOrPhone")
                    # Find the input field by name attribute
                    full_name_input = driver.find_element(By.NAME, "fullName")
                    # Find and fill the username input field
                    username_input = driver.find_element(By.NAME, "username")
                    # Find and fill the password input field
                    password_input = driver.find_element(By.NAME, "password")


                    email_input.send_keys(email)
                    full_name_input.send_keys(full_name)
                    username_input.send_keys(username)
                    password_input.send_keys(password)

                    time.sleep(random.uniform(2, 4))

                    mark_email_as_used(email)
                    print(f"{email} marked as used")
                    domain = random.choice(domains)
                    new_email = generate_temp_email(domain)
                    print("New Email:", new_email)

                    

                    # Find and click the "Sign up" button
                    signup_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    signup_button.click()


                    # Wait for the page to load
                    time.sleep(random.uniform(3, 5))
                    # Generate random month, day, and year
                    random_month = random.randint(1, 12)
                    random_day = random.randint(1, 28)
                    random_year = random.randint(1980, 2000)

                    # Convert the month integer to its corresponding name
                    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    random_month_name = months[random_month - 1]  # Subtract 1 because list indices start from 0

                    # Fill the birthday form fields with random values
                    month_dropdown = driver.find_element(By.CSS_SELECTOR, "select[title='Month:']")
                    month_dropdown.send_keys(random_month_name)

                    day_dropdown = driver.find_element(By.CSS_SELECTOR, "select[title='Day:']")
                    day_dropdown.send_keys(str(random_day))  # Convert integer to string

                    year_dropdown = driver.find_element(By.CSS_SELECTOR, "select[title='Year:']")
                    year_dropdown.send_keys(str(random_year))  # Convert integer to string
                    
                    # Wait for the action to complete
                    time.sleep(random.uniform(3, 5))

                    # Click the Next button
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")
                    next_button.click()

                    # Wait for the action to complete
                    time.sleep(random.uniform(3, 5))

                    # Find the element with the specified class
                    popup_element = driver.find_element(By.CLASS_NAME, "x1cy8zhl")

                    # Check if the element is present
                    if popup_element:
                        # Close the popup by clicking on the close button
                        close_button = popup_element.find_element(By.CSS_SELECTOR, "button[type='button']")
                        close_button.click()
                        time.sleep(random.uniform(3, 5))
                        next_button = driver.find_element(By.XPATH, "//button[text()='Next']")
                        next_button.click()
                    else:
                        continue

                    # Wait for the action to complete
                    time.sleep(random.uniform(3, 5))

                    # Find the "Next" button element
                    # next_button = driver.find_element(By.XPATH, "//button[text()='Next']")

                    # Click the "Next" button
                    # next_button.click()

                    # Set a timeout for how long to wait for the confirmation code (in seconds)
                    timeout = 300  # Adjust this value as needed

                    start_time = time.time()

                    while time.time() - start_time < timeout:
                        # Get the confirmation code from the last message subject
                        last_subject = fetch_last_message(mailname, maildomain)  # Replace with your actual username and domain

                        if last_subject:
                            # Check if the confirmation code is received
                            if "is your Instagram code" in last_subject:
                                # Extract the 6-digit code from the subject
                                confirmation_code = last_subject.split()[0]  # Extract the first word, which is the 6-digit code
                                print("Confirmation Code:", confirmation_code)
                                # Now you can fill the confirmation code in the input field
                                confirmation_code_input = driver.find_element(By.NAME, "email_confirmation_code")  # Assuming you have a WebDriver instance named 'driver'
                                confirmation_code_input.send_keys(confirmation_code)
                                break  # Exit the loop once the confirmation code is received
                            else:
                                print("Confirmation code not received yet. Waiting...")
                                time.sleep(random.uniform(5, 10))  # Wait for 10 seconds before checking again
                        else:
                            print("No confirmation code found.")

                    # If the loop completes without finding the confirmation code
                    else:
                        print("Timeout: Confirmation code not received within the specified time.")

                    time.sleep(random.uniform(3, 5))
                    # Find the button element by its class name
                    final_next_button = driver.find_element(By.CSS_SELECTOR, ".x1i10hfl.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x972fbf.xcfux6l.x1qhh985.xm0m39n.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x18d9i69.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x1lku1pv.x1a2a7pz.x6s0dn4.xjyslct.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.x9bdzbf.x1ypdohk.x1f6kntn.xwhw2v2.x10w6t97.xl56j7k.x17ydfre.x1swvt13.x1pi30zi.x1n2onr6.x2b8uid.xlyipyv.x87ps6o.xcdnw81.x1i0vuye.xh8yej3.x1tu34mt.xzloghq.x3nfvp2")
                    # Click the button
                    final_next_button.click()
                    time.sleep(10000)
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
    target_link = 'https://www.instagram.com/p/C3QPAwzIJQc/'
    
    # Initialize the database for temp_emails
    initialize_database()

    # Create a connection and cursor for insta_accs database
    insta_accs_connection, insta_accs_cursor = create_database('insta_accs.db')

    # Create a connection and cursor for temp_emails database
    temp_emails_connection, temp_emails_cursor = create_database('temp_emails.db')

    # Call the function to open Chrome and fill the form
    open_chrome_and_fill_form(target_link, temp_emails_cursor, 'insta_accs.db', domains)

    # Close connections
    insta_accs_connection.close()
    temp_emails_connection.close()
