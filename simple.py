import requests
import apify_client
import json
import pandas as pd 

def tweet_finder(tweet_url):
    url = 'https://api.apify.com/v2/acts/epcsht~twitter-profile-scraper/runs?token=apify_api_9dlIv1Wp4AMrZcTHofLuaMj3d7WcvA38NBdr'
    url2 = 'https://api.apify.com/v2/datasets?offset=0&limit=99&desc=true&unnamed=true&token=apify_api_9dlIv1Wp4AMrZcTHofLuaMj3d7WcvA38NBdr'
    myobj = {'somekey': 'somevalue'}

    myobj = {"addUserInfo": False,
        "maxItems": 20,
        "proxy": {
            "useApifyProxy": False,
            "proxyUrls": [
                "http://wwbqyspk-1:krvrehhik4mj@p.webshare.io:80"
            ]
        },
        "startUrls": [
            tweet_url
        ]}

    into = requests.post(url, json = myobj)
    dataset_list = requests.get(url2)
    dataset_list = dataset_list.text
    dataset_list_string = str(dataset_list)
    #print(dataset_list_string[1:200])
    id_index = dataset_list_string.index("id")
    dataset_id = (dataset_list_string[(id_index+6):(id_index+23)])
    #print(dataset_id)
    url2 = 'https://api.apify.com/v2/datasets/' + dataset_id + '/items?token=apify_api_9dlIv1Wp4AMrZcTHofLuaMj3d7WcvA38NBdr&format=csv'
    tweets_out = requests.get(url2)
    tweets_out = (tweets_out.text)
    tweets_out = str(tweets_out)
    print(tweets_out)
    with open('tweet_file.csv', 'w', encoding="utf8") as out:
        out.write(tweets_out)
    df_tweet = pd.read_csv('tweet_file.csv')
    print(df_tweet.columns.values)
    df_favorite_counts = df_tweet.favorite_count
    df_text = df_tweet.full_text
    return df_text, df_favorite_counts 

'''input3 = input("Enter a url link to your twitter account: ")
text, favorites = tweet_finder(input3)

text = list(text)
favorites = list(favorites)

output_3l = []
output_1l = []
output_2l = []
for i in range (len(text)):
    inpute = text[i]
    output_1ll, output_2ll, output_3ll = init(inpute)
    output_1l+=output_1ll
    output_2l+=output_2ll
    output_3l+=output_3ll

#weights_1t, weights_2t, weights_3t = init(input3)'''