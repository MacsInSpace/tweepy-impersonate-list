import time
import tweepy
import csv
import traceback

auth = tweepy.OAuthHandler("", "")
auth.set_access_token("",
                      "")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

user = "me"
target = "realdonalttrump"


twitterlist = (target)+ "_friends"
mode = "private"
path = "/tmp/" +(target)+ "_friends.csv"


def get_friends(user_name):
    """
    get a list of all friends of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    friends = []
    for page in tweepy.Cursor(api.friends, screen_name=user_name, wait_on_rate_limit=True,count=200).pages():
        try:
            friends.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return friends


def save_friends_to_csv(user_name, data):
    """
    saves json data to csv
    :param data: data recieved from twitter
    :return: None
    """
    HEADERS = ["screen_name"]
    with open(path, 'w',encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        """csv_writer.writerow(target)"""
        for profile_data in data:
            profile = []
            for header in HEADERS:
                profile.append(profile_data._json[header])
            csv_writer.writerow(profile)

if __name__ == '__main__':
    friends = get_friends(target)
    save_friends_to_csv(target, friends)




list = api.create_list(twitterlist, mode = mode) 

api.add_list_member(list_id = list.id_str, screen_name = target, owner_screen_name = user)

with open(path, 'r') as f:
    for line in f:
      try:  
        print(line)
        api.add_list_member(list_id = list.id_str, screen_name = line, owner_screen_name = user)
      except Exception:
        traceback.print_exc()
