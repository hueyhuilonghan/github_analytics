#!/usr/bin/env python
# coding: utf-8
import requests
import json
import pandas as pd


username = 'hueyhuilonghan'
token = '54545cce103d8c5181667870dae85da1f1810e06'

index = []
df_list = []

for issue_num in range(47602, 53614):
    print(issue_num)

    # create a re-usable session object with the user creds in-built
    gh_session = requests.Session()
    gh_session.auth = (username, token)

    request_url = 'https://api.github.com/repos/cockroachdb/cockroach/issues/{}'.format(issue_num)
    
    response = json.loads(gh_session.get(request_url).text)    
    
    if "message" in response:
        if response["message"] == "Not Found":
            continue
        if response["message"] == "This issue was deleted":
            continue

    for key in ["user", "closed_by", "pull_request", "labels", "assignee", "assignees", "milestone"]:
        if key in response:
            response[key] = [response[key]]
        else:
            response[key] = None

    index.append(issue_num)
    df_list.append(pd.DataFrame(response))

# get dataframe
df = pd.concat(df_list)

# export dataframe
df.to_pickle("issues.pkl")
