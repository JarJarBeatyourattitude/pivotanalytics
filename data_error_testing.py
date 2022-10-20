import data
input1 = ("I am a panda or something idk")
response = data.setup(input1)
nap = data.tester(response)
#weights_1, weights_2, weights_3 = data(nap)

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

