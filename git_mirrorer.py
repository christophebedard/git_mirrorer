#!/usr/bin/env python
"""
Script for mirroring git remotes.

Make sure to set the appropriate environment variables:
  ORIGIN_URL:       remote URL of the origin repo
  DESTINATION_URL:  remote URL of the destination repo
  BRANCHES_LIST:    list of branches to update, e.g. [branch1,branch2,branch3]
  UPDATE_PERIOD:    delay between updates (seconds) [default: 60]
"""

import os
import shutil
import time
from typing import Dict
from typing import List

import git


from_repo_url = os.environ['ORIGIN_URL']
to_repo_url = os.environ['DESTINATION_URL']
branches_list = os.environ['BRANCHES_LIST']
update_period = int(os.getenv('UPDATE_PERIOD', 60))


def extract_branches(branches_list: str) -> List[str]:
    """Extract branches list from string representation."""
    # Assuming [a,b,c,d]
    return branches_list[1:-1].split(',')


def delete_directory_if_exists(directory: str) -> None:
    """Delete the directory if it exists."""
    if os.path.isdir(directory):
        print(f'deleting directory: {directory}')
        shutil.rmtree(directory)


def get_last_commits(remote: git.Remote, branches: List[str]) -> Dict[str, str]:
    """Get last commit of each given branch for the given remote."""
    last_commits = {}
    for branch in branches:
        fetch_info = remote.fetch(branch)[0]
        last_commits[branch] = fetch_info.commit.hexsha
    return last_commits


def update(remote: git.Remote, branch: str) -> None:
    """Update given remote by pushing the given branch."""
    print(f'pushing {branch}!')
    remote.push(f'origin/{branch}:refs/heads/{branch}')


def launch(repo_directory: str = 'repo_dir') -> None:
    """Launch and run."""
    print('will update every:', update_period)

    branches = extract_branches(branches_list)
    print('will mirror branches:', branches)

    # Init repo (we do not actually need to keep an updated clone)
    delete_directory_if_exists(repo_directory)
    print('cloning origin repo..')
    repo = git.Repo.clone_from(from_repo_url, repo_directory)
    print('adding destination remote..')
    to_remote = repo.create_remote('to_remote', url=to_repo_url)

    # Fetch last commit of each branch
    last_commits = get_last_commits(repo.remotes.origin, branches)
    print('latest commits:', last_commits)

    # Force the first update
    for branch in branches:
        update(to_remote, branch)

    while (True):
        print('checking..')

        # Fetch last commit of each branch
        last_commits_check = get_last_commits(repo.remotes.origin, branches)

        for branch in branches:
            # If commit changed, update
            if last_commits[branch] != last_commits_check[branch]:
                print((
                    f'{branch} changed from <{last_commits[branch]}> '
                    'to <{last_commits_check[branch]}>!'
                ))
                update(to_remote, branch)
                last_commits[branch] = last_commits_check[branch]

        time.sleep(update_period)


if __name__ == '__main__':
    launch()
