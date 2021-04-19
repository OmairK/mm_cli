import logging as log

from dateutil import parser
from googleapiclient.discovery import build
from sqlalchemy.orm import Query

from g_client.gmail.v1.utils import provide_service
from utils.query_filters import filter_controller
from utils.sessions import provide_session
from models.emails import EMail

log.basicConfig(level=log.DEBUG)  # TODO: remove debug


@provide_session
def store_emails(session, service, message_ids):
    new_mails = 0
    for message_id in message_ids:
        response = (
            service.users()
            .messages()
            .get(userId="me", id=message_id["id"], format="metadata")
            .execute()
        )
        headers = response["payload"]["headers"]
        response = {"message_id": response["id"], "labels": response["labelIds"]}
        for header in headers:
            if header["name"] == "From":
                response["sender"] = header["value"]
            elif header["name"] == "To":
                response["recipient"] = header["value"]
            elif header["name"] == "Subject":
                response["subject"] = header["value"]
            elif header["name"] == "Date":
                response["date"] = parser.parse(header["value"]).date()

        mail = EMail(**response)
        q = session.query(EMail).filter_by(message_id=mail.message_id)
        if not session.query(q.exists()).scalar():
            session.add(mail)
            new_mails += 1
    log.debug(f"{new_mails} new emails added")


def retrieve_emails(creds, labels, max_results):
    """
    Retrieve emails from the gmail api
    """
    service = build("gmail", "v1", credentials=creds)
    include_spam_trash = False
    if "SPAM" in labels or "TRASH" in labels:
        include_spam_trash = True

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=labels,
            maxResults=max_results,
            includeSpamTrash=include_spam_trash,
        )
        .execute()
    )

    message_ids = response.get("messages", [])
    if not message_ids:
        log.debug(f"No new {fetch_label} messages!")
    else:
        log.debug(f"{len(message_ids)} {labels} messages were fetched!")
        store_emails(service=service, message_ids=message_ids)


def process_labels(actions):
    """
    All the actions can be summarized with different labels a
    email carries hence we just have to add/remove a label(s)
    from the email to move/mark an email.
    """
    add_labels = []
    remove_labels = []

    for action in actions:
        if action["action"].upper() == "MOVE":
            add_labels.append(action["value"].upper())
        elif action["action"].upper() == "MARK" and action["value"].upper() == "UNREAD":
            add_labels.append(action["value"].upper())
        elif action["action"].upper() == "MARK" and action["value"].upper() == "READ":
            remove_labels.append("UNREAD")

    return add_labels, remove_labels


def perform_action(creds, rules_json):
    """
    Performs action on the emails stored in the database.
    """
    service = build("gmail", "v1", credentials=creds)
    query_list = []

    for rule in rules_json["rules"]:
        query_list.append(filter_controller(rule))

    if rules_json["rulesRelation"].upper() == "ALL":
        mails = Query.intersect(*query_list).all()
    elif rules_json["rulesRelation"].upper() == "ANY":
        mails = Query.union(*query_list).all()

    add_labels, remove_labels = process_labels(rules_json["actions"])

    for mail in mails:
        response = (
            service.users()
            .messages()
            .modify(
                userId="me",
                id=mail.message_id,
                body={"addLabelIds": add_labels, "removeLabelIds": remove_labels},
            )
            .execute()
        )
        mail.labels = response["labelIds"]
    log.debug(f"Actions performed on {len(mails)} matching emails")
