#!/usr/bin/env python

## Script for mirroring git remotes
# Make sure to set the appropriate environment variables:
#   ORIGIN_URL:       remote url of the origin repo
#   DESTINATION_URL:  remote url of the destination repo
#   BRANCHES_LIST:    [branch1,branch2,branch3]

import os
import sys
import time
from git import Repo

from_repo_url = os.environ['ORIGIN_URL']
to_repo_url = os.environ['DESTINATION_URL']
branches_list = os.environ['BRANCHES_LIST']


def extract_branches(branches_list):
    # assuming [a,b,c,d]
    return branches_list[1:-1].split(',')


def update(remote, branches):
    for branch in branches:
        print('pushing %s' % branch)
        remote.push('origin/%s:refs/heads/%s' % (branch, branch))


def launch():
    branches = extract_branches(branches_list)
    print('will mirror branches: ', branches)

    # init repo (we do not actually need to keep an updated clone)
    print('cloning origin repo..')
    repo = Repo.clone_from(from_repo_url, 'repo_dir')
    print('adding destination remote..')
    to_remote = repo.create_remote('to_remote', url=to_repo_url)

    while (True):
        print("update..")
        update(to_remote, branches)
        time.sleep(1)


if __name__ == '__main__':
    launch()
