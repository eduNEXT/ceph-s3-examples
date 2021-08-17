#! /usr/bin/env python3


import os
import sys
from argparse import ArgumentParser
import json

import boto3
from botocore.exceptions import ClientError


with open('credentials.json', 'r') as fd:
    credentials = json.loads(fd.read())

generic_open_cors = [
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "HEAD",
            "GET",
            "PUT"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
]

command_description = '''This command allow to get, set, or delete a group of Static CORS rules
in a bucket. These CORS rules enables access from any host to the bucket, using HEAD, GET, or PUT
requests. This is required for for specific cases'''


def main():

    parser = ArgumentParser(description=command_description)
    parser.add_argument('--bucket-name',
                        dest='bucket_name',
                        action='store',
                        required=True,
                        help='the name of the bucket to create')
    parser.add_argument('--create-bucket',
                        action='store_true',
                        dest='create_bucket',
                        help='Set this flag to force the bucket creation if it does not exist')
    parser.add_argument('--action',
                        default='get',
                        choices=['set', 'get', 'delete'],
                        dest='cors_action',
                        help='Set the action to perform with CORS. By default the command gets the bucket CORS rules')
    args = parser.parse_args()

    s3 = boto3.resource('s3',
                        endpoint_url=credentials['endpoint_url'],
                        aws_access_key_id=credentials['access_key'],
                        aws_secret_access_key=credentials['secret_key'])

    bucket = s3.Bucket(args.bucket_name)
    bucket.creation_date

    if args.create_bucket:
        bucket.create()

    if not bucket.creation_date:
        sys.exit(
            'The bucket you specified does not exist. You can use the option --create-bucket to force bucket creation'
        )

    if args.cors_action == 'delete':
        bucket.Cors().delete()
        print(f'Successfully deleted generic CORS rules from bucket {bucket.name}')
    elif args.cors_action == 'set':
        bucket.Cors().put(CORSConfiguration={'CORSRules': generic_open_cors})
        print(f'Successfully added generic CORS rules to bucket {bucket.name}')
    else:  # This is the get default action processing
        try:
            cors_rules = bucket.Cors().cors_rules
        except ClientError as e:
            # Check the exception message to check if it is a known error
            if 'NoSuchCORSConfiguration' not in str(e):
                raise
            cors_rules = []

        print(f'Cors rules for bucket {bucket.name}: {cors_rules}')


if __name__ == '__main__':
    main()
