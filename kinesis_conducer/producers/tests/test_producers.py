import os
from importlib import reload
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, MagicMock

import environs

from kinesis_conducer import producers
from kinesis_conducer.producers.producer import GEKinesisProducer


class TestGEKinesisProducerInstantiation(TestCase):
    """
    Environment variables must be set on a test to test basis. The variables
    can NOT be set using tox or any other global means. If the subprocess is
    spun up for any reason it will block the test suite.

    NOTE: Patch the SubprocessLoop/KinesisProducer start method to prevent
    startup.

    Env vars in use:
    USE_KINESIS_PRODUCER=<boolean>
    KINESIS_SESSION=<key=val,...>
    KINESIS_PRODUCER=<key=val,...>
    KINESIS_BOTO3_CLIENT_SETTINGS=<key=val,...>
    """

    def test_default(self):
        reload(producers)
        self.assertEqual(producers.KINESIS_PRODUCER.__class__, producers.DummyProducer)

    @mock.patch.dict(
        os.environ,
        {
            "USE_KINESIS_PRODUCER": "true",
            "KINESIS_SESSION": "aws_access_key_id=foobar,aws_secret_access_key=foobar,region_name=us-east-1",
            "KINESIS_PRODUCER": "stream_name=test-stream",
            "KINESIS_BOTO3_CLIENT_SETTINGS": "endpoint_url=http://localstack:4568"
        }
    )
    @patch("kinesis_conducer.producers.producer.GEAsyncProducer.start", MagicMock(return_value=None))
    def test_full_env_var(self):
        reload(producers)
        self.assertEqual(producers.KINESIS_PRODUCER.__class__, GEKinesisProducer)

    @mock.patch.dict(
        os.environ,
        {
            "USE_KINESIS_PRODUCER": "true",
        }
    )
    def test_no_configuration(self):
        with self.assertRaises(environs.EnvError) as e:
            reload(producers)
        self.assertEqual(e.exception.args, ('Environment variable "KINESIS_SESSION" not set',))

    @mock.patch.dict(
        os.environ,
        {
            "USE_KINESIS_PRODUCER": "true",
            "KINESIS_SESSION": "aws_access_key_id=foobar,aws_secret_access_key=foobar,region_name=us-east-1",
        }
    )
    def test_session_only_configuration(self):
        with self.assertRaises(environs.EnvError) as e:
            reload(producers)
        self.assertEqual(e.exception.args, ('Environment variable "KINESIS_PRODUCER" not set',))

    @mock.patch.dict(
        os.environ,
        {
            "USE_KINESIS_PRODUCER": "true",
            "KINESIS_SESSION": "aws_access_key_id=foobar,aws_secret_access_key=foobar,region_name=us-east-1",
            "KINESIS_PRODUCER": "stream_name=test-stream",
        }
    )
    # With the Queue mocked, this is not strictly needed
    @patch("kinesis_conducer.producers.producer.GEAsyncProducer.start", MagicMock(return_value=None))
    @patch("kinesis_conducer.producers.producer.multiprocessing.Queue", MagicMock(return_value=None))
    @patch("kinesis_conducer.producers.producer.GEAsyncProducer.__init__")
    def test_session_and_producer_configuration(self, init):
        init.return_value = None
        reload(producers)
        init.assert_called_with(
            boto3_client_settings={},
            boto3_session=producers.KINESIS_SESSION,
            buffer_time=0.5,
            max_count=None,
            max_size=None,
            # NOTE: Mocked value
            queue=None,
            stream_name='test-stream'
        )

    @mock.patch.dict(
        os.environ,
        {
            "USE_KINESIS_PRODUCER": "true",
            "KINESIS_SESSION": "aws_access_key_id=foobar,aws_secret_access_key=foobar,region_name=us-east-1",
            "KINESIS_PRODUCER": "stream_name=test-stream",
            "KINESIS_BOTO3_CLIENT_SETTINGS": "endpoint_url=http://localstack:4568"
        }
    )
    # With the Queue mocked, this is not strictly needed
    @patch("kinesis_conducer.producers.producer.GEAsyncProducer.start", MagicMock(return_value=None))
    @patch("kinesis_conducer.producers.producer.multiprocessing.Queue", MagicMock(return_value=None))
    @patch("kinesis_conducer.producers.producer.GEAsyncProducer.__init__")
    def test_full_config_init_values_configuration(self, init):
        init.return_value = None
        reload(producers)
        init.assert_called_with(
            boto3_client_settings={"endpoint_url": "http://localstack:4568"},
            boto3_session=producers.KINESIS_SESSION,
            buffer_time=0.5,
            max_count=None,
            max_size=None,
            # NOTE: Mocked value
            queue=None,
            stream_name='test-stream'
        )
