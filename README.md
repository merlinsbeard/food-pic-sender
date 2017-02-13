
Reddit Picture Retriever
==============

A script that views the any subreddit daily and send the top 5 to selected user.

Usage:
Setting up

```
$ pip install -r requirements.txt
```
Create the pages folder. This will containe the generated html page
```
$ mkdir pages
```
Environment variables are located at .env file
Copy the file .sample_env to .env
```
$ cp .sample_env .env
```

Open and edit .env file put your own values
```
$ vim .env
```


FOOD_EMAIL=email address
FOOD_EMAIL_PASS=email address password
CLIENT_ID=[ generated from reddit](https://www.reddit.com/prefs/apps)
CLIENT_SECRET=[generated from reddit]https://www.reddit.com/prefs/apps)

To run the file
python foodie.py email subreddit

```
$ python foodie.py hallo@gmail.com baking+FoodPorn
```
