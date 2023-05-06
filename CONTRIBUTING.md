# Contributing

As all good free software projects, you can fork this repo and change the software to you conveniance.
If you think your modification can benefit to other users, please open a pull request explaining the changes in details
(*that way I don't have to guess what you were trying to do*).

## Bugs, errors and other fun things

Because I am not a machine (yet), there is probably bugs everywhere. If you find one, please open an issue.

## Security

If you find a security problem, please email me at *slashformotion [at] protonmail [dot] com*.

### How to release

We use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as guideline for the version management.

Steps to release:

- Create a new branch labeled `release/vX.Y.Z` from the latest `main`.
- Improve the version number in `changelog.md`.
- Verify the content of the `changelog.md`.
- Commit the modifications with the label `Release version vX.Y.Z`.
- Create a pull request on github for this branch into `main`.
- Once the pull request validated and merged, tag the `main` branch with `vX.Y.Z`
- After the tag is pushed, make the release on the tag in GitHub

### Git: Default branch

The default branch is master. Direct commit on it is forbidden. The only way to update the application is through pull request.

Release tag are only done on the `master` branch.
