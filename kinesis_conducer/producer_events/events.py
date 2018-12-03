from datetime import datetime
import json
import pytz

from kinesis_conducer.producer_events import schemas, utils
from kinesis_conducer.producers import KINESIS_PRODUCER


def put_event(event_type, site_id, **kwargs):
    """
    Generic method used to put all event types into Kinesis.
    """

    schema = schemas.EventTypes.SCHEMAS[event_type]

    # Append BASE_SCHEMA values to all event data
    kwargs.update(
        {
            "timestamp": f"{datetime.utcnow().isoformat()}Z",
            "site_id": site_id,
            "event_type": event_type
        }
    )
    utils.validate(kwargs, schema)

    # Base producer supports only the singular put event, it does a
    # boto3.client.put_records of all queued events.
    KINESIS_PRODUCER.put(json.dumps(kwargs), partition_key=event_type)
