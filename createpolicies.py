#!/usr/bin/python
import json
import glob
import hvac
import sys, getopt
from pprint import pprint

def initVault(vurl, vtoken):
    global vault_client
    vault_client = hvac.Client(url=vurl, token=vtoken)

def writePolicies():
    for file in glob.glob("*.json"):
        print("Policy being written" + str(file.split('.')[0]))
        vault_client.set_policy(file.split('.')[0], open(file, 'r').read())

def listPolicies():
    print("Policies " +  str(vault_client.list_policies()))

def main(argv):
    write = ''
    listp = ''
    url = ''
    token = ''
    try:
       opts, args = getopt.getopt(sys.argv[1:],'hlwu:t:',['url','token','list','write'])
    except getopt.GetoptError:
       print 'createpolicies.py --list/write -u <vault url> -t <vault token>'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'createpolicies.py --list/write -u <vault url> -t <vault token>'
          sys.exit()
       elif opt in ("-u", "--url"):
          url = arg
       elif opt in ("-t", "--token"):
          token = arg
       elif opt in ("--list", "-l"):
          listp = 'true'
          write = 'false'
       elif opt in ("-w", "--write"):
          write = 'true'
          listp = 'true'
    initVault(url, token)
    if write == 'false':
        print("Listing policies")
        listPolicies()
    elif write == 'true':
        listPolicies()
        print("Writing policies")
        writePolicies()

if __name__ == "__main__":
   main(sys.argv[1:])
