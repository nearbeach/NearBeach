.. _git-flow:

========
Git Flow
========

NearBeach uses Git flow for it's development cycle.

Learning Resources:

* `Github Documentation of Git Flow <https://docs.github.com/en/get-started/using-github/github-flow>`_
* `Atlassian Documentation of Git Flow <https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow>`_
* `Git Flow cheat sheet by Daniel Kummer <https://danielkummer.github.io/git-flow-cheatsheet/>`_

Branch Names:

+--------------------+--------------------------+
| Git Default Branch | Branch Name In NearBeach |
+--------------------+--------------------------+
| Master/Main        | main                     |
+--------------------+--------------------------+
| Develop            | develop                  |
|                    |                          |
+--------------------+--------------------------+
| Feature            | feature                  |
+--------------------+--------------------------+
| Release            | release                  |
+--------------------+--------------------------+
| Hotfix             | hotfix                   |
+--------------------+--------------------------+

Notes:

* Any new features, should have the feature created from the `develop` branch
* Any new hotfixes, should have the hotfix created from the `main` branch
* Any new releases, will automatically trigger the github actions, and preform a release
* If releasing new code, the release should be created from the `develop` branch
* If releasing separate from development, i.e. deploying same code base with updated libraries, then follow the
  deployment instructions.