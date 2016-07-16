import praw
import re

user_agent = "Give me Food"
r = praw.Reddit(user_agent=user_agent)

def get_urls(subreddit):
    submissions = r.get_subreddit(subreddit).get_hot()
    return [x for x in submissions]

def is_image(url):
    patterns = [
        "((http(s?):\/\/)?((i\.)?)redd\.it\/)([a-zA-Z0-9]{5,13})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)",
        "((http(s?):\/\/)?((i\.)?)imgur\.com\/)((?:[a]\/)?)([a-zA-Z0-9]{5,8})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)",
        ]
    for pattern in patterns:
        result = re.search(pattern, url)
        if result:
            return True
    return False

def get_img_links(links):
    img_links = []

    for link in links:
        if is_image(link.url):
           img_links.append(link)
    return img_links

def get_imgur_links(links):
    
    pattern ="((http(s?):\/\/)?((i\.)?)imgur\.com\/)((?:[a]\/)?)([a-zA-Z0-9]{5,8})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)"

    imgur_links = []
    for count, x in enumerate(links):
        output = count, x.url
        result = re.search(pattern, x.url)
        if result:
            imgur_links.append(x.url)
    return imgur_links 

#def get_link_details(link):
#    detail = r.get_submission(submission_id = link.id)
#    details = {
#        'subreddit': detail.subreddit.__str__(),
#        'permalink': detail.permalink,
#        'link': detail.url
#        }
#    return details
   

subreddits = "baking+FoodPorn"

links1=get_urls(subreddits)
links = get_img_links(links1)
#a = [x for x in  get_imgur_links(links)]
print("DETAILS")
for link in links:
    print("""
        ID: {},
        Permalink: {},
        Link: {},
        Subreddit: {}
        Score:{},
        """.format(link.id, link.permalink,link.url,link.subreddit,link.score)
        )

