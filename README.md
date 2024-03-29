# GDPR-Bot

## About

This robot is made to delete data in an OpenOrchestrator database.

When run it will check if data in the database is older than the input values and then
delete it as needed.

## Usage

The robot takes the following arguments as input in a JSON string:

- **Delete_Logs**: The maximum age of logs before they're deleted.
- **Delete_Queues**: The maximum age of queue elements before they're deleted.
- **Delete_Queue_References**: The maximum age of queue elements before their reference is deleted.
- **Delete_Queue_Data**: The maximum age of queue elements before their data is deleted.
- **Delete_Queue_Messages**: The maximum age of queue elements before their message is deleted.

All values are given in days.
If a value is not defined or less than 1 the action is skipped.

A queue element's age is measured by its creation time.

Example JSON:

```json
{
    "Delete_Logs": 30,
    "Delete_Queues": 60,
    "Delete_Queue_References": 14,
    "Delete_Queue_Data": 14,
    "Delete_Queue_Messages": 45
}
```
