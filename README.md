# git_mirrorer

Mirrors two git remotes

(alternate description: containerize everything!)

## How to use

Whether you use a container or call the Python script directly, set the following parameters as environment variables:

* `ORIGIN_URL`: remote URL of the origin repo
* `DESTINATION_URL`: remote URL of the destination repo
* `BRANCHES_LIST`: list of branches to update, e.g. [branch1,branch2,branch3]
* `UPDATE_PERIOD`: delay between updates (seconds) [default: 60]
