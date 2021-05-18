import requests
import json
import pandas as pd
import os

# remove if output file already exists
if os.path.exists("output.csv"):
  os.remove("output.csv")

# main GraphQL query
query = """ 
{
  community {
    teams(limit: $total_count, offset: $start_index) {
      totalCount
      values {
        name
        id
        createdDate
        teamPublicId
        url
        category
        lentAmount
        loanCount
        membershipType
        loanBecause
        description
        whereabouts
        lenderCount
      }
    }
  }
}
"""

# query to get total count of teams
tc_query = """ 
{
  community {
    teams(limit: 1) {
      totalCount
    }
  }
}
"""

url = 'https://api.kivaws.org/graphql'

#run tc_query to get the total team count in tc
resp = requests.get(url, json={'query': tc_query})
json_data = json.loads(resp.text)
try:
    tc = json_data["data"]["community"]["teams"]["totalCount"]
except Exception as e:
    tc = 0
    print("Response code : "+ str(resp.status_code) + "\t" + "Error : "+ str(e))

#create empty dataframes to store json responses
df_final = pd.DataFrame()
df_temp = pd.DataFrame()

#set $total_count to tc in main query
query = query.replace("$total_count",f'{tc}')

#for loop with range of tc and step count of 100
for index in range(0,tc, 100):
    # set start_index to index values 0,100,200,300.............
    user_query = query.replace("$start_index",f'{index}')
    resp = requests.get(url, json={'query': user_query})
    json_data = json.loads(resp.text)
   
    try:
      # store json response for each iteration in temp dataFrame
      df_temp = pd.DataFrame(json_data["data"]["community"]["teams"]["values"])
    except Exception as e:
      print("Response code : "+ str(resp.status_code) + "\t" + "Error : "+ str(e))
      break
    # append the temp dataframe to final dataframe
    df_final = df_final.append(df_temp,ignore_index=False)

# write the dataframe to output csv file 
df_final.to_csv('output.csv',sep=',',encoding='utf-8',index=False)