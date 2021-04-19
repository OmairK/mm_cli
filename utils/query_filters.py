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
        q = session.query(EMail).filter(
            EMail.date.between(start_date, end_date)
        )
    elif rule['predicate'].upper() == 'GREATER THAN DAYS':
        filter_date = date.today() - relativedelta(days=rule['value'])
        q = session.query(EMail).filter(
            EMail.date <= filter_date
        )
    elif rule['predicate'].upper() == 'LESS THAN MONTHS':
        end_date = date.today()
        start_date = end_date - relativedelta(months=rule['value'])
        q = session.query(EMail).filter(
            EMail.date.between(start_date, end_date)
        )
    elif rule['predicate'].upper() == 'GREATER THAN MONTHS':
        filter_date = date.today() - relativedelta(days=rule['value'])
        q = session.query(EMail).filter(
            EMail.date <= filter_date
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
        q = session.query(EMail).filter(
            EMail.sender==rule['value']
        )
    elif rule['predicate'].upper() == 'CONTAINS':
        q = session.query(EMail).filter(
            EMail.sender.contains(rule['value'])
        )
    elif rule['predicate'].upper() == 'NOT EQUAL':
        q = session.query(EMail).filter(
            EMail.sender!=rule['value']
        )
    elif rule['predicate'].upper() == 'DOES NOT CONTAIN':
        q = session.query(EMail).filter(
            not_(EMail.sender.contains(rule['value']))
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
        q = session.query(EMail).filter(
            EMail.subject==rule['value']
        )
    elif rule['predicate'].upper() == 'CONTAINS':
        q = session.query(EMail).filter(
            EMail.subject.contains(rule['value'])
        )
    elif rule['predicate'].upper() == 'NOT EQUAL':
        q = session.query(EMail).filter(
            EMail.subject!=rule['value']
        )
    elif rule['predicate'].upper() == 'DOES NOT CONTAIN':
        q = session.query(EMail).filter(
            not_(EMail.subject.contains(rule['value']))
        )
    return q


def filter_controller(rule):
    if rule['field'].upper() == 'FROM':
        q = recipient_filter(rule=rule)
    elif rule['field'].upper() == 'SUBJECT':
        q = subject_filter(rule=rule)
    elif rule['field'].upper() == 'DATE':
        q = date_filter(rule=rule)
    return q
