# typings-global
@types/node in the right version

## Availabililty
[![npm](https://pushrocks.gitlab.io/assets/repo-button-npm.svg)](https://www.npmjs.com/package/typings-global)
[![git](https://pushrocks.gitlab.io/assets/repo-button-git.svg)](https://GitLab.com/pushrocks/typings-global)
[![git](https://pushrocks.gitlab.io/assets/repo-button-mirror.svg)](https://github.com/pushrocks/typings-global)
[![docs](https://pushrocks.gitlab.io/assets/repo-button-docs.svg)](https://pushrocks.gitlab.io/typings-global/)

## Status for master
[![build status](https://GitLab.com/pushrocks/typings-global/badges/master/build.svg)](https://GitLab.com/pushrocks/typings-global/commits/master)
[![coverage report](https://GitLab.com/pushrocks/typings-global/badges/master/coverage.svg)](https://GitLab.com/pushrocks/typings-global/commits/master)
[![npm downloads per month](https://img.shields.io/npm/dm/typings-global.svg)](https://www.npmjs.com/package/typings-global)
[![Dependency Status](https://david-dm.org/pushrocks/typings-global.svg)](https://david-dm.org/pushrocks/typings-global)
[![bitHound Dependencies](https://www.bithound.io/github/pushrocks/typings-global/badges/dependencies.svg)](https://www.bithound.io/github/pushrocks/typings-global/master/dependencies/npm)
[![bitHound Code](https://www.bithound.io/github/pushrocks/typings-global/badges/code.svg)](https://www.bithound.io/github/pushrocks/typings-global)
[![TypeScript](https://img.shields.io/badge/TypeScript-2.x-blue.svg)](https://nodejs.org/dist/latest-v6.x/docs/api/)
[![node](https://img.shields.io/badge/node->=%206.x.x-blue.svg)](https://nodejs.org/dist/latest-v6.x/docs/api/)
[![JavaScript Style Guide](https://img.shields.io/badge/code%20style-standard-brightgreen.svg)](http://standardjs.com/)

## Important: NodeJS Version Support
Since recently some issues have come up regarding version support:

This package makes sure that @types/node is installed in the right version when installing a module that depends on node. Since node changes dynamically over time, this package does **NOT follow semver**. But instead will follow the node LTS schedule.

That means that current LTS versions will always be supported. To get installs working on versions earlier than current LTS, you can lock the typings-global package on your own.

## Usage
Use TypeScript for best in class instellisense.

checks your node version during installation and then installs the best matching @types/node version

To install type

```shell
npm install --save typings-global
```

To gain node instellisense in your project simply type

```typescript
import "typings-global"
``` 

You can then import any node core modules like `path` or `crypto` with intellisense working.

For further information read the linked docs at the top of this README.

> MIT licensed | **&copy;** [Lossless GmbH](https://lossless.gmbh)
| By using this npm module you agree to our [privacy policy](https://lossless.gmbH/privacy.html)

[![repo-footer](https://pushrocks.gitlab.io/assets/repo-footer.svg)](https://push.rocks)
