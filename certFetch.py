#!/usr/bin/env python

import subprocess
import json
import sys

# if requests is not installed, install it
try:
    import requests
except ModuleNotFoundError:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', 'requests', '--disable-pip-version-check'], stdout=subprocess.DEVNULL)
    import requests

# get the initial xsuaa information from CF HANA Gateway
try:
    oauthtoken = subprocess.check_output(["cf oauth-token"], shell=True, encoding="utf8").replace("bearer", "Bearer").strip()
except Exception as e:
    raise SystemExit(e)

# select the app to get the token from (i.e. hana-gateway, tenant-management)
# defaults to hana-gateway
app_to_use = 'hana-gateway'
#defaults to eu10, could also pass in api.cf.us30.hana.ondemand.com for example
url_to_use = 'api.cf.sap.hana.ondemand.com'

if len(sys.argv) > 1:
    app_to_use = sys.argv[1]

if len(sys.argv) > 2:
    url_to_use = sys.argv[2]

app_guid = subprocess.check_output([f'cf app --guid {app_to_use}'], shell=True, encoding="utf8")
url = f'https://{url_to_use.strip()}/v2/apps/{app_guid.strip()}/env'

headers = {
    'Accept': 'application/json',
    'Authorization': oauthtoken
}

try:
    resp = requests.get(url, headers=headers)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

# get the xsuaa data
json_data = json.loads(resp.text)
json_xsuaa = json_data["system_env_json"]["VCAP_SERVICES"]["xsuaa"][0]

cred_id = json_xsuaa["credentials"]["clientid"]
cred_certurl = json_xsuaa["credentials"]["certurl"]
cred_key = json_xsuaa["credentials"]["key"]
cred_cert = json_xsuaa["credentials"]["certificate"]

# create the certificate.pem file
certificatepem = open('certificate.pem', 'w')
certificatepem.write(cred_cert)
certificatepem.close()

# create the key.pem file
keypem = open('key.pem', 'w')
keypem.write(cred_key)
keypem.close()

# get the bearer token
dataparams = {
    'grant_type': 'client_credentials',
    'client_id': cred_id
}

urltoken = f'{cred_certurl}/oauth/token'

try:
    resp = requests.post(urltoken, data=dataparams, cert=('./certificate.pem', './key.pem'))
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

access_token = json.loads(resp.text)["access_token"]

print(access_token)