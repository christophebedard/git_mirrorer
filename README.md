# git_mirrorer

Mirror two git remotes

(alternate description: containerize everything!)

## What it does

It periodically fetches an `origin` repo. If the last commit of a branch on the watchlist changed, it pushes that branch to the `destination`. It does not need to checkout or pull everything locally.

## How to use

Whether you use a container or call the Python script directly, set the following parameters as environment variables:

* `ORIGIN_URL`: remote URL of the origin repo
* `DESTINATION_URL`: remote URL of the destination repo
* `BRANCHES_LIST`: list of branches to update, e.g. [branch1,branch2,branch3]
* `UPDATE_PERIOD`: delay between updates (seconds) [default: 60]

## Authentication

This currently expects one-time authentication methods in the remote URL itself. It does not currently use `GIT_ASKPASS`.

* [tokens on GitHub](https://developer.github.com/v3/auth/#via-oauth-tokens) (e.g. remote URL: `https://<token>@github.com/<username>/<repo>.git`)
* username/password authentication over HTTPS (e.g. remote URL: `https://<username>:<password>@github.com/<username>/<repo>.git`) or SSH
