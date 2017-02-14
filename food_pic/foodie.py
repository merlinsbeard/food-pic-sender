import praw
import re
from string import Template
import random
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os
import sys, getopt
import argparse
from envparse import env
from os.path import basename

env.read_envfile()

user_agent = env('USER_AGENT')
client_id=env('CLIENT_ID')
client_secret=env('CLIENT_SECRET')
r = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent)

def get_urls(subreddit):
    """
    Returns a list of urls depending on what subreddit
    """
    submissions = r.subreddit(subreddit).hot(limit=100)

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

def send_html_mail(you, subject, food_page):

    #me = os.environ['food_email']
    me = env('FOOD_EMAIL')
    me_pass = env('FOOD_EMAIL_PASS')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    with open(food_page,'r')as f:
        html_file = f.read()
        a = MIMEBase('application', 'octet-stream')
        a.set_payload(html_file)
        #encoders.encode_base64(a)
        a.add_header('Content-Disposition','attachment',filename=food_page)
        
        msg.attach(a)

    html = html_file
    text = "HOLA"
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    #msg.attach(part1)
    msg.attach(part2)


    s = smtplib.SMTP("smtp.zoho.com",587)
    s.ehlo()
    s.starttls()
    s.login(me, me_pass)

    s.sendmail(me, you, msg.as_string())
    s.close()

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

    if not os.path.exists("pages"):
        os.makedirs("pages")
    pages = os.listdir("pages")
    page_num = len(pages)+ 1
    filename = "pages/{}.html".format(page_num)
    url = "http://caffeine.dailywarrior.ph/food"
    previous_link = "{}/{}.html".format(url, page_num -1)
    page_url = "{}/{}.html".format(url, page_num)

    #sounds = os.listdir("sounds")
    #music = "sounds/{}.mp3".format(len(sounds))
    music = "sounds/"

    d = {
        'images': "\n".join(images),
        'next' : "",
        'previous': previous_link,
        'page_url': page_url,
        'music': music,
        }
    result = src.substitute(d)
    filein.close()
    result = str(result)

    # Creates a new file and putting the image links in new file
    #filename = "{}.html".format(datetime.now().__str__())
    #filename = "pages/{}".format(filename)
    print("Creating New page {}.html".format(page_num))
    with open(filename,'w') as f:
        f.write(result)

def foodie(email, subreddit):
    links1 = get_urls(subreddit)
    links = get_img_links(links1)
    save_html_file(links)
    pages = os.listdir("pages")
    page_num = len(pages)
    filename = "pages/{}.html".format(page_num)
    send_html_mail(email, "[FOOD] From your friendly neighbor", filename)


def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("email", type=str, help="Email")
    parser.add_argument("subreddit",type=str, help="subreddits")

    args = parser.parse_args()
    email = args.email
    # subreddit = baking+FoodPorn
    subreddit = args.subreddit

    print("HEYO {}".format(email))
    links1 = get_urls(subreddit)
    links = get_img_links(links1)
    print("Now Creating HTML file")
    save_html_file(links)
    pages = os.listdir("pages")
    page_num = len(pages)
    filename = "pages/{}.html".format(page_num)
    send_html_mail(email, "[FOOD] From your friendly neighbor", filename)
    print("SUCCESS!")



if __name__ == '__main__':
    main()
    #food_play(sys.argv[1:])
