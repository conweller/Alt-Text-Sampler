import requests
import base64
import sys

from creds import CONSUMER_KEY, CONSUMER_SECRET


KEY_SECRET = '{}:{}'.format(CONSUMER_KEY, CONSUMER_SECRET).encode('ascii')
B64_ENCODED_KEY = base64.b64encode(KEY_SECRET)
B64_ENCODED_KEY = B64_ENCODED_KEY.decode('ascii')

BASE_URL = 'https://api.twitter.com/'
AUTH_URL = f'{BASE_URL}oauth2/token'

AUTH_HEADERS = {
    'Authorization': f'Basic {B64_ENCODED_KEY}',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

AUTH_DATA = {
    'grant_type': 'client_credentials'
}

AUTH_RESP = requests.post(AUTH_URL, headers=AUTH_HEADERS, data=AUTH_DATA)

ACCESS_TOKEN = AUTH_RESP.json()['access_token']

SEARCH_HEADERS = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


def get_tweets_by_query(query):
    search_params = {
        'q': query,
        'include_entities': 'true',
        'include_entities': 'true',
        'result_type': 'mixed',
        'count': 100,
    }

    search_url = f'{BASE_URL}1.1/search/tweets.json'

    search_resp = requests.get(search_url, headers=SEARCH_HEADERS, params=search_params).json()
    statuses = []
    for idx, status in enumerate(search_resp['statuses']):
        search_params = {
            'id': status['id'],
            'include_ext_alt_text': 'true',
            'count': 100,
        }
        search_url = f'{BASE_URL}1.1/statuses/show.json'
        search_resp = requests.get(
            search_url,
            headers=SEARCH_HEADERS,
            params=search_params
        ).json()
        statuses.append(search_resp)
    return statuses


def get_tweets_by_user(username):
    search_params = {
        'include_ext_alt_text': 'true',
        'screen_name': username,
        'count': 200,
    }

    search_url = f'{BASE_URL}1.1/statuses/user_timeline.json'

    search_resp = requests.get(
        search_url,
        headers=SEARCH_HEADERS,
        params=search_params
    ).json()
    return search_resp


def count_alt_text_for_imgs(response):
    count_img = 0
    count_alt = 0

    for tweet in response:
        date = int(tweet.get('created_at', '0').split()[-1])
        if 'extended_entities' in tweet and date > 2016:
            if 'media' in tweet['extended_entities']:
                for media in tweet['extended_entities']['media']:
                    if media['type'] == 'photo':
                        count_img += 1
                        if media['ext_alt_text'] is not None:
                            count_alt += 1
    return count_img, count_alt


if __name__ == "__main__":
    assert(len(sys.argv) == 2)
    if sys.argv[1] == "t50":
        usernames = [
            'BarackObama', 'justinbieber', 'katyperry', 'rihanna', 'taylorswift13',
            'Cristiano', 'ladygaga', 'realDonaldTrump', 'TheEllenShow', 'ArianaGrande',
            'YouTube', 'KimKardashian', 'jtimberlake', 'selenagomez', 'narendramodi',
            'twitter', 'cnnbrk', 'britneyspears', 'ddlovato', 'shakira'
        ]
        count_img = 0
        count_alt = 0
        for name in usernames:
            img, alt = count_alt_text_for_imgs(get_tweets_by_user(name))
            print(name)
            print("\tImages found:", img)
            print("\tImages containing alt-text found:", alt)
            count_img += img
            count_alt += alt

        print("Total number of images:", count_img) # 988
        print("Total number of images containing alt text:", count_alt) # 0
    elif sys.argv[1] == 'kw':
        keywords = [
            'graphs',
            'bar graph',
            'line graph',
            'pie chart',
            'flow chart',
            'line plot',
            'scatterplot',
            'boxplot',
            'diagram',
            'infographic',
            'histogram',
        ]
        count_img = 0
        count_alt = 0

        for keyword in keywords:
            img, alt = count_alt_text_for_imgs(get_tweets_by_query(sys.argv[1]))
            print(keyword)
            print("\tImages found:", img)
            print("\tImages containing alt-text found:", alt)
            count_img += img
            count_alt += alt

        print("Total number of images:", count_img) # 83
        print("Total number of images containing alt text:", count_alt) # 0


