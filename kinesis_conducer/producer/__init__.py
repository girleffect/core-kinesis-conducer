import os

import boto3
from environs import Env

from kinesis_conducer.producer import GEKinesisProducer

env = Env()

# TODO generalise comment
# To ensure there are no Django startup issues, this module does not rely
# on settings.py for setup variables.
# It can also not be instantiated under all circumstances. The extra process
# the producer creates halts some of Django's management commands, as the
# process does not terminate automatically.
if env.bool("USE_KINESIS_PRODUCER", False) and not env.bool("BUILDER", False):
    print("Kinesis producer setup commencing...")

    print("Creating Kinesis session...")
    # Boto3 session that will be used for authentication
    KINESIS_SESSION = boto3.Session(**env.dict("KINESIS_SESSION"))

    print("Creating producer settings...")
    # The AsyncProducer that will be used to perform put_records
    PRODUCER_SETTINGS = env.dict("KINESIS_PRODUCER")
    print("Setting producer session...")
    PRODUCER_SETTINGS["boto3_session"] = KINESIS_SESSION

    print("Setting client settings...")
    # Override the boto3 client settings, if needed
    CLIENT_SETTINGS = env.dict("KINESIS_BOTO3_CLIENT_SETTINGS") \
        if "KINESIS_BOTO3_CLIENT_SETTINGS" in os.environ else dict()
    if CLIENT_SETTINGS.get("endpoint_url"):
        print("Setting producer client settings...")
        PRODUCER_SETTINGS["boto3_client_settings"] = CLIENT_SETTINGS

    print("Creating producer...")
    KINESIS_PRODUCER = GEKinesisProducer(**PRODUCER_SETTINGS)
    print("Kinesis producer created!")
