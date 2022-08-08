import requests
import json
import time
 
# Workspace and report id https://www.twilio.com/docs/flex/developer/insights/api/export-data
# UPDATE this section
workspace_id = "kstp7so3c7hypws470e3gXXXXXX"
report_id = "2447"
login_email = "apanagidis@twilio.com"
password = ""
# # # # # # # # # # # #
 
login_url = 'https://analytics.ytica.com/gdc/account/login'
token_url = 'https://analytics.ytica.com/gdc/account/token'
raw_url= 'https://analytics.ytica.com/gdc/app/projects/'+ workspace_id +'/execute/raw'
 
headers = {
   'Accept': 'application/json',
   'Content-Type': 'application/json',
}
 
data = {"postUserLogin":{ "login": login_email, "password":password, "remember": 0, "verify_level": 2}}
 
# login: https://www.twilio.com/docs/flex/developer/insights/api/authentication#api-authentication
r_login = requests.post(login_url, headers=headers, json=data)
if r_login.status_code == 200:
   r_json=json.loads(r_login.content)
   token=r_json["userLogin"]["token"]
 
   headers = {
       'Accept': 'application/json',
       'Content-Type': 'application/json',
       'X-GDC-AuthSST': token,
   }
   # temporary token: https://www.twilio.com/docs/flex/developer/insights/api/authentication#retrieving-the-temporary-token
   r_token = requests.get(token_url, headers=headers)
   if r_token.status_code == 200:
       r_token_json=json.loads(r_token.content)
       temp_token=r_token_json["userToken"]["token"]
 
       # Export the raw report: https://www.twilio.com/docs/flex/developer/insights/api/export-data#export-the-raw-report
       cookies = {
       'GDCAuthTT': temp_token,
       }
 
       headers = {
           'Accept': 'application/json',
           'Content-Type': 'application/json',
       }
 
       url_setup = "/gdc/md/"+workspace_id+"/obj/"+report_id
       url_setup_s= json.dumps({ "report_req": { "report": url_setup } })
 
       r_url = requests.post(raw_url, headers=headers, cookies=cookies, data=url_setup_s)
       if r_url.status_code == 201:
           r_url_json=json.loads(r_url.content)
           uri=r_url_json["uri"]
           print(uri)
 
           # https://www.twilio.com/docs/flex/developer/insights/api/export-data#download-the-report
           download_url = "https://analytics.ytica.com/"+uri
           r_data = requests.get(download_url, headers=headers, cookies=cookies)
           while r_data.status_code == 202:
               time.sleep(1)
               print("waiting the report to become available")
           if r_data.status_code == 200:
               print(r_data.content)
