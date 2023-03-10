import os
import openai
from dotenv import load_dotenv
import tiktoken

load_dotenv()

openai.api_key = os.environ["OPENAPI_KEY"]

# def get_summary(text):
#     response = openai.Completion.create(
#         model="text-davinci-003", #gpt-3.5-turbo
#         prompt='''Can you give me a summary of the text below? I would like
#                 as much detail as possible: ''' + text + ''''\n\nTl;dr''',
#         # rich and lengthy summary of this text two or three paragraphs long:
#         temperature=0.15,
#         max_tokens=500, # find a dynamic way of optimizing for this
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=1
#     )
#     print(response)
#     return response.choices[0].text


# https://platform.openai.com/docs/guides/chat/introduction

prompt = '''
Stephanie Shore  [12:57 PM]
Hello friends! I'm a fractional CMO / Marketing Consultant based in Boston that's built some iconic brands (Zipcar, MOO and McBride Sisters, to name a few.) I'm comfortable managing strategy at 30k feet, and jumping into the trenches.
What I've learned: Read a quote from Jason Lemkin that really resonated: "Most CEOs do not have 15 minutes to do a 'quick call'. Most CEOs WILL read your email though if it looks like it will truly help their company. If it's one of their Top 5-10 problems to solve, right now. Make that email truly awesome and solve that problem. Instead of asking for a 'quick call.' See what happens."
How I can help: Happy to help the community in any way I can. I love making connections between talented people, especially those that also qualify as good humans. And of course, I welcome any leads for fractional CMO and marketing consulting work for b2c companies. (edited)
Sydney Reinhard  [10:06 AM]
Hello everyone! My name is Sydney and I am a college student from Madison, WI now helping with the social media management.
Something I've learned lately: Entrepreneurs are a group of people who are likely to own cats!
How I can help others: I would love to bring a new spark and sense of creativity to content
Something that others might be able to help me with: A personal goal of mine this year is to learn how to invest some of my savings, so if anyone has any advice for starter investors, please send it my way! :)
Sherene Strausberg  [11:16 AM]
Hi everyone! So nice to meet you all. And thank you to @Laurel Carpenter for introducing me to this group!!
About Me:  I'm based in NY, and run my own company, 87th Street Creative, that creates animated marketing videos (like explainers, promos, commercials, ads) to help explain complex topics or if you have just have a product to sell or a story to tell. I create custom illustrations, and then animate them with music, VO and sound effects. However, I don't do any of the strategy or writing or placing it online. So, I'm always excited to connect with marketing strategists, writers, media marketers and web developers.
How I Can Help Others: I love introducing people to each other. I'm part of several networking groups and have a strong network of people I know, like and trust. Let me know who you're looking to meet, and hopefully I can make a solid introduction for you! Always happy to hop on a call and meet new people.
Something I Learned Recently: I'm in the middle of reading an amazing book called "Can I Recycle This?" And there's so much fascinating information in there, like glass is worth less on the commodities market than plastic, or bottle caps are best recycled by collecting them inside a can, or those red SOLO cups we all drank from at parties in college can never be recycled. So, BYOB next time you go drinking at a frat party! Or in this case BYOC - bring your own cup, and then reuse it! :rolling_on_the_floor_laughing:
Super excited to meet all of you and engage in this community. :tada:
Tea Korpi  [6:24 AM]
Hi all! I’m thrilled to take part in this community and meet you all! :tada:
I’m Tea, Product Marketing Manager at Supermetrics. I have a background in marketing management and last year I made a professional switch to product marketing. Currently, I plan, position, and strategize marketing for our data integration products.
1. Something I’ve learned lately. I’ve understood I can’t know everything about everything, the hard realization that there’s just too much happening all the time. Plus I’m still learning to unwind from work and not be reachable all the time.
8:35
2. How can I help you. I love to brainstorm ideas around marketing and communication, and I have pretty long experience in planning and marketing in growth SaaS companies. Plus my work revolves around marketing data and how to leverage it, so if this is something that interests you I’m happy to brainstorm about this as well.
3. Something that others might be able to help me with. If you have good book recommendations, feel free to suggest them. I’m always looking for new books to read/listen to. Plus I’m interested in marketing reporting use cases and cool things you might’ve done with your marketing data.
David Berkowitz  [9:34 AM]
There's a ton coming up in the community @channel, and we've got a new request. @Yarden Tadmor is wondering who's here from South Fl as he moved to Miami Beach and would love to organize something. We have the #local-florida channel (which maybe should be the local-south-fl channel... but we'll get there) so please join that and chime in if you're interested. Maybe that'll even be my excuse to get down there.
And for anyone who wants to host a Serial Marketers meetup, whether a First Wednesday or other kind of event, I will gladly promote it in Slack, newsletters, Meetup etc and even see if anyone wants to foot the bill. Be sure to browse the channels and see all the options that start with #local...
Donny Dye  [7:30 AM]
Good Morning everyone,
What a great group!
I am currently looking for a new opportunity, but in the recent past, I was the SVP of Marketing & Sales at a social advertising company, called Tiger Pistol. I also founded and manage a revenue strategies firm called Quota NYC. I lived in the Upper West Side, NYC, until last August when I moved outside of Cleveland.
Something I learned lately
I heard an increasingly valuable phrase "Make sure you know why the fence is there before you take it down".
I love this saying. It reminds me to respect the context.
How can I help others
My primary expertise is connecting sales and marketing through strategy. Please reach out with any questions on how the two can work together.
How others can help me
As I mentioned, I am looking for a new job. I have spent the last 20 years in Martech, Adtech, and SaaS sales. If you know of anyone worth having a conversation with in any of those types of companies, I would be incredibly appreciative of an introduction.
'''
new_prompt = prompt * 5

