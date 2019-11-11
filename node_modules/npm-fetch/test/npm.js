'use strict'

var assert = require('assert')
var fs = require('fs')

var barrage = require('barrage')
var RegClient = require('npm-registry-client')

require('./setup.js')
var npm = require('../')
var server = require('./fixtures/testserver.js')
var createServer = server.createServer

var fakeRegistryPort = 1337
var fakeRegistry = 'http://localhost:' + fakeRegistryPort

var dest = __dirname + '/output/foo.tar.gz'
var versionedTarball = 'underscore-1.3.3.tgz'
var tarballSource = __dirname + '/fixtures/' + versionedTarball

var client = new RegClient({
  cache: __dirname + '/output',
  registry: fakeRegistry,
  log: {
    error: noop,
    warn: noop,
    info: noop,
    verbose: noop,
    silly: noop,
    http: noop,
    pause: noop,
    resume: noop
  }
})
function noop() {

}

// mock json response from the registry
// will get a reference patched to our mocked registry
var underscore = require('./fixtures/underscore-res-version.json')
underscore.dist.tarball = fakeRegistry + '/underscore/-/' + versionedTarball

describe('npm', function () {
  describe('npm.tag', function () {
    it('returns an error if the engine does not match', function (done) {
      var underscoreTag = require('./fixtures/underscore-res-tag.json')
      underscoreTag.versions['1.3.3'].engines.node = 'Rockobert'
      var s = createServer(function (req, res) {
        res.statusCode = 200
        return res.end(JSON.stringify(underscoreTag))
      }, function listen () {
        npm('underscore', 'latest', {
          registryClient: client,
          registry: fakeRegistry
        })
        .on('error', function (err) {
            s.close()
            assert.ok(err)
            done()
        })
      })
    })
    it('downloads a tarball with npm.version if dist-tags was found', function (done) {
      var underscoreTag = require('./fixtures/underscore-res-tag.json')
      underscoreTag['dist-tags'] = {
        "latest": "1.3.3"
      }
      var s = createServer(function (req, res) {
        res.statusCode = 200
        if (req.url === '/underscore/-/' + versionedTarball) {
          // third request: send tarball
          var readStream = fs.createReadStream(tarballSource)
          readStream.on('end', function () {
            s.close()
          })
          readStream.pipe(res)
        } else if (req.url === '/underscore/1.3.3') {
          // second request
          return res.end(JSON.stringify(underscore))
        } else {
          // first request
          return res.end(JSON.stringify(underscoreTag))
        }
      }, function listen () {
        npm('underscore', 'latest', {
          registryClient: client,
          registry: fakeRegistry,
          force: true
        })
        .syphon(barrage(fs.createWriteStream(dest)))
        .wait(function (err) {
          assert.ok(fs.existsSync(dest))
          done()
        })
      })
    })
  })
  describe('npm.version', function () {
    it('downloads underscore 1.3.3', function (done) {
      var s = createServer(function (req, res) {
          res.statusCode = 200
          // first request
          if (req.url !== '/underscore/-/' + versionedTarball) {
            return res.end(JSON.stringify(underscore))
          }
          // send tarball
          var readStream = fs.createReadStream(tarballSource)
          readStream.on('end', function () {
            s.close()
          })
          readStream.pipe(res)
      }, function listen () {
        npm('underscore', '1.3.3', {
          registryClient: client,
          registry: fakeRegistry
        })
        .syphon(barrage(fs.createWriteStream(dest)))
        .wait(function (err) {
          assert.ok(fs.existsSync(dest))
          done()
        })
      })
    })
    it('returns an error if no shasum is defined', function (done) {
      var s = createServer(function (req, res) {
          res.statusCode = 200
          // first request but the package has no shasum
          var u = JSON.parse(JSON.stringify(underscore))
          u.dist.shasum = null
          res.end(JSON.stringify(u))
          s.close()
      }, function listen () {
          npm('underscore', '1.3.3', {
            registryClient: client,
            registry: fakeRegistry
          })
          .on('error', function (err) {
            assert.ok(err)
            assert.ok(/shasum/.test(err.message))
            done()
          })
      })
    })
  })
  describe('npm.range', function () {
    it('downloads underscore ~1.3.3 when thats the latest', function (done) {
      var s = createServer(function (req, res) {
          res.statusCode = 200
          // first request
          if (req.url === '/underscore') {
            return res.end(JSON.stringify({
              'dist-tags': {'latest': '1.3.3'},
              'versions' : {'1.3.3' : {}}
            }))
          }
          //second request
          if (req.url !== '/underscore/-/' + versionedTarball) {
            return res.end(JSON.stringify(underscore))
          }
          // send tarball
          var readStream = fs.createReadStream(tarballSource)
          readStream.on('end', function () {
            s.close()
          })
          readStream.pipe(res)
      }, function listen () {
        npm('underscore', '~1.3.3', {
          registryClient: client,
          registry: fakeRegistry
        })
        .syphon(barrage(fs.createWriteStream(dest)))
        .wait(function (err) {
          assert.ok(fs.existsSync(dest))
          done()
        })
      })
    })
    it('downloads underscore ~1.3.3 even when that isnt the latest', function (done) {
      var s = createServer(function (req, res) {
          res.statusCode = 200
          // first request
          if (req.url === '/underscore') {
            return res.end(JSON.stringify({
              'dist-tags': {'latest': '1.5.0'},
              'versions' : {'1.3.3' : {}, '1.5.0' : {}}
            }))
          }
          //second request
          if (req.url !== '/underscore/-/' + versionedTarball) {
            return res.end(JSON.stringify(underscore))
          }
          // send tarball
          var readStream = fs.createReadStream(tarballSource)
          readStream.on('end', function () {
            s.close()
          })
          readStream.pipe(res)
      }, function listen () {
        npm('underscore', '~1.3.3', {
          registryClient: client,
          registry: fakeRegistry
        })
        .syphon(barrage(fs.createWriteStream(dest)))
        .wait(function (err) {
          assert.ok(fs.existsSync(dest))
          done()
        })
      })
    })
  })
})