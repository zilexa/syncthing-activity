#!/usr/bin/env python3

import requests
import time
import json
import sys
import os
import re

__author__    = "Jan-Piet Mens <jp@mens.de>"
__copyright__ = "Copyright 2019 Jan-Piet Mens"
__license__   = "GNU General Public License"

last_id = 0
folders = {}

def getfolders(data):

    global folders

    for f in data['folders']:
        folders[f["id"]] = {
            "label" : f["label"],
        }

def process(array, pat=None):
    """ process if pattern `pat' (regular expression) can be found in
        folder label or item """

    global last_id


    for event in array:
        if "type" in event and event["type"] == "FolderCompletion":
            last_id = event["id"]
            
            folder_label = folders[folder_id]["label"]
            
            e = {
                "time"          : event["time"],
                "type"          : event["type"],
                "completion"    : event["data"]["completion"],
                "device"        : event["data"]["device"],
                "folder"        : event["data"]["folder"],
                "folder_label"  : folder_label,
            }
            
            if pat:
                s = "{folder_label}".format(**e)
                if not re.search(pat, s):
                    continue
                    
            # print(json.dumps(e, indent=4))
            print("{time:>15} {device:>15} {folder_label:>15}".format(**e))

def main(url, apikey, pat):
    headers = { "X-API-Key" : apikey }

    r = requests.get("{0}/rest/system/config".format(url), headers=headers)
    getfolders(json.loads(r.text))

    while True:

        params = {
            "since" : last_id,
            "limit" : 1,
            "events" : "FolderCompletion",
        }

        r = requests.get("{0}/rest/events".format(url), headers=headers, params=params)
        if r.status_code == 200:
            process(json.loads(r.text), pat)
        elif r.status_code != 304:
            time.sleep(60)
            continue
        time.sleep(10.0)

if __name__ == "__main__":

    url = os.getenv("SYNCTHING_URL", "http://localhost:8384")
    apikey = os.getenv("SYNCTHING_APIKEY")
    if apikey is None:
        print("Missing SYNCTHING_APIKEY in environment", file=sys.stderr)
        exit(2)

    pattern = None
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    try:
        main(url, apikey, pattern)
    except KeyboardInterrupt:
        exit(1)
    except:
        raise
