#!/usr/bin/env python

## Script for mirroring git remotes
# Make sure to set the appropriate environment variables:
#   ORIGIN_URL:       remote URL of the origin repo
#   DESTINATION_URL:  remote URL of the destination repo
#   BRANCHES_LIST:    list of branches to update, e.g. [branch1,branch2,branch3]
#   UPDATE_PERIOD:    delay between updates (seconds) [default: 60]

import os
import sys
import time
from git import Repo

from_repo_url = os.environ['ORIGIN_URL']
to_repo_url = os.environ['DESTINATION_URL']
branches_list = os.environ['BRANCHES_LIST']
update_period = int(os.getenv('UPDATE_PERIOD', 60))


def extract_branches(branches_list):
    # assuming [a,b,c,d]
    return branches_list[1:-1].split(',')


def get_last_commits(remote, branches):
    last_commits = {}
    for branch in branches:
        fetch_info = remote.fetch(branch)[0]
        last_commits[branch] = fetch_info.commit.hexsha
    return last_commits


def update(remote, branch):
    print('pushing %s!' % branch)
    remote.push('origin/%s:refs/heads/%s' % (branch, branch))


def launch():
    print('will update every:', update_period)

    branches = extract_branches(branches_list)
    print('will mirror branches:', branches)

    # init repo (we do not actually need to keep an updated clone)
    print('cloning origin repo..')
    repo = Repo.clone_from(from_repo_url, 'repo_dir')
    print('adding destination remote..')
    to_remote = repo.create_remote('to_remote', url=to_repo_url)

    # fetch last commit of each branch
    last_commits = get_last_commits(repo.remotes.origin, branches)
    print('latest commits:', last_commits)
    
    # force the first update
    for branch in branches:
        update(to_remote, branch)

    while (True):
        print('checking..')

        # fetch last commit of each branch
        last_commits_check = get_last_commits(repo.remotes.origin, branches)

        for branch in branches:
            # if commit changed, update
            if last_commits[branch] != last_commits_check[branch]:
                print('%s changed!' % branch)
                update(to_remote, branch)
                last_commits[branch] = last_commits_check[branch]

        time.sleep(update_period)


if __name__ == '__main__':
    launch()
