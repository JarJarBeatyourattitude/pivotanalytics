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
import operator 
from operator import add
from operator import mul
import statistics

'''!gcloud auth application-default login
  ^Authenticate for a new runtime '''

#Input for topics: 

input2 = input("Enter your draft tweet to be scored:")
weights_1i, weights_2i, weights_3i = data.init(input2)

input3 = input("Enter a url link to your twitter account: ")
d, text, favorites = data.tweet_finder(input3)

#For this work, let's start with example/fake scores and code for that, then set up the real time analysis with AWS
#Test initializations: ( _r ending defines variables based on original scan )

#Running sentiment on past tweets
r_list = []
l_list = []
for i in range(len(text)):
    input = text[i]
    r = requests.get('https://api.uclassify.com/v1/uClassify/Sentiment/classify/?readKey=CXv5qrtonYLk&text=' + input)
    r_max = len(r.text)
    r = (float)(r.text[r_max-8:r_max-1])
    r_list.append(r)
    l = len(input.split())
    l_list.append(l)
f_sum = sum(favorites)
if (f_sum == 0):
  f_sum = 1
r_avg = 0
l_avg = 0
#Finds the average positivity weighted as each tweets favorite count share from the whole 
for i in range (len(text)):
  r_avg = r_avg + (favorites[i] / f_sum) * r_list[i]
  l_avg = l_avg + (favorites[i] / f_sum) * l_list[i]

top_1_list = []
top_2_list = []
top_3_list = []

for i in range(len(text)):
  top_1_list += d["output1_" + (str)(i)]
  top_2_list += d["output2_" + (str)(i)]
  top_3_list += d["output3_" + (str)(i)]

median = statistics.median(favorites)
if (median==0):
    median = 1
    #Weights each value 
    #This design heavily rewards and punishes, maybe it should only mainly reward with a small bit punish?
for i in range(len(text)):
    fav_check = (favorites[i]/median)-1
    fav_score = favorites[i]/median
    if (fav_check<1):
        fav_score = -1*(1/(favorites[i]/median+.000001))
    d["output1_" + str(i)] += [i * fav_score for i in d["output1_" + str(i)]]
    d["output2_" + str(i)] +=  [i * fav_score for i in d["output2_" + str(i)]]
    d["output3_" + str(i)] +=  [i * fav_score for i in d["output3_" + str(i)]]

#Thingy to add up all weighted scores from each tag to each other for total 
for i in range(len(text)):
  top_1_list = map(add, d["output1_" + (str)(i)], top_1_list)   
  top_2_list = map(add, d["output2_" + (str)(i)], top_2_list)
  top_3_list = map(add, d["output3_" + (str)(i)], top_3_list)



top_1_added = list([d["output1_0"]])
top_2_added = list([d["output2_0"]])
top_3_added = list([d["output3_0"]])
i = 0
while i < (len(text)-1):
  i += 1
  top_1_added = list(map(add, list([d["output1_" + (str)(i)]]), (top_1_added))) 
  top_2_added = list(map(add, list([d["output2_" + (str)(i)]]), (top_2_added)))
  top_3_added = list(map(add, list([d["output3_" + (str)(i)]]), (top_3_added)))

#Running sentiment on current draft tweet 
tweet = input2
r = requests.get('https://api.uclassify.com/v1/uClassify/Sentiment/classify/?readKey=CXv5qrtonYLk&text=' + tweet)
r_len = len(r.text)
r = (float)(r.text[r_len-8:r_len-1])
l = len(tweet.split())
top_1 = weights_1i
top_2 = weights_2i
top_3 = weights_3i

r_score = 1-(abs(r_avg-r))
l_score = 1-(abs(l_avg-l))/l_avg
#Finding topic score super simply by multiplying weighted past list with new list then adding up all numbers 
top_1_added = [item for sublist in top_1_added for item in sublist]
top_2_added = [item for sublist in top_2_added for item in sublist]
top_3_added = [item for sublist in top_3_added for item in sublist]
top_1_score = sum(list(map(operator.mul,top_1_added, top_1)))
top_2_score = sum(list(map(operator.mul,top_2_added, top_2)))
top_3_score = sum(list(map(operator.mul,top_3_added, top_3)))

#Past tweets we have: r_list, (sentiment list) l_list, (length list) and top_ 1,2,3 _list added (topic list) 
#Draft tweet we have r_score, (sentiment) l_score, (length) and top_ 1,2,3 (topic list)

#How should we go about this now we have all the important data? 
#We could make an ai to find the value of each variable for an account, but it's data intensive
#Also they're already favorite-weighted, so an AI wouldn't use that data anyway 
#r_score and l_score range from 0 to 1 

weights = [0.2,0.2,0.2,0.2,0.2]

estimate = (median * weights[0] * 2 * r_score) + (median * weights[1] * 2 * l_score) + (median * weights[2] * 120 * top_1_score)+ (median * weights[2] * 120 * top_2_score)+ (median * weights[2] * 120 * top_3_score)
print("Your estimated favorite count is " + str(estimate))

print("Look at the size of " + str(top_1_score) + " and " + str(top_2_score) + ". If it's small, you might have to scale it up a lot.")
