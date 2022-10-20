import requests
import data 
import operator 
from operator import add
import statistics
from operator import mul


d, text, favorites = data.tweet_finder('https://twitter.com/finkd')
print(len(text))
s_list = []
for i in range(len(text)):
    input = text[i]
    r = requests.get('https://api.uclassify.com/v1/uClassify/Sentiment/classify/?readKey=CXv5qrtonYLk&text=' + input)
    r_max = len(r.text)
    r = (float)(r.text[r_max-8:r_max-1])
    s_list.append(r)


top_1_list = []
top_2_list = []
top_3_list = []

for i in range(len(text)):
  top_1_list += d["output1_" + str(i)]
  top_2_list += d["output2_" + str(i)]
  top_3_list += d["output3_" + str(i)]

print(top_1_list[5])

top_1_list = list([d["output1_0"]])
top_2_list = list([d["output2_0"]])
top_3_list = list([d["output3_0"]])
i = 0

# Function to turn each list thing from map into something weighted somehow idk 
#Maybe use likes to turn each score to be negative or positive (factor from median)

d, text, favorites = data.tweet_finder('https://twitter.com/Jonatha68658584')


print("before: " + str(d["output1_1"]))
median = statistics.median(favorites)
if (median==0):
    median = 1
for i in range(len(text)):
    fav_check = (favorites[i]/median)-1
    fav_score = favorites[i]/median
    if (fav_check<1):
        fav_score = -1*(1/(favorites[i]/median+.000001))
    d["output1_" + str(i)] += [i * fav_score for i in d["output1_" + str(i)]]
    d["output2_" + str(i)] +=  [i * fav_score for i in d["output2_" + str(i)]]
    d["output3_" + str(i)] +=  [i * fav_score for i in d["output3_" + str(i)]]


print("after: " + str(d["output1_9"]))
print(median)
print(text[9])

#Scale max fav score to 1 so it matches the lowest fav score of -1 

top_1_added = list([d["output1_0"]])
top_2_added = list([d["output2_0"]])
top_3_added = list([d["output3_0"]])
i = 0
while i < (len(text)-1):
  i += 1
  top_1_addedd = list(map(add, list([d["output1_" + (str)(i)]]), (top_1_added))) 
  top_2_addedd = list(map(add, list([d["output2_" + (str)(i)]]), (top_2_added)))
  top_3_addedd = list(map(add, list([d["output3_" + (str)(i)]]), (top_3_added)))

input2 = input("Enter your draft tweet to be scored:")
weights_1i, weights_2i, weights_3i = data.init(input2)
top_1 = weights_1i
top_2 = weights_2i
top_3 = weights_3i

print(top_1)
print(top_2)

top_1_added = [item for sublist in top_1_addedd for item in sublist]
top_2_added = [item for sublist in top_2_addedd for item in sublist]
top_3_added = [item for sublist in top_3_addedd for item in sublist]


top_1_score = sum(list(map(operator.mul,top_1_added, top_1)))
top_2_score = sum(list(map(operator.mul,top_2_added, top_2)))
top_3_score = sum(list(map(operator.mul,top_3_added, top_3)))

print(top_3_score)