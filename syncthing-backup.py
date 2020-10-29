#!/usr/bin/env python3

import requests
import time
import json
import sys
import os
import re
import logging

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
            "path"  : f["path"],
        }

def process(array, pat=None):
    """ process if pattern `pat' (regular expression) can be found in
        folder label or item """

    global last_id


    for event in array:
        if "type" in event and event["type"] == "ItemFinished":
            last_id = event["id"]
            
            folder_id = event["data"]["folder"]
            folder_label = folders[folder_id]["label"]
            folder_path = folders[folder_id]["path"]

            path = os.path.join(folder_path, event["data"]["item"])

            e = {
                "time"          : event["time"],
                "type"          : event["type"],
                "action"        : event["data"]["action"],
                "error"         : event["data"]["error"],
                "item"          : event["data"]["item"],
                "folder_label"  : folder_label,
                "path"          : path,
            }
            
            if pat:
                s = "{folder_label}".format(**e)
                if not re.search(pat, s):
                    continue
            if event["data"]["action"] == "update":
            # print(json.dumps(e, indent=4))
           # print("{time:>20} {type:>10} {action:>5} {error:>5} {folder_label:>15} {path:>15}".format(**e))
              logging.basicConfig(level=logging.DEBUG, filename="syncthing-backup.log", filemode="a+",
                          format="%(asctime)-15s %(levelname)-8s %(message)s")
              logging.info("{time:>20} {type:>10} {action:>10} {folder_label:>15} {path:>50}".format(**e))

def main(url, apikey, pat):
    headers = { "X-API-Key" : apikey }

    r = requests.get("{0}/rest/system/config".format(url), headers=headers)
    getfolders(json.loads(r.text))

    while True:

        params = {
            "since" : last_id,
            "limit" : 1,
            "events" : "ItemFinished",
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
