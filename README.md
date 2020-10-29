# syncthing-backup

This small program uses [Syncthing](https://syncthing.net)'s [REST
API](https://docs.syncthing.net/dev/rest.html) backup files incrementally each time local SyncThing has finished syncing a folder. (No worries: the API is queried on
the machine on which you run `syncthing-activity`.)


## Requirements

### Get api key 
Open Syncthing's Web UI at `http://127.0.0.1:8384`, click on _Actions_ and
_Settings_. On the Settings panel, _General_ tab you'll find the API key on the
right. Copy that into an environment variable before launching
`syncthing-activity.py`:

```bash
export SYNCTHING_APIKEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
./syncthing-activity.py
```
If your Syncthing is listening on a special URL, you can additionally override
the default URL:

```bash
export SYNCTHING_URL="http://localhost:8384"
```

## usage
`./syncthing-activity` 
Run this command to simply monitor all folders and copy new files to the backup location. 
Additionally files will be moved to the folder/archive subfolder (so that the user knows those files have been backed up and can delete them safely). 

`./syncthing-activity photos` 
Run this command to monitor all Syncthing folders with "photos" in their name and copy new files to the backup location. 
Additionally files will be moved to the folder/archive subfolder (so that the client device can still use those files, but the user can easily empty the /archive folder if needed). 


## example

The family runs Syncthing-fork on their Android phones. 
The folders /Pictures are being synced to a home NAS/PC. 
On that PC, I run this script to continuously monitor completed sync actions of folders with "Pictures" in their name. 
For example "Tom's Pictures" will be monitored but "Tom's AppBackups" will not. 

To-Do (have to figure this part out yet, with rsync and mv commands): 
When new photos are created in the phone /Picture folder, Syncthing will sync those to the PC.
Then syncthing-backup.py will copy new/modified files to a backup location (not synced by Syncthing). 
Lastly, it moves these files to the /Picture/archive folder, and syncs those changes back to the phone. 

Tom, will now still be able to use/see his pictures, but whenever he runs out of storage, he can delete items in /Pictures/archive (or delete ../archives folder). 

Done:
For debugging, logfile is created each time a folder with a specific name has completed syncing. 