def get_summary_chatgpt(prompt):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[
                    {"role": "system", "content": "You are a Chatbot being used in Slack to summarize messages in the channel."},
                    {"role": "user", "content": "Please summarize the following messages with a rich level of detail: " + prompt},
                ]
            )
    #print(response)
    return response.choices[0].message['content']


#print(get_summary_chatgpt(prompt))

''' testing sandbox: using tiktoken to count token length'''

# encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
#
# #print(encoding.encode("tiktoken is great!"))
#
# #print(len(encoding.encode(prompt)))
#
# test_of_encoded_prompt = encoding.encode(prompt)
#
# max_token_length = 500
#
# print(test_of_encoded_prompt[:max_token_length])
# print(len(test_of_encoded_prompt[:max_token_length]))
#
# print(encoding.decode(test_of_encoded_prompt[:max_token_length]))

'''testing recursive function'''

def completion_request_handler(text, max_tokens):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    prompt_tokens = encoding.encode(text)
    if len(prompt_tokens) < max_tokens:
        return get_summary_chatgpt(text)
    else:
        return recursive_completion(prompt_tokens, max_tokens)


def recursive_completion(prompt_tokens, max_tokens):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-0301")
    while len(prompt_tokens) > 0:
        chunk = encoding.decode(prompt_tokens[:min(max_tokens, len(prompt_tokens))])
        print(get_summary_chatgpt(chunk))
        prompt_tokens = prompt_tokens[min(max_tokens, len(prompt_tokens)):len(prompt_tokens)]
        if len(prompt_tokens) > max_tokens:
            recursive_completion(prompt_tokens, max_tokens)
        else:
            return get_summary_chatgpt(encoding.decode(prompt_tokens))




# def num_tokens_from_string(string: str, encoding_name: str) -> int:
#     """Returns the number of tokens in a text string."""
#     encoding = tiktoken.get_encoding(encoding_name)
#     num_tokens = len(encoding.encode(string))
#     return num_tokens

#print(completion_request_handler(new_prompt, 3200))
#print(get_summary_chatgpt(prompt))

# import time
# import datetime as DT
#
# print(time.time())
#
# today = DT.date.today()
# week_ago = today - DT.timedelta(days=7)
# print(week_ago)
#
# print("unix_timestamp => ",
#       (time.mktime(week_ago.timetuple())))


slack_key = os.environ["SLACK_BOT_TOKEN"]

from slack_sdk import WebClient
client = WebClient(token=slack_key) #'xoxb-390481124449-4701642463253-dEkE6r7iw4GUvquayrqeBSKh')
derp = client.auth_test()
#derp = client.users_list()
outfile = open('resources/bot_user_id_GLBZ.txt', 'w')
outfile.write(str(derp))
outfile.close()

print(derp['bot_id'])