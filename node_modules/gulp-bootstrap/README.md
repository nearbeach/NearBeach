# gulp-bootstrap
works with gulp, but does nothing. Use it to bootstrap your own gulp plugin with TypeScript.

### Buildstatus/Dependencies
[![Build Status](https://travis-ci.org/pushrocks/gulp-bootstrap.svg?branch=master)](https://travis-ci.org/pushrocks/gulp-bootstrap)
[![devDependency Status](https://david-dm.org/pushrocks/gulp-bootstrap/dev-status.svg)](https://david-dm.org/pushrocks/gulp-bootstrap#info=devDependencies)
[![bitHound Score](https://www.bithound.io/github/pushrocks/gulp-bootstrap/badges/score.svg)](https://www.bithound.io/github/pushrocks/gulp-bootstrap)
[![bitHound Dependencies](https://www.bithound.io/github/pushrocks/gulp-bootstrap/badges/dependencies.svg)](https://www.bithound.io/github/pushrocks/gulp-bootstrap/master/dependencies/npm)
[![Coverage Status](https://coveralls.io/repos/github/pushrocks/gulp-bootstrap/badge.svg?branch=master)](https://coveralls.io/github/pushrocks/gulp-bootstrap?branch=master)

### Usage
This npm package comes with everything you need to start your own gulp plugin.

Features:

* TypeScript: Code your plugin in TypeScript
* Use npmts to
  * compile TypeScript
  * run mocha tests
  * get coverage with istanbul
  * create declaration files for TypeScript module support

This package only has 1 dev-dependency: npmts-g. It searches for npmts globally and tests the version.
If for any reason the npmts global dependency is not fullfilled it'll try to install npmts locally

