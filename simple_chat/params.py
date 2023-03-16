
from dataclasses import dataclass
from typing import Union, List
import json

@dataclass
class ChatParams:
    
    """OpenAI GPT chat API parmaeters

    You should always check the OPENAI API documentation for the latest parameters.
    here is the link: https://platform.openai.com/docs/api-reference/chat

    Parameters:
    ----------
        model: str, model endpoint to use, refer to https://platform.openai.com/docs/models/model-endpoint-compatibility
        temperature: float, between 0 and 2, higher value means more random
        top_p: float, between 0 and 1, higher value means more random
        n: int, number of samples to return
        stream: bool, whether to stream the response
        stop: Union[List, str], list of tokens to stop on, or a single token
        max_tokens: int, maximum number of tokens to return
        presence_penalty: float, Number between -2.0 and 2.0. larger value means more random
            Positive values penalize new tokens based on whether they appear in the text so far, 
            increasing the model's likelihood to talk about new topics.
        frequency_penalty: float, Number between -2.0 and 2.0. larger value means more random
            Positive values penalize new tokens based on their existing frequency in the text so far, 
            decreasing the model's likelihood to repeat the same line verbatim.
        logit_bias: dict, dictionary of token to bias to apply to logit scores before sampling
                    Modify the likelihood of specified tokens appearing in the completion.
        user: str, user id to associate with the request
    
    Note:
    ----------
        Except the above, you have to pass a messages list
        messages: list, list of dict with keys being role and value been content
        It the most important thing, and not abstracted as a parameter here.

    Usage:
    ----------
        # create a chat params object
        params = ChatParams.gpt4()
        params = ChatParams.gpt3()
        params = ChatParams(model = "text-davinci-003", temperature = 1, stream = False)

        # convert to dictionary of json
        params.dict()
        params.json()

    
    """

    model:str=  'gpt-3.5-turbo'
    temperature:float = 1
    top_p:float = 1
    n:int = 1
    stream:bool = False
    stop:Union[List, str] = None
    max_tokens:int = None
    presence_penalty:float = 0
    frequency_penalty:float = 0
    logit_bias:dict = None
    user:str = None

    @classmethod
    def gpt4(cls, *args, **kwargs):
        return cls(model = "gpt-4", *args, **kwargs)
    
    @classmethod
    def gpt3(cls, *args, **kwargs):
        return cls(model = "gpt-3.5-turbo", *args, **kwargs)

    def dict(self):
        param_dict = {
            'model': self.model,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'n': self.n,
            'stream': self.stream,
            'stop': self.stop,
            'max_tokens': self.max_tokens,
            'presence_penalty': self.presence_penalty,
            'frequency_penalty': self.frequency_penalty,
            'logit_bias': self.logit_bias,
            'user': self.user
        }
        return {k:v for k,v in param_dict.items() if v is not None}
    
    def json(self):
        return json.dumps(self.dict())
    

if __name__ == "__main__":
    params = ChatParams.gpt4()
    print(params.dict())
    print(params.json())

    params = ChatParams.gpt3()
    print(params.dict())
    print(params.json())
