'use strict'

var fs = require('fs')
var assert = require('assert')

var barrage = require('barrage')

require('./setup')
var downloadRemoteTarball = require('../lib/tarball.js')

var dest = __dirname + '/output/foo.tar.gz'

var mr = require('npm-registry-mock')
var strongClient = require('strong-caching-http-client')
// config
var port = 1331
var address = 'http://localhost:' + port

var pkg = '/underscore/-/underscore-1.3.3.tgz'
var tb = address + pkg

describe('tarball', function () {
  describe('downloadRemoteTarball', function () {
    it('returns an error if the checked sha-sum does not match', function (done) {
      mr(port, function (s) {
        downloadRemoteTarball('name', tb, {shasum: '1'})
          .on('error', function (err) {
            assert.ok(err)
            s.close()
            done()
          })
          .pipe(fs.createWriteStream(dest))
      })
    })
    it('downloads files and calls a callback', function (done) {
      mr(port, function (s) {
        downloadRemoteTarball('name', tb)
          .syphon(barrage(fs.createWriteStream(dest)))
          .wait(function (err) {
            if (err) return done(err)
            fs.exists(dest, function (exists) {
              assert.ok(exists)
              s.close()
              done()
            })
          })
      })
    })
    it('retries if a http 500 status code was given back and succeeds if it then works', function (done) {
      function plugin(s) {
        s.get(pkg).reply(500, {'data': 'true'})
        s.get(pkg).reply(500, {'rockmeister': 'true'})
        s.get(pkg).reply(200, {'lala': 'true'})
      }
      var times = 0
      mr({port: port, mocks: plugin}, function (s) {
        downloadRemoteTarball('name', tb, {retries: 4})
          .syphon(barrage(fs.createWriteStream(dest)))
          .wait(function () {
            s.close()
            done()
          })
      })
    })
    it('if a http 500 status code was given back an error is emitted', function (done) {
      var customMocks = {
        'get': {
          '/underscore/-/underscore-1.3.3': [500, {}]
        }
      }
      mr({port: port, mocks: customMocks}, function (s) {
        downloadRemoteTarball('name', '/underscore/-/underscore-1.3.3', {retries: 1})
          .on('error', function (err) {
            assert.ok(err)
            s.close()
            done()
          })
      })
    })
    it('is able to use other http-clients, e.g. the strong-caching-http-client', function (done) {
      mr(port, function (s) {
        downloadRemoteTarball('name', tb, {httpClient: strongClient.request, cache: __dirname + '/output/', method: 'GET'})
          .syphon(barrage(fs.createWriteStream(dest)))
          .wait(function (err) {
            if (err) return done(err)
            fs.exists(dest, function (exists) {
              assert.ok(exists)
              s.close()
              done()
            })
          })
      })
    })
  })
})