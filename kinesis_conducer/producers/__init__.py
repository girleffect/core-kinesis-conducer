import os

import boto3
from environs import Env

from kinesis_conducer.producers.producer import GEKinesisProducer

env = Env()


class DummyProducer:
    """
    A DummyProducer object to prevent attribute errors when the producer is
    used, but not setup. The producer does not have a response that processes
    should block for, making this a safe replacement.
    """

    def __getattr__(self, name):
        return self.__getattribute__("dummy_method")

    def dummy_method(self, *args, **kwargs):
        return None


# Instantiate dummy producer object, to be replaced if actual producer is setup
KINESIS_PRODUCER = DummyProducer()

# The extra process the producer creates has been known to halt some of the
# services' command line actions, as the process does not terminate
# automatically. It waits for a shutdown signal which it does not receive under
# most circumstances.
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
    print("Setting producer client settings...")
    PRODUCER_SETTINGS["boto3_client_settings"] = CLIENT_SETTINGS

    print("Creating producer...")
    KINESIS_PRODUCER = GEKinesisProducer(**PRODUCER_SETTINGS)
    print("Kinesis producer created!")
