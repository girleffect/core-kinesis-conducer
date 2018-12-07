from importlib import reload
from unittest import TestCase
from unittest import mock
from unittest.mock import patch, MagicMock
import uuid

import jsonschema

from kinesis_conducer.producer_events import events, schemas, utils


class TestPutEventsSchemaValidation(TestCase):
    login_event = schemas.EventTypes.USER_LOGIN
    logout_event = schemas.EventTypes.USER_LOGOUT

    @mock.patch.dict(
        schemas.EventTypes.SCHEMAS[schemas.EventTypes.USER_LOGIN],
        {
            "properties": {
                "event_type": "string"
            }
        }
    )
    def  test_base_schema_schema_validation(self):
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            for event_type, schema in schemas.EventTypes.SCHEMAS.items():
                utils.validate(schema["properties"], schemas.BASE_SCHEMA)
                assert event_type == schema["properties"]["event_type"]["pattern"]

    @patch("kinesis_conducer.producer_events.events.KINESIS_PRODUCER.put")
    def test_login_event_schema_validation(self, mocked_put):
        mocked_put.return_value = None
        data = {
            "user_id": str(uuid.uuid1())
        }
        events.put_event(self.login_event, 1, **data)
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            events.put_event(self.login_event, 1)
        self.assertEqual(e.exception.args[0], "'user_id' is a required property")
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            events.put_event(self.login_event, 1, user_id="a")
        self.assertEqual(e.exception.args[0], "'a' is not a 'uuid'")

    @patch("kinesis_conducer.producer_events.events.KINESIS_PRODUCER.put")
    def test_logout_event_schema_validation(self, mocked_put):
        mocked_put.return_value = None
        data = {
            "user_id": str(uuid.uuid1())
        }
        events.put_event(self.logout_event, 1, **data)
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            events.put_event(self.logout_event, 1)
        self.assertEqual(e.exception.args[0], "'user_id' is a required property")
        with self.assertRaises(jsonschema.exceptions.ValidationError) as e:
            events.put_event(self.logout_event, 1, user_id="b")
        self.assertEqual(e.exception.args[0], "'b' is not a 'uuid'")
