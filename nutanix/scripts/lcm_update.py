#!/usr/bin/env python3.6

"""

    nutanix-clusters-lcm.py

    Connect to a Nutanix Prism Central instance, verify new software versions and update them if available

    The intention is to use this script as very high-level and *unofficial* as-built documentation for sites using Nutanix Prism Central
  
    You would need to *heavily* modify this script for use in a production environment so that it contains appropriate error-checking, exception handling and data collection

"""
# required modules
import os
import json
import argparse
import getpass
import requests
import sys
import urllib.request
import urllib.parse
import urllib3
from requests.auth import HTTPBasicAuth

__author__ = "Pierre Grothe @ Nutanix"
__version__ = "1.0"
__maintainer__ = "Pierre Grothe @ Nutanix"
__email__ = "pierre.grothe@nutanix.com"
__status__ = "Development/Demo"

cluster_ip = "172.16.32.10"
username = "admin"
password = "Not4Ya03!"
DISPLAY_OUTPUT = 0
ENTITY_RESPONSE_LENGTH = 50

def set_options():
    global ENTITY_RESPONSE_LENGTH
    ENTITY_RESPONSE_LENGTH = 50
    #global DISPLAY_OUTPUT
    #DISPLAY_OUTPUT = False

    global entity_totals
    entity_totals = {}

def get_options():
    global cluster_ip
    global username
    global password
    global DISPLAY_OUTPUT

    parser = argparse.ArgumentParser('Connect to Prism Central, gather some details and generate PDF documentation')
    parser.add_argument('-pcip', '--pcip', help='Prism Central IP address', default="172.16.32.10")
    parser.add_argument('-u', '--username', help='Prism Central username', default="admin")
    parser.add_argument('-p', '--password', help='Prism Central password', default="Not4Ya03!")

    
    args = parser.parse_args()

    if args.username:
        username = args.username
    else:
        username = input('Please enter your Prism Central username: ')

    if args.password:
        password = args.password
    else:
        password = getpass.getpass()

    if args.pcip:
        cluster_ip = args.pcip
    else:
        username = input('Please enter your Prism Central IP address: ')

    print("\n")


class ApiClient():

    def __init__(self, cluster_ip, request, body, username, password):
        self.cluster_ip = cluster_ip
        self.username = username
        self.password = password
        self.base_url = "https://%s:9440/api/nutanix/v3" % (self.cluster_ip)
        self.entity_type = request
        self.request_url = "%s/%s" % (self.base_url, request)
        self.body = body

    def get_info(self):

        print("Requesting '%s' ..." % self.entity_type )        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        try:
            r = requests.post(self.request_url, data=self.body, verify=False, headers=headers, auth=HTTPBasicAuth(self.username, self.password), timeout=10)
        except requests.ConnectTimeout:
            print('Connection timed out while connecting to %s. Please check your connection, then try again.' % self.cluster_ip)
            sys.exit()
        except requests.ConnectionError:
            print('An error occurred while connecting to %s. Please check your connection, then try again.' % self.cluster_ip)
            sys.exit()
        except requests.HTTPError:
            print('An HTTP error occurred while connecting to %s. Please check your connection, then try again.' % self.cluster_ip)
            sys.exit()
        
        if r.status_code >= 500:
            print('An HTTP server error has occurred (%s)' % r.status_code ) 
        else:
            if r.status_code == 401:
                print('An authentication error occurred while connecting to %s. Please check your credentials, then try again.' % self.cluster_ip)
                sys.exit()
            if r.status_code >= 401:
                print('An HTTP client error has occurred (%s)' % r.status_code )
                sys.exit()
            else:
                print('Connected and authenticated successfully.')
        
        return(r.json())

def show_intro():
    print( """
%s:

Connect to a Nutanix Prism Central instance, grab some high-level details then generate a PDF from it

Intended to generate a very high-level and *unofficial* as-built document for an existing Prism Central instance.

This script is GPL and there is *NO WARRANTY* provided with this script ... AT ALL.  You can use and modify this script as you wish, but please make sure the changes are appropriate for the intended environment.

Formal documentation should always be generated using best-practice methods that suit your environment.
""" % sys.argv[0])

def main():

    current_path = os.path.dirname(sys.argv[0])

    show_intro()

    # first we must make sure the cluster JSON file exists in the currect directory
    # if os.path.isfile( 'cluster.json' ) == True:
    
    # set the global options
    set_options()

    # get the cluster connection info
    get_options()

    # disable insecure connection warnings
    # please be advised and aware of the implications in a production environment!
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # make sure all required info has been provided
    if not cluster_ip:
        raise Exception("Cluster IP is required.")
    elif not username:
        raise Exception("Username is required.")
    elif not password:
        raise Exception("Password is required.")
    else:
        length = ENTITY_RESPONSE_LENGTH

        json_results = []
        endpoints = {}
        endpoints['clusters'] = [ 'cluster', ( '"length":%s' % length ) ]

        for endpoint in endpoints:
            if endpoints[endpoint][1] != '':
                client = ApiClient(cluster_ip, ( "%ss/list" % ( endpoints[endpoint][0] ) ), ( '{ "kind": "%s", %s }' % ( endpoints[endpoint][0], endpoints[endpoint][1] ) ), username, password )
            else:
                client = ApiClient(cluster_ip, ( "%ss/list" % ( endpoints[endpoint][0] ) ), ( '{ "kind": "%s" }' % ( endpoints[endpoint][0] ) ), username, password )
            results = client.get_info()
            json_results.append( [ endpoints[endpoint][0], results ] )
            
        print(json.dumps(json_results, indent = 4, sort_keys=True))

        clusters = json_results
        for cluster in clusters:
            for d in cluster:
                    print(d)

if __name__ == "__main__":
    main()
