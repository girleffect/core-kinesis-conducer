from kinesis_conducer.producer_events import utils

BASE_SCHEMA = {
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "event_type": {
            "type": "object",
        },
        "timestamp": {
            "type": "object",
        },
        "site_id": {
            "type": "object"
        }
    },
    "required": [
        "event_type",
        "timestamp",
        "site_id"
    ],
}


class EventTypes:
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    INVITATION_SENT = "INVITATION_SENT"
    INVITATION_REDEEMED = "INVITATION_REDEEMED"
    USER_DELETION_REQUESTED = "USER_DELETION_REQUESTED"
    EXPIRED_INVITATION_PURGE_REQUESTED = "EXPIRED_INVITATION_PURGE_REQUESTED"
    RESOURCE_CRUD = "RESOURCE_CRUD"

    SCHEMAS = {
        USER_LOGIN: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": USER_LOGIN
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer"
                },
                "user_id": {
                    "format": "uuid",
                    "type": "string"
                },
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "user_id"
            ],
        },
        USER_LOGOUT: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": USER_LOGOUT
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer"
                },
                "user_id": {
                    "format": "uuid",
                    "type": "string"
                },
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "user_id"
            ],
        },
        INVITATION_SENT: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": INVITATION_SENT
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer",
                    "minimum": 0
                },
                "invitation_id": {
                    "type": "string",
                    "format": "uuid"
                },
                "invitor_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The user that created the invitation"
                },
                "recipient_email": {
                    "type": "string",
                    "format": "email"
                },
                "organisation_id": {
                    "type": "integer"
                }
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "invitation_id",
                "invitor_id",
                "recipient_email",
                "organisation_id"
            ]
        },
        INVITATION_REDEEMED: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": INVITATION_REDEEMED
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer",
                    "minimum": 0
                },
                "invitation_id": {
                    "type": "string",
                    "format": "uuid"
                },
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The user that redeemed the invitation"
                }
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "invitation_id",
                "user_id"
            ],
        },
        USER_DELETION_REQUESTED: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": "USER_DELETION_REQUESTED"
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer",
                    "minimum": 0
                },
                "requestor_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The user that requested the deletion"
                },
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The user to be deleted"
                },
                "reason": {
                    "type": "string",
                }
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "requestor_id",
                "user_id",
                "reason"
            ]
        },
        EXPIRED_INVITATION_PURGE_REQUESTED: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": EXPIRED_INVITATION_PURGE_REQUESTED
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer",
                    "minimum": 0
                },
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "The user that requested the purge"
                },
                "cutoff_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Optional cut-off date specified"
                }
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "user_id"
            ]
        },
        RESOURCE_CRUD: {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "event_type": {
                    "type": "string",
                    "pattern": RESOURCE_CRUD
                },
                "timestamp": {
                    "type": "string",
                    "format": "date-time"
                },
                "site_id": {
                    "type": "integer",
                    "minimum": 0
                },
                "resource_urn": {
                    "type": "string",
                    "format": "urn"
                },
                "resource_id": {
                  "type": "string",
                  "description": "The id of the resource converted to a string",
                },
                "action": {
                    "type": "string",
                    "enum": ["create", "update", "delete"]
                },
                "user_id": {
                    "type": "string",
                    "format": "uuid",
                },
                "post_action_data": {
                    "type": "object",
                    "description": "Opaque object representing the state of the object"
                }
            },
            "required": [
                "event_type",
                "timestamp",
                "site_id",
                "resource_urn",
                "resource_id",
                "action",
                "user_id",
                "post_action_data"
            ]
        }
    }


# Check all schema definitions
for event_type, schema in EventTypes.SCHEMAS.items():
    utils.validate(schema["properties"], BASE_SCHEMA)
    assert event_type == schema["properties"]["event_type"]["pattern"]
