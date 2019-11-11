'use strict'

var fs = require('fs')
var assert = require('assert')

var barrage = require('barrage')

require('./setup')
var npm = require('../')
var downloadGithubTarball = require('../lib/github.js')

var dest = __dirname + '/output/foo.tar.gz'

describe('github', function () {
  // external
  it('downloads archives from github', function (done) {
    npm('npm-fetch', 'ForbesLindesay/npm-fetch', {})
      .pipe(barrage(fs.createWriteStream(dest)))
      .wait(function (err) {
        if (err) return done(err)
        fs.exists(dest, function (exists) {
          assert.ok(exists)
          done()
        })
      })
  })
})