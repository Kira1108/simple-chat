import openai
from simple_chat.config import get_config

from dataclasses import dataclass
from typing import TypedDict
import textwrap
from rich.console import Console
from rich.table import Table


config = get_config()
openai.api_key = config.openai_api_key


def print_log(message):
    table = Table(title="ChatLog",show_lines = True)

    table.add_column("Id", justify = 'center', style = 'white')
    table.add_column("Role", justify="right", style="cyan", no_wrap=True)
    table.add_column("Content", style="white")

    for i, row in enumerate(message):
        table.add_row(str(i + 1), row['role'].title(), row['content'])

    console = Console()
    console.print(table)

class MessageObject(TypedDict):
    role: str
    content: str

@dataclass
class Role:
    """A role object create chatting content according to openai API"""
    role:str
    def __call__(self, content:str) -> MessageObject:
        return {'role':self.role, 'content':content}

class Chat:
    
    """The Chat class provide functionalities added to openai API,
    which offers a set of chatting friendly interface as if you are using chatGPT.
    """

    def __init__(self, model = "gpt-3.5-turbo", verbose = True, print_role = False, print_width = 90):
        self.model = model
        self.message = []
        self.eager = False
        self.verbose = verbose
        self.print_role = print_role
        self.print_width = print_width

    @classmethod
    def gpt4(cls):
        return cls(model = "gpt-4")
    
    @classmethod
    def gpt35(cls):
        return cls(model = "gpt-3.5-turbo")

    def role_chat(self, role, content):
        # generate chatting message object
        msgobj = role(content)
        
        # append chatting message object to context
        self.message.append(msgobj)
        
        # execute the content if eager mode is on
        if self.eager:
            self.openai_request()

    def go(self):
        """Set chatting mode on"""
        self.eager = True

    def system(self, content):
        """A system content passed to bot"""
        return self.role_chat(Role("system"), content)

    def assistant(self, content):
        """An assistant content passed to bot"""
        return self.role_chat(Role("assistant"), content)

    def user(self, content):
        """A user content passed to bot"""
        return self.role_chat(Role("user"), content)

    def prune(self, indx:int):
        """delete a message given by id"""
        del self.message[indx - 1]

    def prune_range(self, start:int, end:int):
        """delete a range of index given by id"""
        del self.message[start - 1: end - 1]

    def prune_indices(self, indices):
        """delete a list of index given by id"""
        self.message = [msg for i, msg in enumerate(self.message) if i+1 not in indices]

    def __call__(self, content):
        """A user content passed to bot"""
        return self.user(content)

    def openai_request(self):
        """Make openai api call, all the chatting content should be passed into messages parameter,
        print out openai response content and append it to chat message list
        """
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.message
        )
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']

        if self.verbose:
            if self.print_role:
                print(f"{role}:\n")

            self._print_wrapped(content)

        self.message.append({'role':role,'content':content})

    def _print_wrapped(self, content):
        wrapped = textwrap.wrap(
                content, 
                width = self.print_width, 
                expand_tabs = False, 
                replace_whitespace=False, 
                break_long_words = False, 
                drop_whitespace=False, 
                break_on_hyphens=False, 
                tabsize = 4)
        print("".join(wrapped))

    def show(self):
        print_log(self.message)