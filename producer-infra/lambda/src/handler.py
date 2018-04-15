from __future__ import print_function

import base64
import json
import boto3
import os

sts = boto3.client('sts')

def get_or_die(e):
    var = os.getenv(e)
    if not var:
        print("Could get get necessary environment variable: " + e)
        exit(1)
    return var

# https://gist.github.com/gene1wood/938ff578fbe57cf894a105b4107702de
def role_arn_to_session(**args):
    """
    Usage :
        session = role_arn_to_session(
            RoleArn='arn:aws:iam::012345678901:role/example-role',
            RoleSessionName='ExampleSessionName')
        client = session.client('sqs')
    """
    response = sts.assume_role(**args)
    return boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])

role_to_assume = get_or_die('RoleToAssume')
forwarding_stream_name = get_or_die('ForwardingStreamName')

ca_session = role_arn_to_session(
    # FIXME:
    # - get role from ssm
    # - figure out role expiry and cycle as-necessary
    RoleArn = role_to_assume,
    RoleSessionName = 'cross-accountlambda-event-forwarder'
)

# the cross-accout kinesis client
ca_kinesis = ca_session.client('kinesis')

def main(event, context):

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record['kinesis']['data'])

        print("Decoded payload: " + payload)

        response = ca_kinesis.put_record(
            StreamName=forwarding_stream_name,
            Data=payload,
            PartitionKey='some-key',
        )

        print("forwarded payload: ", response)

    return 'Successfully processed {} records.'.format(len(event['Records']))

