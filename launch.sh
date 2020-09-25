#!/usr/bin/env bash

# params
export ORIGIN_URL=https://github.com/USERNAME/REPO_ORIGIN.git
export DESTINATION_URL=https://github.com/USERNAME/REPO_DESTINATION.git
export BRANCHES_LIST=[branch1,branch2]

docker run -d -it --rm \
-e ORIGIN_URL \
-e DESTINATION_URL \
-e BRANCHES_LIST \
-e UPDATE_PERIOD \
--name git_mirrorer christophebedard/git_mirrorer:latest
