import botometer 

import pandas as pd 

import matplotlib.pyplot as plt 

  

""" 

this program uses the training set to create histograms for 

each account type (human, bot, organization) using the 

english and universal display scores. The results of running this 

should be: 

    - 6 pngs with 7 subplots each 

    - 6 csv files with 7 columns each 

""" 

rapidapi_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX" 

twitter_app_auth = { 

    'consumer_key': 'XXXXXXXXXXXXXXXXXXX', 

    'consumer_secret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX', 

    # 'access_token': 'YOUR_ACCESS_TOKEN_HERE', 

    # 'access_token_secret': 'YOUR_ACCESS_TOKEN_SECRET_HERE', 

} 

bom = botometer.Botometer(wait_on_ratelimit=True, 

                          rapidapi_key=rapidapi_key, 

                          **twitter_app_auth) 

  

# turning the id column into a list makes it easier to iterate through 

training_set = pd.read_csv(r'C:InsertFileLocation.csv') 

ids = training_set['id'].tolist() 

  

# these empty dataframes will be used to hold english and universal scores for each account type 

columns_list = ["id", "CAP", "astroturf", "fake follower", "financial", "other", "overall", "self-declared", "spammer", 

                "label"] 

eng_results_df = pd.DataFrame(columns=columns_list) 

univ_results_df = pd.DataFrame(columns=columns_list) 

  

for id, result in bom.check_accounts_in(ids): 

    # for loop uses the list of ids to get dictionary of information for each account 

    # try statement throws an exception if corresponding twitter account cannot be found for id 

    label = 0 

    row = {} 

    try: 

        if result["user"]["majority_lang"] == 'en': 

            if (training_set.iat[ids.index(id), 1]).lower() == "human": 

                label = 1 

            elif (training_set.iat[ids.index(id), 1]).lower() == "bot": 

                label = 0 

            elif (training_set.iat[ids.index(id), 1]).lower() == "organization": 

                label = 2 

            row = pd.DataFrame({ 

                "id": [result["user"]["user_data"]["id_str"]], 

                "CAP": [result['cap']['english']], 

                "astroturf": [result['display_scores']['english']['astroturf']], 

                "fake follower": [result['display_scores']['english']['fake_follower']], 

                "financial": [result['display_scores']['english']['financial']], 

                "other": [result['display_scores']['english']['other']], 

                "overall": [result['display_scores']['english']['overall']], 

                "self-declared": [result['display_scores']['english']['self_declared']], 

                "spammer": [result['display_scores']['english']['spammer']], 

                "label": [label] 

            }, columns=columns_list) 

            eng_results_df = pd.concat([eng_results_df, row], ignore_index=True) 

  

        else: 

            if (training_set.iat[ids.index(id), 1]).lower() == "human": 

                label = 1 

            elif (training_set.iat[ids.index(id), 1]).lower() == "bot": 

                label = 0 

            elif (training_set.iat[ids.index(id), 1]).lower() == "organization": 

                label = 2 

            row = pd.DataFrame({ 

                "id": [result["user"]["user_data"]["id_str"]], 

                "CAP": [result['cap']['english']], 

                "astroturf": [result['display_scores']['english']['astroturf']], 

                "fake follower": [result['display_scores']['english']['fake_follower']], 

                "financial": [result['display_scores']['english']['financial']], 

                "other": [result['display_scores']['english']['other']], 

                "overall": [result['display_scores']['english']['overall']], 

                "self-declared": [result['display_scores']['english']['self_declared']], 

                "spammer": [result['display_scores']['english']['spammer']], 

                "label": [label] 

            }, columns=columns_list) 

            univ_results_df = pd.concat([univ_results_df, row], ignore_index=True) 

  

        print(f'{id} has been processed.') 

  

    except Exception as e: 

        print("{} could not be fetched: {}".format(id, e)) 

  

# the contents of the dataframes are strings but histograms cant use strings 

# astype() converts the dataframes to floats 

# so that they can be used to make histograms 

human_eng = eng_results_df[eng_results_df["label"] == 1] 

human_eng = human_eng[columns_list[2:9]].astype(float) 

bot_eng = eng_results_df[eng_results_df["label"] == 0].astype(float) 

bot_eng = bot_eng[columns_list[2:9]].astype(float) 

org_eng = eng_results_df[eng_results_df["label"] == 2].astype(float) 

org_eng = org_eng[columns_list[2:9]].astype(float) 

human_univ = eng_results_df[eng_results_df["label"] == 1].astype(float) 

human_univ = human_univ[columns_list[2:9]].astype(float) 

bot_univ = eng_results_df[eng_results_df["label"] == 0].astype(float) 

bot_univ = bot_univ[columns_list[2:9]].astype(float) 

org_univ = eng_results_df[eng_results_df["label"] == 2].astype(float) 

org_univ = org_univ[columns_list[2:9]].astype(float) 

  

# saves all the dataframes to two csv files 

# one csv file for english accounts and another for universal 

# index=False keeps the dataframe from creating a blank column for the indexes 

eng_results_df.to_csv(r'C:InsertFileLocation.csv', index=False) 

univ_results_df.to_csv(r'C:InsertFileLocation.csv', index=False) 

  

# formats and saves all the histogram plots to png files 

# figsize allows you to specify the size of the graph 

# tight_layout() keeps the graphs and titles from overlapping 

# suptitle() adds a title 

# all of these are optional. i like the way these values make the graphs look, 

# but you can change them to whatever you want 

human_eng_hist = human_eng.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Human (English)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

bot_eng_hist = bot_eng.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Bot (English)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

org_eng_hist = org_eng.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Organization (English)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

human_univ_hist = human_univ.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Human (Universal)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

bot_univ_hist = bot_univ.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Bot (Universal)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

org_univ_hist = org_univ.hist(figsize=(15, 12)) 

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 

plt.suptitle("Organization (Universal)") 

plt.savefig(r'C:InsertFileLocation.png') 

  

# displays the histograms. if you dont care to see them then you dont have to include this 

# they will be saved to the png files regardless 

plt.show() 
