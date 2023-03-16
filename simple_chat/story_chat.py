from .base import Chat

class StoryChat(Chat):
    
    def __init__(self, 
                story_scope = "reveals realities of the society",
                story_style = "miserable, sad",
                story_purpose = 'high-converting',
                topic = "Hard working and Luckiness",
                *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = [
            
            {'role':'system', 
            'content':"""
                You are a story teller, you write stories that {story_scope},
                You write stories in {story_style} style. You write {story_purpose} stories.
                """.format(story_scope = story_scope, story_style = story_style, story_purpose = story_purpose)
            },
            
            {'role':'user', 
            'content':"""
                I want you to act as a storyteller, you have three tasks.
                For the first task, I wil provide you with a {{topic}} you are going to expand your story around this {{topic}}.
                For the second task, Your story has a main character, male, hard working, but his life is very rough.
                For the third task, Your story should have a complicate story line, ends in miserable or sadness.
                
                topic="{topic}"
                
                Write in Chinese, An adult short story, 5000 Chinese characters.
                """.format(topic = topic)}
        ]        