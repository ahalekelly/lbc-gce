#!/usr/bin/env python3
import os
import yaml
import sys
import keyring, keyrings.alt
from datetime import datetime

# restart if running on a Skylake server because they're slower. Hope for Broadwell next time.
if '2000.0' in open('/proc/cpuinfo').read():
    import shutdown
    shutdown.restart()

os.chdir(os.path.dirname(sys.argv[0])) # set working directory

# Get Metadata items from google cloud
os.system("gcloud compute project-info describe > gcloud-items.yaml")
with open("gcloud-items.yaml", 'r') as stream:
    try:
        itemList = yaml.load(stream)['commonInstanceMetadata']['items']
    except yaml.YAMLError as exc:
        print(exc)
        exit()
os.remove("gcloud-items.yaml")

#Process items
items = {item['key']: item['value'] for item in itemList}
del items['ssh-keys']

#Set pushbullet API key
if isinstance(keyring.get_keyring(), keyrings.alt.file.EncryptedKeyring):
    keyring.set_keyring(keyrings.alt.file.PlaintextKeyring())
keyring.set_password("pushbullet", "cli", items['pushbullet-key'])

#Log time
with open("collider.log", 'a') as logfile:
    logfile.write("\n\n"+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Start LBC
os.system("cd /home/shardbearer/collider && sudo ./LBC --address "+items['btc-address']+" --id "+items["lbc-id"]+" --secret "+items["lbc-secret"]+" --cpus 24 >> collider.log & 2>&1")
