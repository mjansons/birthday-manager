# birthdays

birthday manager

Features:

    Adding Birthdays:

Implement a function to add birthdays, including the person's name and birthdate.
Store this information in a file or a database.

    Birthday Notification:

Use a loop to check for upcoming birthdays.
Send a notification or display a message for birthdays that are approaching.

    AI-Generated Wishes:

Utilize a language model (like GPT-3, if available) to generate personalized birthday wishes.
Implement a function that takes the person's name and generates a unique and friendly birthday message.

    Email or Message Sending:

Use an email library or an API to send automated birthday wishes.
Incorporate the AI-generated text into the message body.

    Exception Handling:

Implement exception handling for cases where the email/message sending fails, ensuring a graceful response or retry mechanism.

    Help/Usage Information:

Provide a brief description of the app and how to use it.
Use a -h or --help argument to display this information.
could use ARGPARSE library for this one

    Search and find List Information about a certain person

    Send Wishes Manually:

    add/remove a contact

    adjust contact details

    maybe I could have another file with "message history"? or congratulated history.

    I wonder could I automate the congratulation process, by pre-approving messages? lol..
    Maybe there could be some sort of auto-congratulator mode..

    there is also a way to run the program once a day

    # so a congratulation history file in no particular order perhaps?
    # a settings file for autolaunch and time it was last launched? and where I would store my api key?

...

the message sending can happen in telegram, email, sms or whatsapp.

so what would be the flow?

I suppose there could also be like a setting file that would contain the time it was last launched and if the auto mode is on.

when I launch the program I want i want it to print hi and who's birthday it is today.



should I add stuff in the file only in lowercase? 

https://elevenlabs.io/sign-up

need to get user's name
need to remember to catch all the errors for failed API call and failed e-mail sending.

need to come back to format the long ass f strings in all pages
need to remeber to create logic for making a history file
need to remember to change every year status congratulated to False


How to make sure not to break auto mode when someone's email is not valid? (can't receive e-mails)
what if my e-mail is invalid? Auto mode should work only as long as API works a


had to update my certificates for mac:
/Applications/Python\ 3.12/Install\ Certificates.command

