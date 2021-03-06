import requests
import urllib3
import re
import string
urllib3.disable_warnings()

print("\nillumio Policy Status Changer")
print("Note: Used in a POC to demonstrate time based segmentation use case + help to illustrate integration with automation tools using scripts\n")
print('{:<50s}'.format("< List of Policies >") + ("< Policy State >"))
pce_url = "https://demo6.illum.io/api/v2"                                               #The PCE URL
org = "/orgs/org_id/"                                                                   #Ensure you have the correct org ID
username = "api_username"                                                               #The API username
password = "api_password"                                                               #The API password
cert_check = True                                                                       #False for self-signed, else put True

response = requests.get(url=pce_url+org+"sec_policy/draft/rule_sets", verify=cert_check, auth=(username, password)) #Retrieve rulesets information from PCE
number_of_policies = len(response.json())                                               #Find out how many policies are there in the list
start_num = 0                                                                           #Starts the counting up from 0
while start_num < number_of_policies:                                                   #Keep going until every item in the list is done
    if response.json()[start_num]['enabled'] == True:                                   #Convert Boolean result to represent if a policy is Enabled or Disabled
        policy_status = "Enabled"
    else:
        policy_status = "Disabled"
    print('{:<50s}'.format(str(start_num) + ". " + response.json()[start_num]['name']) + policy_status)  # Displays the policy created in PCE
    start_num += 1                                                                      #Adding 1 to the count up

user_choice = input("Select number between 0-" + str(number_of_policies-1) + ": ")      #Specify the number range a user should choose
user_choice = int(user_choice)                                                          #Converts user input into integer
policy_number = response.json()[user_choice]["href"]                                    #Selects href from the user list index
policy_href_list = re.sub('['+string.punctuation+']', ' ', policy_number).split()       #split href into individual items in a list
if response.json()[user_choice]["enabled"] == True:                                     #If the selected policy is enabled, disable it
    requests.put(url=pce_url + org + "sec_policy/draft/rule_sets/" + policy_href_list[-1], verify=cert_check, auth=(username, password), json={"enabled": False})
    requests.post(url=pce_url + org + "sec_policy", verify=cert_check, auth=(username, password), json={"change_subset": {"rule_sets": [{"href": org + "sec_policy/draft/rule_sets/" + policy_href_list[-1]}]}, "update_description": "Modified over API"})
    print("\nPolicy Disabled Successfully\nPlease refresh the PCE UI > Segmentation Rulesets")
else:                                                                                   #Else, the selected policy is disabled
    requests.put(url=pce_url + org + "sec_policy/draft/rule_sets/" + policy_href_list[-1], verify=cert_check, auth=(username, password), json={"enabled": True})
    requests.post(url=pce_url + org + "sec_policy", verify=cert_check, auth=(username, password), json={"change_subset": {"rule_sets": [{"href": org + "sec_policy/draft/rule_sets/" + policy_href_list[-1]}]}, "update_description": "Modified over API"})
    print("\nPolicy Enabled & Provisioned Successfully\nPlease refresh the PCE UI > Segmentation Rulesets")
