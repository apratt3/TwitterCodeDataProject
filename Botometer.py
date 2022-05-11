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
rapidapi_key = "InsertKey" 

twitter_app_auth = { 

    'consumer_key': 'InsertKey', 

    'consumer_secret': 'InsertKey', 

     'access_token': 'YOUR_ACCESS_TOKEN_HERE', 

     'access_token_secret': 'YOUR_ACCESS_TOKEN_SECRET_HERE', 

} 

bom = botometer.Botometer(wait_on_ratelimit=True, 

                          rapidapi_key=rapidapi_key, 

                          **twitter_app_auth) 

  

# turning the id column into a list makes it easier to iterate through 

training_set = pd.read_csv(r'C: InsertFileLocation') 

ids = training_set['id'].tolist() 

  

# these empty dataframes will be used to hold english and universal scores for each account type 

human_eng = pd.DataFrame(columns=["astroturf", "fake follower", 

                                  "financial", "other", "overall", "self-declared", "spammer"]) 

bot_eng = pd.DataFrame(columns=["astroturf", "fake follower", 

                                "financial", "other", "overall", "self-declared", "spammer"]) 

org_eng = pd.DataFrame(columns=["astroturf", "fake follower", 

                                "financial", "other", "overall", "self-declared", "spammer"]) 

human_univ = pd.DataFrame(columns=["astroturf", "fake follower", 

                                   "financial", "other", "overall", "self-declared", "spammer"]) 

bot_univ = pd.DataFrame(columns=["astroturf", "fake follower", 

                                 "financial", "other", "overall", "self-declared", "spammer"]) 

org_univ = pd.DataFrame(columns=["astroturf", "fake follower", 

                                 "financial", "other", "overall", "self-declared", "spammer"]) 

  

for id, result in bom.check_accounts_in(ids): 

    # for loop uses the list of ids to get dictionary of information for each account 

    # try statement throws an exception if corresponding twitter account cannot be found for id 

  

    try: 

        if result["user"]["majority_lang"] == 'en': 

            # if the majority of the user's tweets are in english, use the english display scores 

            # otherwise, use the universal display scores 

            # creates 7x1 row dataframe that contains the account's scores 

            # concatenates this row to one of the original dataframes based on the account's type and language 

            row = pd.DataFrame([[ 

                result['display_scores']['english']['astroturf'], 

                result['display_scores']['english']['fake_follower'], 

                result['display_scores']['english']['financial'], 

                result['display_scores']['english']['other'], 

                result['display_scores']['english']['overall'], 

                result['display_scores']['english']['self_declared'], 

                result['display_scores']['english']['spammer']]], 

                columns=["astroturf", "fake follower", 

                         "financial", "other", "overall", "self-declared", "spammer"]) 

  

            if (training_set.iat[ids.index(id), 1]).lower() == "human": 

                human_eng = pd.concat([human_eng, row], ignore_index=True) 

            elif (training_set.iat[ids.index(id), 1]).lower() == "bot": 

                bot_eng = pd.concat([bot_eng, row], ignore_index=True) 

            elif (training_set.iat[ids.index(id), 1]).lower() == "organization": 

                org_eng = pd.concat([org_eng, row], ignore_index=True) 

  

        else: 

            row = pd.DataFrame([[ 

                result['display_scores']['universal']['astroturf'], 

                result['display_scores']['universal']['fake_follower'], 

                result['display_scores']['universal']['financial'], 

                result['display_scores']['universal']['other'], 

                result['display_scores']['universal']['overall'], 

                result['display_scores']['universal']['self_declared'], 

                result['display_scores']['universal']['spammer']]], 

                columns=["astroturf", "fake follower", 

                         "financial", "other", "overall", "self-declared", "spammer"]) 

  

            if (training_set.iat[ids.index(id), 1]).lower() == "human": 

                human_univ = pd.concat([human_univ, row], ignore_index=True) 

            elif (training_set.iat[ids.index(id), 1]).lower() == "bot": 

                bot_univ = pd.concat([bot_univ, row], ignore_index=True) 

            elif (training_set.iat[ids.index(id), 1]).lower() == "organization": 

                org_univ = pd.concat([org_univ, row], ignore_index=True) 

  

        # these strings make it easy to see how many ids you have gone through 

        # they are also useful for detecting errors in your code 

        print(f'{id} has been processed.') 

  

    except Exception as e: 

        print("{} could not be fetched: {}".format(id, e)) 

  

# the contents of the dataframes are strings but histograms cant use strings 

# astype() converts the dataframes to floats 

# so that they can be used to make histograms 

human_eng = human_eng.astype(float) 

bot_eng = bot_eng.astype(float) 

org_eng = org_eng.astype(float) 

human_univ = human_univ.astype(float) 

bot_univ = human_univ.astype(float) 

org_univ = human_univ.astype(float) 

  

# saves all the dataframes to two csv files 

# uses concat() to create a hierarchically indexed dataframe 

# one csv file for english accounts and another for universal 

# index=False keeps the dataframe from creating a blank column for the indexes 

eng_merged = pd.concat([human_eng, bot_eng, org_eng], axis=1, keys=['human', 'bot', 'organization']) 

eng_merged.to_csv(r'C:CreateFileLocation', index=False) 

univ_merged = pd.concat([human_univ, bot_univ, org_univ], axis=1, keys=['human', 'bot', 'organization']) 

univ_merged.to_csv(r'C:CreateFileLocation', index=False) 

  

# formats and saves all the histogram plots to png files 

# figsize allows you to specify the size of the graph 

# tight_layout() keeps the graphs and titles from overlapping 

# w_pad and h_pad are used to specify how much space is between each graph 

# all of these are optional. i like the way these values make the graphs look, 

# but you can change them to whatever you want 

human_eng_hist = human_eng.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

bot_eng_hist = bot_eng.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

org_eng_hist = org_eng.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

human_univ_hist = human_univ.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

bot_univ_hist = bot_univ.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

org_univ_hist = org_univ.hist(figsize=(15, 12)) 

plt.tight_layout(w_pad=3, h_pad=3) 

plt.savefig(r'C:CreateFileLocation.png') 

  

# displays the histograms. if you dont care to see them then you dont have to include this 

# they will be saved to the png files regardless 

plt.show() 
