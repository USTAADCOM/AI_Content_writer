"""
noun generator module will take the string and return the nouns list in string.
"""
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai.api_key  = os.getenv('OPENAI_API_KEY')
def make_prompt()-> str:
    """
    make_prompt take code as input and retirn the prompt with the given
    pargraph.

    Parameters
    ----------
    paragraph: str
        string text to find the nouns.
    action: str
        type of action.
    Return
    ------
    prompt: str
        prompt to find the nouns from given paragraph.
    """
    file_path = "./prompt/blog_or_essay_prompt.txt"
    with open(file_path, "r", encoding = "utf8") as file:
        prompt = file.read()
    return prompt
def generate_blog(topic = " ",
                  content_type = " ", link = " ", tone = " ",
                  length = 500):
    """
    code_debug method take topic type link tone length as input and return the output
    according to the prompt.

    Parameters
    ----------
    topic: str
        topic of essay or blog.
    type: str
        essay or blog.
    link: str
        link of user sources.
    tone: str
        essay or blog tone.
    Return
    ------
        return generated blog or essay.
    """
    full_text =  ""
    length = str(length)
    prompt = make_prompt()
    prompt = prompt.format(TOPIC = topic, WORDS = length,
                           TYPE = content_type,
                           LINKS = link
                           )
    tone_prompt = f"tone should be {tone}"
    messages=[
        {
        "role": "system",
        "content": prompt
        },
        {
        "role": "user",
        "content": tone_prompt
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages,
        temperature = 1,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        stream = True,
        stop = None
    )
    try:
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta'].get("content")
            full_text = full_text + chunk_message
            yield full_text
    except Exception as error:
        print("OPenAI reponse (streaming) error" + str(error))
        return 503
        
