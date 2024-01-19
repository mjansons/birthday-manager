# Birthday Manager (Python Command Line Program)

This Python project helps you manage and automate birthday congratulations for your contacts.

## Features
- **Generate congratulation e-mail with AI**, taking into account:
    - Name
    - Age
    - Previous congratulation messages
    - Any additional information provided
    - Ability to re-generate messages based on your suggestions
- **Auto-congratulation mode**
    - AI generates semi-formal messages unless about section indicates otherwise
- **Manually generate congratulation e-mail**
    - Create your own subject
    - Conduct a custom multi-line e-mail message
- **View all contacts**
- **Search and Edit specific contact details**
    - Name
    - Email
    - About
- **View sent message history**
    - Contact
    - Date and time
    - Message
- **View failed senders**
- **Wipe all files**
- **Error handling, flagging, yearly data re-set**

## Prerequisites
- Python 3.12
- Gmail account

### Steps
1. Generate your own OpenAI API key from: `https://platform.openai.com/api-keys`
2. Generate your Gmail app password:
    - Go to your Google Account.
    - Select Security.
    - Under "Signing in to Google," select 2-Step Verification.
    - At the bottom of the page, select App passwords.
    - Generate one and use it as MY_EMAIL_PASS.
3. Create your own `.env` file and populate it with the following values:
    ```
    MY_NAME=John Doe
    MY_EMAIL=youremail@gmail.com
    MY_EMAIL_PASS=jkdf dsas rtee vfgg
    OPENAI_API_KEY=fd-1234JNKdfgUTadf4QSJKDFFgfSARLEjnjfhgddsg45
    ```

## Installing
1. Install the required dependencies:
    ```bash
    pip install openai
    pip install python-dotenv
    pip install validator-collection
    ```

## Usage
To run the program, execute the following command in your terminal:
```bash
python3 main.py
```
