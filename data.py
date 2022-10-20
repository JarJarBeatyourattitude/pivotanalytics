from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import numpy as np
import requests
import apify_client
import requests
import json
import pandas as pd 
import data 

def setup(input1):
    response = predict_text_classification_single_label_sample(
        project="754491550466",
        endpoint_id="1954285161348595712",
        location="us-central1",
        content = input1
    )
    return response

def predict_text_classification_single_label_sample(
    project: str,
    endpoint_id: str,
    content: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
    ):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = predict.instance.TextClassificationPredictionInstance(
        content=content,
    ).to_value()
    instances = [instance]
    parameters_dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    #print("response")
    #print(" deployed_model_id:", response.deployed_model_id)

    predictions = response.predictions
    listy = np.array([])

    for prediction in predictions:
        np.append(listy, (dict(prediction)))
        #print(" prediction:", dict(prediction))
    return prediction




def tester(response):
  
  resp = (dict(response))
  poss = list(resp)
  confidence_i = poss.index("confidences")
  subreddit_i = poss.index("displayNames")
  id_i = poss.index("ids")
  liste = np.array( tuple(resp.values()) )
  s_names = (liste[(subreddit_i):(subreddit_i+1)]).flatten()
  s_values = (liste[(confidence_i):(confidence_i+1)]).flatten()  

  #print("This should be a number: " + (str)(s_values[0:1]))
  #print("This should be a word: " + (str)(s_names[0:1]))

  z_n =[x for _, x in sorted(zip(s_values, s_names), key=lambda pair: pair[0])]
  z_n = np.flipud(z_n)
  z_v = np.sort(s_values)
  z_v = np.flipud(z_v)
  nap = np.array([z_n, z_v])
  nap_n = nap[1]
  nap_n = nap_n.astype(float)
  nap_list = nap_n.tolist()
  master_list = []
  nap_t = nap[0]
  nap_t_list = nap_t.tolist()
  for i in range(len(nap_list)):
    if (nap_list[i]>= 0.02):
      temp_i = "Subreddit: " + (nap_t_list[i]) + "\nConfidence: " + (str)(round(nap_list[i]*100)) + "%"
      print(temp_i)
  return nap



def data(nap):
    import pandas as pd
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSQgkEMMGB8y2KR2OheV1sQS1uiLSsNjCR3RHem63o_ZZbPff2zBdKIdza9zzdyJabEeA-Qlw25lUEz/pub?gid=1675254761&single=true&output=tsv', sep='\t', names=['subreddit','category_1', 'category_2', 'category_3'])
    #print(df)
    c = {}

    #Initializing 
    for i in range (1013):
        c[(i)] = float(0)

    for i in range(938):
        columnn = df.subreddit.str.contains(nap[0,i]).idxmax()
        weight_i = nap[1,i]
        c[columnn] += (float)(weight_i)

    d = {}

    for i in range(1012):
        i = i + 1
        category_1 = df.loc[i, 'category_1']
        category_2 = df.loc[i, 'category_2']
        category_3 = df.loc[i, 'category_3']
        d[category_1] = 0
        d[category_2] = 0
        d[category_3] = 0
    #print(df.loc[2, "category_2"])
    #print(d['data recovery'])

    for i in range(1012):
        i = i + 1
        category_1 = df.loc[i, 'category_1']
        category_2 = df.loc[i, 'category_2']
        category_3 = df.loc[i, 'category_3']
        d[category_1] += c[i]
        d[category_2] += c[i]
        d[category_3] += c[i]

    category_1_list = df['category_1']
    category_2_list = df['category_2']
    category_3_list = df['category_3']

    from collections import OrderedDict
    category_1_list = list(OrderedDict((x, True) for x in category_1_list).keys())
    category_2_list = list(OrderedDict((x, True) for x in category_2_list).keys())
    category_3_list = list(OrderedDict((x, True) for x in category_3_list).keys())

    weights_1 = []
    for i in (category_1_list)[1:]:
        weights_1.append(d[i])
    weights_2 = []
    for i in (category_2_list)[1:]:
        weights_2.append(d[i])
    weights_3 = []
    for i in (category_3_list)[1:]:
        weights_3.append(d[i])
    data = {
        'Category 1': category_1_list,
        'Score1': weights_1,
        'Category 2': category_2_list,
        'Score2': weights_2,
        'Category 3': category_3_list,
        'Score3': weights_3
    }


    dm = pd.DataFrame.from_dict(data, orient='index')
    dm = dm.transpose()


    print(dm)
    return (weights_1, weights_2, weights_3)

def init(input1):
  response = setup(input1)
  nap = tester(response)
  weights_1, weights_2, weights_3 = data(nap)
  return weights_1, weights_2, weights_3

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
    id_index = dataset_list_string.index("id")
    dataset_id = (dataset_list_string[(id_index+6):(id_index+23)])
    url2 = 'https://api.apify.com/v2/datasets/' + dataset_id + '/items?token=apify_api_9dlIv1Wp4AMrZcTHofLuaMj3d7WcvA38NBdr&format=csv'
    tweets_out = requests.get(url2)
    tweets_out = (tweets_out.text)
    tweets_out = str(tweets_out)
    #print(tweets_out)
    with open('tweet_file.csv', 'w', encoding="utf8") as out:
        out.write(tweets_out)
    df_tweet = pd.read_csv('tweet_file.csv')
    #print(df_tweet.columns.values)
    df_favorite_counts = df_tweet.favorite_count
    df_text = df_tweet.full_text
    text = list(df_text)
    favorites = list(df_favorite_counts)
    d = {}

    for i in range (len(text)):
        inpute = text[i]
        d["output1_{}".format(i)], d["output2_{}".format(i)], d["output3_{}".format(i)] = init(inpute)
    return d, text, favorites
#nap = tester(response)    