from requirments import *
# required twitter keys
API_KEY = API_KEY
API_KEY_SECRET = API_KEY_SECRET
BEARER_TOKEN = BEARER_TOKEN
ACCESS_TOKEN = ACCESS_TOKEN
ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET
CLIENT_ID = CLIENT_ID
CLIENT_SECRET = CLIENT_SECRET
# twitter auth


def OAuth():
    try:
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth
    except Exception as e:
        return None


oauth = OAuth()
api = tweepy.API(oauth, parser=tweepy.parsers.JSONParser())
# BEARER_TOKEN
auth1 = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
api2 = tweepy.API(auth1)
client = tweepy.Client(BEARER_TOKEN)
# usa world id
usa_woeid = 23424977
# twitter trending based on world id



def gptTweet():

    trending = api.get_place_trends(usa_woeid)
    trending1 = str(random.choice(trending[0]['trends'][:20]))
    # openAI NLP tweet creation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": danPrompt +
                promptTwitterAddOn+tweetPrompts+trending1}
        ]
    )
    reply = str(response['choices'][0]['message']['content'])
    reply1 = reply.split('\n')
    for i in range(len(reply1)):
        if 'DAN: ' in reply1[i]:
            reply2 = reply1[i].strip('DAN: ')
            reply2 = reply2.strip('\"')
            try:

                api.update_status(reply2)
                print(reply2)
                
            except:
                print('error')
    else:
        pass



schedule.every(30).minutes.do(gptTweet)
while True:
    schedule.run_pending()
