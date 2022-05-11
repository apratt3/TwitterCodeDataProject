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

account_info_df.to_excel('api_account_info.xlsx') 
