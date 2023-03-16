# Simple Chat


An OpenAI chat wrapper, simplify chatting with python.
> All your chatting history is passed into the next request.    
> No optimization for maintaining chat history.      
> You should pay special attention to tokens counts.    

## 1. Export openai api key
```bash
export OPENAI_API_KEY="your_openai_api_key"
```
or
```python
from simple_chat import set_openai_api_key
set_openai_api_key("your_openai_api_key")
```

## 2. Chat with python
start chatting.
```python
from simple_chat import Chat
chat = Chat()
chat.go()
chat("Hello there")
```

chat after wram up.
```python
chat = Chat()

#-------------Warm up Phase--------------
chat.system("""You are a english teacher, you correct your student's english. Point out every misktasks that they make. and correct them.""")

chat.user("She are a woman")

chat.assistant(
"""The correct sentence should be: "She is a woman."

The verb "are" is incorrect because it is the plural form of "is." "She" is a singular subject, so it requires a singular verb "is.""")
#-------------Chatting Phase--------------
chat.go()

chat("I eat an apple last night")


```
Output:
```
>>> The correct sentence should be: "I ate an apple last night."

The past tense of the verb "eat" is "ate," so the sentence should use "ate" instead of "eat." Also, since the time reference is in the past ("last night"), the verb should be in the past tense. Finally, "an" is incorrect because "apple" starts with a vowel sound, but "a" should be used because "apple" is not a word that starts with a vowel letter, but rather with the consonant "a."
```


## 3. Openai Chat Parameters
In case you want more flexible control over API parameters.
```python
from simple_chat import ChatParams, Chat
# you can pass any parameters of chat api to ChatParams, except for `messages`
# because messages is dynamically build whild chatting.
params = ChatParams(model = "text-davinci-003", temperature = 1, stream = False)

# pass params to Chat object
chat = Chat(params = params)

```

## 4. View Chat History
A simple table of chat history.
```
chat.show()
```