# CEPH S3 Commands
This repo offers commands to interact with a CEPH file system account. This service exposes an API compatible with AWS S3, reason why the main dependency of this project is boto3.

# How to use it.

1. Create a `credentials.json` file. This file will contain the credentials to connect to the CEPH FS account. You'll find a `credentials.json.tpl` file as a reference indicating the credentials required. Please DON'T COMMIT `credentials.json` file (it is ignored in the repo just in case)

2. Create a virtualenv in python3 and install the requirements with `pip install -r requirements.txt`. The commands have been tested in Python 3.7 and 3.8.

3. Activate the virtualenv and proceed using the commands. Every file in this repo whose name starts with `ceph-` is a command. The name of he files are self-explanatory, describing the operation to execute. To run them, you just need to execute the appropriate python file and specify the argurment, if required. For instance, to list all the buckets in a CEPH account, just run:

`./ceph-list-buckets.py`

This is a command that requires no arguments. You can check every command arguments by running them with the `-h` option (help) or by looking at the file content.
