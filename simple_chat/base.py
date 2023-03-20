import openai
from simple_chat.config import get_config

from dataclasses import dataclass
from typing import TypedDict
import textwrap
from rich.console import Console
from rich.table import Table
from simple_chat.params import ChatParams
from simple_chat.printer import HtmlPrinter,is_notebook


config = get_config()
openai.api_key = config.openai_api_key

def set_openai_api_key(api_key:str):
    openai.api_key = api_key

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

    def __init__(self, 
                 params:ChatParams = None, 
                 verbose:bool = True, 
                 print_role:bool = False,
                 printer = None):
        
        self.params = params if params else ChatParams.gpt3()
        self.message = []
        self.eager = False
        self.verbose = verbose
        self.print_role = print_role

        if printer:
            self.printer = printer
        else:
            self.printer = HtmlPrinter() if is_notebook() else print

    @classmethod
    def gpt4(cls, **kwargs):
        if 'model' in kwargs:
            del kwargs['model']
        params = ChatParams.gpt4(**kwargs)
        return cls(params)
    
    @classmethod
    def gpt3(cls, **kwargs):
        if 'model' in kwargs:
            del kwargs['model']
        params = ChatParams.gpt3(**kwargs)
        return cls(params)

    def flex(self):
        self.set_param('temperature', 1.5)
        return self
    
    def freedom(self):
        self.set_param('temperature', 2)
        return self
    
    def set_param(self, param, value):
        setattr(self.params, param, value)

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
            messages=self.message,
            **self.params.dict()
        )
        role = response['choices'][0]['message']['role']
        content = response['choices'][0]['message']['content']

        if self.verbose:
            if self.print_role:
                print(f"{role}:\n")

            self.printer(content)

        self.message.append({'role':role,'content':content})

    def show(self):
        print_log(self.message)