'use strict'

var assert = require('assert')
var fs = require('fs')

var barrage = require('barrage')
var sha = require('sha')

require('./setup')
var npm = require('../')

var tarball = __dirname + '/output/foo.tar.gz'

describe('local', function () {
  describe('local.dir', function () {
    it('it returns a stream for a tarball', function (done) {
      var input = __dirname + '/fixtures/npm-user-validate'
      npm('name', input, {})
        .syphon(barrage(fs.createWriteStream(tarball)))
        .wait(done)
    })
    it('returns an error if package.json is missing a version', function (done) {
      var input = __dirname + '/fixtures/package-json-version-missing'
      npm('name', input, {})
      .on('error', function (err) {
        assert.ok(err)
        assert.ok(/version/.test(err.message))
        done()
      })
    })
    it('returns an error if package.json is missing a name', function (done) {
      var input = __dirname + '/fixtures/package-json-name-missing'
      npm('name', input, {})
      .on('error', function (err) {
        assert.ok(err)
        assert.ok(/name/.test(err.message))
        done()
      })
    })
  })
  describe('local.file', function () {
    it('returns a stream for a tarball', function (done) {
      var input = __dirname + '/fixtures/npm-fetch-master.tar.gz'
      npm('name', input, {})
      .syphon(barrage(fs.createWriteStream(tarball)))
      .wait(function (err) {
        if (err) return done(err)
        sha.get(input, function (err, hash) {
          if (err) return done(err)
          sha.check(tarball, hash, function (err) {
            if (err) return done(err)
            else done()
          })
        })
      })
    })
  })
})