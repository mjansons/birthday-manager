"""this file manages openai api calls"""

import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError
from dataclasses import dataclass, field
from data_manager import turning_years

load_dotenv()

MY_NAME = os.environ["MY_NAME"]

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

chat_history = [{"role": "system", "content": f"Instructions for the chatbot"}]


class WriteManual(Exception):
    pass


@dataclass
class MessageMaker:
    contact: list[dict]
    global_history: list[dict]

    users_past_messages: list = field(init=False)
    chat_history: list = field(init=False)
    first_instruction: list[dict] = field(init=False)

    def __post_init__(self) -> None:
        self.set_users_past_messages()
        self.chat_history = [
            {
                "role": "system",
                "content": f"""
                    You are a constructor of a birthday congratulation email's body
                    for my contact {self.contact[0]['name']}. 
                    1. The message should start with Dear [person's name]. 
                    2. It should be minimum 2 and max 4 sentences, 
                    unless I tell you otherwise. 
                    3. It should end with Warm Wishes,{MY_NAME} at the bottom of the email, 
                    as email should. But don't sign it twice. 
                    Make sure there is only one signature.  
                    Never use any placeholders, for signatures, age or anything, 
                    if info is missing. Take a general approach.  
                    4. It has to take into account my notes about the 
                    contact: "{self.contact[0]['about']}". 
                    5. It has to be unique. Here are some past messages 
                    I've sent: {self.users_past_messages}
                    6. If I didn't indicate that it's a close friend or family member, 
                    treat it quite formally and avoid references to any past 
                    experiences or feelings and avoid mentioning our friendship 
                    or the person's characteristics or anything we potentially 
                    could have done together
                    7. It has to be quite general.
                    8. Avoid mentioning any past experiences or memories 
                    or my relationship to the person.
                    9. Congratulation should start with something similar to
                    congratulations on your {turning_years(self.contact)} birthday!
                    10. If it's a family member, indicate that I appreciate having them
                    in my life.
                """,
            },
        ]

    def set_users_past_messages(self) -> list:
        if self.global_history:
            self.users_past_messages = [
                person["message"]
                for person in self.global_history
                if "uid" in person and person["uid"] == self.contact[0]["uid"]
            ]
        else:
            self.users_past_messages = [
                "There have not been any previous congratulations"
            ]

    def get_prompt(self) -> str:
        try:
            self.chat_history.append(
                {
                    "role": "user",
                    "content": "Please take a deep breath, relax, and write me that letter.",
                }
            )
            api_response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=self.chat_history
            )
            api_message = api_response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": api_message})
            return api_message
        except AuthenticationError:
            print("\nAuthentication Error: Please check your OpenAI API key.")
            raise WriteManual
        except RateLimitError:
            print("\nRate Limit Error: You've exceeded your token usage limit.")
            raise WriteManual
        except APIConnectionError:
            print("\nOpenAI API request failed to connect.")
            raise WriteManual

    def re_prompt(self, corrections) -> str:
        try:
            self.chat_history.append(
                {"role": "user", "content": f"Conduct another variation. {corrections}"}
            )
            api_response = client.chat.completions.create(
                model="gpt-3.5-turbo", messages=self.chat_history
            )
            api_message = api_response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": api_message})
            return api_message
        except AuthenticationError:
            print("\nAuthentication Error: Please check your OpenAI API key.")
            raise WriteManual
        except RateLimitError:
            print("\nRate Limit Error: You've exceeded your token usage limit.")
            raise WriteManual
        except APIConnectionError:
            print("\nOpenAI API request failed to connect.")
            raise WriteManual
