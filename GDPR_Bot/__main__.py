"""The main module of the project."""

import json
from datetime import datetime, timedelta
import time

from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from OpenOrchestrator.database import db_util
from OpenOrchestrator.database.logs import Log
from OpenOrchestrator.database.queues import QueueElement
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


def main():
    """The main function of the process."""
    orchestrator_connection = OrchestratorConnection.create_connection_from_args()

    log_info(orchestrator_connection, "Starting GDPR process.")

    # Unpack arguments
    args = orchestrator_connection.process_arguments
    args = json.loads(args)

    # Create connection
    conn_string = db_util.get_conn_string()
    engine = create_engine(conn_string)

    # Delete logs
    days = args.get("Delete_Logs", 0)
    if days > 0:
        with Session(engine) as session:
            delete_logs(days, session, orchestrator_connection)
    else:
        log_info(orchestrator_connection, "Skipping: Delete logs")

    # Delete queue elements
    days = args.get("Delete_Queues", 0)
    if days > 0:
        with Session(engine) as session:
            delete_queue_elements(days, session, orchestrator_connection)
    else:
        log_info(orchestrator_connection, "Skipping: Delete queue elements")

    # Delete queue references
    days = args.get("Anon_Queue_Reference", 0)
    if days > 0:
        with Session(engine) as session:
            anon_queue_reference(days, session, orchestrator_connection)
    else:
        log_info(orchestrator_connection, "Skipping: Delete queue element references")

    # Delete queue data
    days = args.get("Anon_Queue_Data", 0)
    if days > 0:
        with Session(engine) as session:
            anon_queue_data(days, session, orchestrator_connection)
    else:
        log_info(orchestrator_connection, "Skipping: Delete queue element data")

    # Delete queue messages
    days = args.get("Anon_Queue_Message", 0)
    if days > 0:
        with Session(engine) as session:
            anon_queue_message(days, session, orchestrator_connection)
    else:
        log_info(orchestrator_connection, "Skipping: Delete queue element messages")

    engine.dispose()


def delete_logs(days: int, session: Session, orchestrator_connection: OrchestratorConnection):
    """Delete all logs in the database older than the given number of days.

    Args:
        days: The maximum age of logs before deletion.
        session: The sqlalchemy session to perform the action.
        orchestrator_connection: The connection to Orchestrator.
    """
    cutoff_date = datetime.today() - timedelta(days=days)

    log_info(orchestrator_connection, f"Deleting logs before: {cutoff_date.date()}")

    query = (
        select(Log)
        .where(Log.log_time < cutoff_date)
    )

    logs = tuple(session.scalars(query))

    for log in logs:
        session.delete(log)

    session.commit()

    log_info(orchestrator_connection, f"Logs deleted: {len(logs)}")


def delete_queue_elements(days: int, session: Session, orchestrator_connection: OrchestratorConnection):
    """Delete all queue elements in the database older than the given number of days.

    Args:
        days: The maximum age of queue elements before deletion.
        session: The sqlalchemy session to perform the action.
        orchestrator_connection: The connection to Orchestrator.
    """
    cutoff_date = datetime.today() - timedelta(days=days)

    log_info(orchestrator_connection, f"Deleting queue elements before: {cutoff_date.date()}")

    query = (
        select(QueueElement)
        .where(QueueElement.created_date < cutoff_date)
    )

    queue_elements = tuple(session.scalars(query))

    for queue_element in queue_elements:
        session.delete(queue_element)

    session.commit()

    log_info(orchestrator_connection, f"Queue elements deleted: {len(queue_elements)}")


def anon_queue_reference(days: int, session: Session, orchestrator_connection: OrchestratorConnection):
    """Delete all references on queue elements in the database older than the given number of days.

    Args:
        days: The maximum age of queue elements before deletion.
        session: The sqlalchemy session to perform the action.
        orchestrator_connection: The connection to Orchestrator.
    """
    cutoff_date = datetime.today() - timedelta(days=days)

    log_info(orchestrator_connection, f"Deleting queue references before: {cutoff_date.date()}")

    query = (
        select(QueueElement)
        .where(QueueElement.created_date < cutoff_date)
    )

    queue_elements = session.scalars(query)

    count = 0

    for queue_element in queue_elements:
        if queue_element.reference:
            queue_element.reference = None
            count += 1

    session.commit()

    log_info(orchestrator_connection, f"Queue references deleted: {count}")


def anon_queue_data(days: int, session: Session, orchestrator_connection: OrchestratorConnection):
    """Delete all data on queue elements in the database older than the given number of days.

    Args:
        days: The maximum age of queue elements before deletion.
        session: The sqlalchemy session to perform the action.
        orchestrator_connection: The connection to Orchestrator.
    """
    cutoff_date = datetime.today() - timedelta(days=days)

    log_info(orchestrator_connection, f"Deleting queue data before: {cutoff_date.date()}")

    query = (
        select(QueueElement)
        .where(QueueElement.created_date < cutoff_date)
    )

    queue_elements = session.scalars(query)

    count = 0

    for queue_element in queue_elements:
        if queue_element.data:
            queue_element.data = None
            count += 1

    session.commit()

    log_info(orchestrator_connection, f"Queue data deleted: {count}")


def anon_queue_message(days: int, session: Session, orchestrator_connection: OrchestratorConnection):
    """Delete all messages on queue elements in the database older than the given number of days.

    Args:
        days: The maximum age of queue elements before deletion.
        session: The sqlalchemy session to perform the action.
        orchestrator_connection: The connection to Orchestrator.
    """
    cutoff_date = datetime.today() - timedelta(days=days)

    log_info(orchestrator_connection, f"Deleting queue messages before: {cutoff_date.date()}")

    query = (
        select(QueueElement)
        .where(QueueElement.created_date < cutoff_date)
    )

    queue_elements = session.scalars(query)

    count = 0

    for queue_element in queue_elements:
        if queue_element.message:
            queue_element.message = None
            count += 1

    session.commit()

    log_info(orchestrator_connection, f"Queue messages deleted: {count}")


def log_info(orchestrator_connection: OrchestratorConnection, message: str):
    """Create a log in Orchestrator slowly.
    If logs are created too quickly they will not sort properly in Orchestrator.
    Yes this is stupid, but it's what we have.

    Args:
        orchestrator_connection: The connection to Orchestrator.
        message: The message to log.
    """
    orchestrator_connection.log_info(message)
    time.sleep(0.01)


if __name__ == '__main__':
    main()
