import praw
import re
from string import Template
import random
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

user_agent = "Give me Food"
r = praw.Reddit(user_agent=user_agent)

def get_urls(subreddit):
    """
    Returns a list of urls depending on what subreddit
    """
    submissions = r.get_subreddit(subreddit).get_hot(limit=100)

    links = [x for x in submissions]
    random.shuffle(links)
    return links
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

def add_jpg(url):
    patterns = [
    "((http(s?):\/\/)?((i\.)?)imgur\.com\/)([a-zA-Z0-9]{5,8})"
    ]

    for pattern in patterns:
        result = re.search(pattern, url)
        if result:
            url = result.group(0) + ".jpg"
        return url

def get_img_links(links):
    """
    Returns the image link of a reddit link
    """
    img_links = []
    score = 50
    image_count = 10
    for link in links:
        if len(img_links) == image_count:
            return img_links
        elif is_image(link.url) and link.score > score:
            link.url = add_jpg(link.url)
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




def send_html_mail(me, you,subject):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    with open("food2.html",'r')as f:
        html_file = f.read()
    html = html_file
    text = "HOLA"
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)


    s = smtplib.SMTP("smtp.zoho.com",587)
    s.ehlo()
    s.starttls()
    s.login(me,os.environ['email_pass'])

    s.sendmail(me, you, msg.as_string())
    s.quit


def show_prints(links):
    """
    Used for prieving the values
    """
    print("DETAILS")
    count = 0
    for link in links:


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
        count += 1

def save_html_file(links):
    """
    Opens food_template.html and writes the <img> tag with links to images.
    Creates a new file based on food_template.html
    """
    images = []
    for link in links:
        images.append(
            "<div class='grid-item'><img src='{}' alt='' /></div>".format(link.url)
        )
    # Opens food_template.html containing the template of html file
    filein = open("food_template.html",'r')
    src = Template(filein.read())

    pages = os.listdir("pages")
    filename = "pages/{}.html".format(str(len(pages)+1))
    
    d = {
        'images': "\n".join(images),
        'next' : "",
        'previous': "",
        }
    result = src.substitute(d)
    filein.close()
    result = str(result)

    # Creates a new file and putting the image links in new file
    #filename = "{}.html".format(datetime.now().__str__())
    #filename = "pages/{}".format(filename)
    print("Creating New page {}.html".format(len(pages)+ 1))
    with open(filename,'w') as f:
        f.write(result)


subreddits = "baking+FoodPorn"

links1=get_urls(subreddits)
links = get_img_links(links1)

print("Now Creating HTML file")
save_html_file(links)
