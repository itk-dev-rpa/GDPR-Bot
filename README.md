# GDPR-Bot

## About

This robot is made to delete data in an OpenOrchestrator database.

When run it will check if data in the database is older than the input values and then
delete it as needed.

## Usage

The robot takes the following arguments as input in a JSON string:

- **Delete_Logs**: The maximum age of logs before they're.
- **Delete_Queues**: The maximum age of queue elements they're deleted.
- **Anon_Queue_Reference**: The maximum age of queue elements before their reference is deleted.
- **Anon_Queue_Data**: The maximum age of queue elements before their data is deleted.
- **Anon_Queue_Message**: The maximum age of queue elements before their message is deleted.

All values are given in days.
If a value is not defined or less than 1 the action is skipped.

A queue element's age is measured by its creation time.

Example JSON:

```json
{
    "Delete_Logs": 30,
    "Delete_Queues": 60,
    "Anon_Queue_Reference": 14,
    "Anon_Queue_Data": 14,
    "Anon_Queue_Message": 45
}
```
