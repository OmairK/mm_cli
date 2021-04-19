import argparse
import logging as log
import json
import os

from g_client.auth.oauth import authenticate
from configs import gmail_configs, db_configs, gen_configs
from models.emails import Base, engine
from g_client.gmail.v1.helpers import retrieve_emails, perform_action
from models.base import engine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/happy_fox"


def main():

    if not engine.dialect.has_table(engine, "email"):
        Base.metadata.create_all(engine)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--credentialsFile",
        help="google app credentials file needed for generation of oauth token",
        default=gmail_configs.CREDENTIALS_FILE,
    )
    parser.add_argument(
        "--tokenFile",
        help="oauth token file generated from client credentials file",
        default=gmail_configs.AUTH_TOKEN,
    )
    parser.add_argument(
        "--maxResults",
        help="max emails retrieved in a single list request",
        type=int,
        default=gmail_configs.MAX_RESULTS,
    )
    parser.add_argument(
        "--retrieveLabel",
        help="retrieves emails with the specified labels",
        nargs="+",
        type=str,
        default=gmail_configs.RETRIEVE_LABELS,
    )
    parser.add_argument(
        "--rulesFile",
        help="path to the rules file that determines the filters and actions to be performed",
        default=gen_configs.RULES_FILE,
    )

    args = parser.parse_args()
    if args.retrieveLabel:
        retrieve_label = args.retrieveLabel
    if args.maxResults:
        max_results = args.maxResults
    if args.rulesFile:
        rules_file = args.rulesFile

    creds = authenticate(args.tokenFile, args.credentialsFile, gmail_configs.SCOPES)

    with open(rules_file, "r") as rf:
        rules = json.load(rf)

    retrieve_label = [label.upper() for label in retrieve_label]

    retrieve_emails(creds, retrieve_label, max_results)
    perform_action(creds, rules)


if __name__ == "__main__":
    main()
