import praw
import re

user_agent = "Give me Food"
r = praw.Reddit(user_agent=user_agent)

def get_urls(subreddit):
    """
    Returns a list of urls depending on what subreddit
    """
    submissions = r.get_subreddit(subreddit).get_hot(limit=100)
    return [x for x in submissions]

def is_image(url):
    """
    Returns True if link is an imgur or reddit link
    """
    patterns = [
        "((http(s?):\/\/)?((i\.)?)redd\.it\/)([a-zA-Z0-9]{5,13})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)",
        "((http(s?):\/\/)?((i\.)?)imgur\.com\/)([a-zA-Z0-9]{5,8})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)",
        #"((http(s?):\/\/)?((i\.)?)imgur\.com\/)((?:[a]\/)?)([a-zA-Z0-9]{5,8})((\.jpg|\.gif|\.gifv|\.png)?)(?:[^a-zA-Z0-9]|$)",
        ]
    for pattern in patterns:
        result = re.search(pattern, url)
        if result:
            return True
    return False

def get_img_links(links):
    """
    Returns the image link of a reddit link
    """
    img_links = []
    score = 200

    for link in links:
        if len(img_links) == 5:
            return img_links
        elif is_image(link.url) and link.score > score :
           img_links.append(link)

    return img_links

def is_imgur_album(imgur_link):
    """
    Checks if a imgur url is an album
    """
    if imgur_link:
        return False
    return True

def imgur_album_images(album_id):

    return [x.url for x in get_album_images(album_id)]


def top_4():
    pass


subreddits = "baking+FoodPorn"

links1=get_urls(subreddits)
links = get_img_links(links1)

print("DETAILS")
count = 0
for link in links:
    count += 1
    print("""
        #: {},
        ID: {},
        Permalink: {},
        Link: {},
        Subreddit: {}
        Score:{},
        Title: {},
        """.format(
            count,
            link.id, link.permalink,
            link.url,link.subreddit,
            link.score, link.title,
                )
        )
