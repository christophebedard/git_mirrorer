#!/usr/bin/env python

## Script for mirroring (remote) git repos
# Make sure to set the appropriate environment variables
# Also, pass the branches you want to be mirrored as params

import os
import sys
import time
import email
from imapclient import IMAPClient
from git import Repo

host = os.environ['EMAIL_HOST']
port = int(os.environ['EMAIL_PORT'])
username = os.environ['EMAIL']
password = os.environ['EMAIL_PASS']
folder = os.environ['EMAIL_FOLDER']
from_repo_url = os.environ['ORIGIN_URL']
to_repo_url = os.environ['DESTINATION_URL']
branches = sys.argv[1:]


def get_server():
    server = IMAPClient(host, use_uid=True)
    server.login(username, password)
    return server


def get_msgids_and_data():
    server = get_server()
    select_info = server.select_folder(folder)

    # not necessary right now, since all email in folder were filtered first
    msgs = server.search(['FROM', 'action@ifttt.com'])

    fetch_result = server.fetch(msgs, 'RFC822')
    ids = list(fetch_result.keys())

    server.logout()

    return ids, fetch_result


def get_latest_id():
    ids, _ = get_msgids_and_data()
    return max(ids)


def process_new_email(remote):
    for branch in branches:
        print('pushing %s' % branch)
        remote.push('origin/%s:refs/heads/%s' % (branch, branch))


def launch():
    # init repo (we do not actually need to keep an updated clone)
    print('cloning origin repo..')
    repo = Repo.clone_from(from_repo_url, 'repo_dir')
    print('adding destination remote..')
    to_remote = repo.create_remote('to_remote', url=to_repo_url)

    # get id of latest email
    print('getting latest email..')
    last_id = get_latest_id()

    while (True):
        print("fetching emails..")

        # get all emails
        ids, data = get_msgids_and_data()

        for id in ids:
            # check if new
            if id > last_id:
                process_new_email(to_remote)
                last_id = id
        
        time.sleep(1)


if __name__ == '__main__':
    launch()
