import requests
import os
import json


username = os.environ.get('APIC_USERNAME', None)
password = os.environ.get('APIC_PASSWORD', None)
Token = ""
header = {"content-type": "application/json"}


def get_token(username, password):
    r = requests.post('https://sandboxapicem.cisco.com/api/v1/ticket',
                 data = json.dumps({'username':username,
                                    'password':password
                                                    }),headers=header, verify = False)
    r_json = r.json()
    Token = {'X-auth-token':r_json['response']['serviceTicket']}
    return Token

def get_devices():
    token = get_token(username,password)
    r = requests.get('https://sandboxapicem.cisco.com/api/v1/network-device', headers = token,verify = False);
    res = r.json()
    resp = ''
    for host in res['response']:
        response = (host['type'],host['serialNumber'],host['macAddress'])
        resp = resp + str(response)
    return resp
    return resp

def get_reachability():
    token = get_token(username,password)
    r = requests.get('https://sandboxapicem.cisco.com/api/v1/reachability-info', headers = token,verify = False);
    res = r.json()
    resu = ''
    for host in res['response']:
        response = (host['mgmtIp'], host['reachabilityStatus'])
        resp = resp + str(response)
    return resp
    return resp

def get_hosts():
    token = get_token(username,password)
    r = requests.get('https://sandboxapicem.cisco.com/api/v1/host', headers = token,verify = False);
    res = r.json()
    resp = ''
    for host in res['response']:
        response = (host['hostIp'],host['hostMac'])
        resp = resp + str(response)
    return resp
    return resp
