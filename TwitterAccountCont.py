import botometer
import pprint
import pandas 


#AAAAAAAAAAAAAAAAAAAAAPODZAEAAAAA%2FsmCaYZVxAniDWfhv1opVrWar%2F0%3DpJoLq8QdQWkCI4cq6PpgG90BG63Eo42UEATvolJgO0sK6uDyPu
rapidapi_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
twitter_app_auth = {
    'consumer_key': 'XXXXXXXXXXXXXXXXXXXXX',
    'consumer_secret': 'XXXXXXXXXXXXXXXXX',
    'access_token': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'access_token_secret': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

# Check a single account by screen name
#result = bom.check_account('@clayadavis')
#pprint.pprint(result)

# Check a single account by id
#result = bom.check_account(1548959833)

# Check a sequence of accounts
#df = pandas.DataFrame.read_csv (r'C:X:InsertFileLocationHere')
accounts = ['@BarackObama', '@rihanna', '@kanyewest','@cristiano','@elonmusk','@KimKardashian','@jtimberlake','@selenagomez','@BillGates','@shakira','@jimmyfallon',"@kingjames",'@KylieJenner','@wizkhalifa','@LilTunechi','@aliciakeys','@Adele','@pitbull','@Eminem','@NICKIMINAJ','@POTUS','@JoeBiden','@LILUZIVERT','@lizzo','@JColeNC','@SupremeDreams_1','@Zendaya','@iamcardib','@PennBadgley','@TomHolland1996','@RobertDowneyJr','@ChrisEvans','@Xolo_Mariduena','@euphoriaHBO','@anguscloud','@chrishemsworth','@TheRock','@KevinHart4real','@KorporateCold','@Beyonce','@JeffBezos','@stephenasmith','@ladygaga','@FLOTUS','@finnwolfhard','@calebmclaughin','@IncredibleCulk','@TomCruise','@VancityReynolds','@oliviarodrigo','@billieeilish','@sza','@theestallion','@50cent','@lilbaby4PF','@gherbo','@Polo_Capalot','@lildurk','@1GunnaGunna','@Drake','@VP','@KamalaHarris','@MarvelStudios','@SpiderManMovie','@PlayStation','@tonyhawk','@tonyparker','@Harry_Styles','@itskerrii','@naomiosaka','@cordae','@MileyCyrus','@JohnCena','@JordanPeele','@KekePalmer','@Nickelodeon','@SnoopDogg','@drdrew','@RobertSmith','@WilliamZabka'
,'@ralphmaccino','@PeytonList','@CobraKaiSeries','@Nope_Movie','@TheBoysTV','@JackQuaid92','@EFMoriarty','@squawksquare','@JeffTutorials','@Manic_Marge','@WholeMarsBlog','@thepennyhoarder','@BillyM2k','@STL_Tech','@NatGeoTV','@cartoonnetwork','@MisterCtoons','@amazon','@PrimeVideo','@camerondallas','@netflix','@joelmchale','@michaelianblack','@blackmirror'
]
account_list = []
account_index = []

for screen_name, result in bom.check_accounts_in(accounts):
    # this will be appended to the new dataframe
    row = {}
    def label_conversion(row):      
        if row["type"] == 'human':    
            return 1    
        elif row["type"] == 'ORGANIZATION':    
            return 2    
        else:    
            return 0 # bot 

    # we use a try-catch because we do not want it to stop execution if botometer fails to get stats on an account.
    try:
        if result["user"]["majority_lang"] == 'en':
            row = {
                "id": result["user"]["user_data"]["id_str"],
                "CAP": result['cap']['english'],
                "astroturf": result['display_scores']['english']['astroturf'],
                "fake_follower": result['display_scores']['english']['fake_follower'],
                "financial": result['display_scores']['english']['financial'],
                "other": result['display_scores']['english']['other'],
                "overall": result['display_scores']['english']['overall'],
                "self-declared": result['display_scores']['english']['self_declared'],
                "spammer": result['display_scores']['english']['spammer'],
                "type": result['display_scores']['english']['type'],
            }
        else:
            row = {
                "id": result["user"]["user_data"]["id_str"],
                "CAP": result['cap']['universal'],
                "astroturf": result['display_scores']['universal']['astroturf'],
                "fake_follower": result['display_scores']['universal']['fake_follower'],
                "financial": result['display_scores']['universal']['financial'],
                "other": result['display_scores']['universal']['other'],
                "overall": result['display_scores']['universal']['overall'],
                "self-declared": result['display_scores']['universal']['self_declared'],
                "spammer": result['display_scores']['universal']['spammer'],
                "type": result['display_scores']['universal']['type']
            }

        account_list.append(row)
        account_index.append(screen_name)

        # notify that we are done processing
        print(f'{result["user"]["user_data"]["id_str"]} has been processed.')

    # skip if error
    except Exception as e:
        print("{} Could not be fetched: {}".format(id, e))

account_info_df = pandas.DataFrame(account_list, index=account_index)

account_info_df.to_csv('api_account_info.csv') # you can name the file whatever you want
   
# determining the name of the file
# saving the excel
account_info_df.to_excel('X:nameoffile.xlsx')
