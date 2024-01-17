# Selenium Form Filler Script

## Overview

This Python script utilizes the Selenium WebDriver to automate interactions with a web page, specifically to fill out a registration form. The script opens a Chrome browser, navigates to a specified link, clicks on the like button, proceeds to the registration form, fills it with randomly generated data, and submits the form. The provided data (email, username, and password) is also stored in a SQLite database.

## Requirements

Before running the script, ensure you have the following dependencies installed:

- Python 3.x
- Selenium
- Faker
- ChromeDriver
- SQLite3

You can install the required Python packages using:

```bash
pip install selenium faker
```

Make sure to download and install [ChromeDriver](https://sites.google.com/chromium.org/driver/) and add its location to your system's PATH.

## Usage

1. Clone the repository or download the script.
2. Install the required dependencies.
3. Replace the placeholder link in the `target_link` variable with the desired webpage URL.
4. Run the script using:

    ```bash
    python script_name.py
    ```

## Configuration

- The script is configured to open Chrome in headless mode by default. If you want to run the browser with a visible window, uncomment the appropriate line in the `open_chrome_and_fill_form` function.

- Adjust the sleep times in the script according to the page load times and your preferences.

## Database

The script creates a SQLite database named `fake_data.db` and a table `fake_data` to store the generated information.

## Disclaimer

Use this script responsibly and in compliance with the terms of service of the websites you are interacting with. Automated interactions may violate the terms of service of certain websites. Ensure that you have the right to automate interactions with the provided link.

Feel free to customize the script according to your needs. For more information on Selenium, refer to the [Selenium documentation](https://www.selenium.dev/documentation/en/).

Happy automating!
