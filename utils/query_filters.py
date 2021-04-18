from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy import not_

from models.emails import EMail
from utils.sessions import provide_session




@provide_session
def date_filter(session, rule):
    """
    Filter messages based on predicate
    specified on 'date' field
    -----------------------------------
    arguments:
        - s: sqlalchemy session object
        - rule: rule dictionary for this field
    """
    if rule['predicate'].upper() == 'LESS THAN DAYS':
        end_date = date.today()
        start_date = end_date - relativedelta(days=rule['value'])
        q = s.query(Message).filter(
            Message.date.between(start_date, end_date)
        )
    elif rule['predicate'].upper() == 'GREATER THAN DAYS':
        filter_date = date.today() - relativedelta(days=rule['value'])
        q = s.query(Message).filter(
            Message.date <= filter_date
        )
    elif rule['predicate'].upper() == 'LESS THAN MONTHS':
        end_date = date.today()
        start_date = end_date - relativedelta(months=rule['value'])
        q = s.query(Message).filter(
            Message.date.between(start_date, end_date)
        )
    elif rule['predicate'].upper() == 'GREATER THAN MONTHS':
        filter_date = date.today() - relativedelta(days=rule['value'])
        q = s.query(Message).filter(
            Message.date <= filter_date
        )
    return q

@provide_session
def recipient_filter(session, rule):
    """
    Filters messages based on predicate
    specified on 'from' field
    -----------------------------------
    arguments:
        - s: sqlalchemy session object
        - rule: rule dictionary for this field
    """
    if rule['predicate'].upper() == 'EQUAL':
        q = s.query(Message).filter(
            Message.sender==rule['value']
        )
    elif rule['predicate'].upper() == 'CONTAINS':
        q = s.query(Message).filter(
            Message.sender.contains(rule['value'])
        )
    elif rule['predicate'].upper() == 'NOT EQUAL':
        q = s.query(Message).filter(
            Message.sender!=rule['value']
        )
    elif rule['predicate'].upper() == 'DOES NOT CONTAIN':
        q = s.query(Message).filter(
            not_(Message.sender.contains(rule['value']))
        )
    return q

@provide_session
def subject_filter(session, rule):
    """
    Filters messages based on predicate
    specified on 'subject' field
    ------------------------------------
    arguments:
        - s: sqlalchemy session object
        - rule: rule dictionary for this field
    """
    if rule['predicate'].upper() == 'EQUAL':
        q = s.query(Message).filter(
            Message.subject==rule['value']
        )
    elif rule['predicate'].upper() == 'CONTAINS':
        q = s.query(Message).filter(
            Message.subject.contains(rule['value'])
        )
    elif rule['predicate'].upper() == 'NOT EQUAL':
        q = s.query(Message).filter(
            Message.subject!=rule['value']
        )
    elif rule['predicate'].upper() == 'DOES NOT CONTAIN':
        q = s.query(Message).filter(
            not_(Message.subject.contains(rule['value']))
        )
    return q


def filter_controller(rule):
    for rule in rules['rules']:
        if rule['field'].upper() == 'FROM':
            q = sender_filter(session, rule)
        elif rule['field'].upper() == 'SUBJECT':
            q = subject_filter(session, rule)
        elif rule['field'].upper() == 'DATE':
            q = date_filter(session, rule)
    return q
