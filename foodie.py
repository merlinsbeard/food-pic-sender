import praw
import re

user_agent = "Give me Food"
r = praw.Reddit(user_agent=user_agent)
subs = "baking"
submissions = r.get_subreddit(subs).get_hot()
listings = [x for x in submissions]

pattern ="((http(s?):\/\/)?((i\.)?)imgur\.com\/)((?:[a]\/)?)([a-zA-Z0-9]{5,8})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)"

urls = []
for count, x in enumerate(listings):
    output = count, x.url
    result = re.search(pattern, x.url)
    if result:
        urls.append(x.url)
        print(x.url)
    


