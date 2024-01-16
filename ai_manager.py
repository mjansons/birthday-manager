from dotenv import load_dotenv
import os
from openai import OpenAI, AuthenticationError, RateLimitError
from dataclasses import dataclass, field
from data_manager import read_csv, turning_years
load_dotenv()
MY_NAME = api_key=os.environ["MY_NAME"]

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],)

chat_history= [{"role": "system", "content": f"Instructions for the chatbot" }]


class WriteManual(Exception):
    pass

@dataclass
class MessageMaker():
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
                "content": (
                    f"You are a constructor of a birthday congratulation email's body"
                    f"for my contact {self.contact[0]['name']}. "
                    f"1. The message should start with Dear [person's name]. "
                    f"2. It should be minimum 2 and max 4 sentences, unless I tell you otherwise. "
                    f"3. It should end with Warm Wishes,{MY_NAME} at the bottom of the email, as email should. "
                    f"But don't sign it twice. Make sure there is only one signature.  "
                    f"Never use any placeholders, for signatures, age or anything, if info is missing. Take a general approach.  "
                    f"4. It has to take into account my notes about the contact: \"{self.contact[0]['about']}\". "
                    f"5. It has to be unique. Here are some past messages I've sent: {self.users_past_messages}"
                    f"6. If I didn't indicate that it's a close friend or family member, treat it quite formally "
                    f"and avoid references to any past experiences or feelings and avoid mentioning our friendship "
                    f"or the person's characteristics or anything we potentially could have done together"
                    f"7. It has to be quite general."
                    f"8. Avoid mentioning any past experiences or memories or my relationship to the person."
                    f"9. Congratulation should start with something similar to"
                    f" congratulations on your {turning_years(self.contact)} birthday!"
                )
            },
        ]


    def set_users_past_messages(self) -> list:
        if self.global_history:
            self.users_past_messages = [person["message"] for person in self.global_history if "uid" in person and person["uid"] == self.contact[0]["uid"]]
        else:
            self.users_past_messages = ["There have not been any previous congratulations"]


    def get_prompt(self) -> str:
        try:
            self.chat_history.append({"role": "user", "content": "Please take a deep breath, relax, and write me that letter."})
            api_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.chat_history)
            api_message = api_response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": api_message})
            return api_message
        except AuthenticationError:
            print("Authentication Error: Please check your OpenAI API key.")
            raise WriteManual
        except RateLimitError:
            print("Rate Limit Error: You've exceeded your token usage limit.")
            raise WriteManual
    

    def re_prompt(self, corrections) -> str:
        try:
            self.chat_history.append({"role": "user", "content": f"Conduct another variation. {corrections}"})
            api_response = client.chat.completions.create(model="gpt-3.5-turbo", messages=self.chat_history)
            api_message = api_response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": api_message})
            return api_message
        except AuthenticationError:
            raise WriteManual("Authentication Error: Please check your OpenAI API key.")
        except RateLimitError:
            raise WriteManual("Rate Limit Error: You've exceeded your token usage limit.")
            

if __name__ == "__main__":
    contact = [    
        {
            'uid': '170466393555551',
            'name': 'Peteris',
            'birthday': '1954.11.11',
            'email': 'peteris@gmail.com',
            'about': 'smth',
            'congratulated': "True"
        }
    ]

    try:
        global_history = read_csv("history.csv")
    except ValueError:
        global_history = []

    bot = MessageMaker(contact, global_history)
    answer = bot.get_prompt()
    print(answer)





# ChatCompletion(id='chatcmpl-8LsbTcj49kGSFvGanYjFr1OMxrIiF',
#                choices=[Choice(finish_reason='stop', index=0, message=ChatCompletionMessage(content='This is a test.', role='assistant', function_call=None, tool_calls=None))],
#                created=1700225475,
#                model='gpt-3.5-turbo-0613',
#                object='chat.completion',
#                system_fingerprint=None,
#                usage=CompletionUsage(completion_tokens=5, prompt_tokens=12, total_tokens=17))