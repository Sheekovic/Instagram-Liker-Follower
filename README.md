
# Instagram Account Creator

This script automates the process of creating Instagram accounts for various purposes. It uses Selenium for web automation and SQLite for managing temporary email addresses and account details.

## Features

- **Automated Account Creation**: The script navigates to the specified Instagram link, fills out the registration form, and creates Instagram accounts automatically.
- **Temporary Email Generation**: Temporary email addresses are generated and used for account registration to avoid spam and simplify the process.
- **Randomized Data Generation**: Random usernames, passwords, and other details are generated to make the accounts more realistic.
- **Headless Mode**: The script can be run in headless mode to operate without a visible browser window.
- **User-Agent Rotation**: User agents are rotated to mimic different devices and browsers, enhancing anonymity and preventing detection.

## Prerequisites

- Python 3.x
- Chrome WebDriver
- Required Python packages (install via `pip`):
  ```
  pip install -r requirements.txt
  ```

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/Sheekovic/Instagram-Liker-Follower.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:

   ```bash
   python main.py
   ```

4. Follow the instructions in the console prompts.

## Configuration

- you can modify `domains` in `main.py` to include your preferred email domains for temporary email generation.
- Add more user agents to the `user_agents` list in `main.py` for user agent rotation.
- Adjust timeouts and delays in the script as needed.

## Disclaimer

This script is for educational and testing purposes only. Use it responsibly and in compliance with Instagram's terms of service. The developer is not responsible for any misuse or damage caused by this script.

## License

[MIT License](LICENSE)
