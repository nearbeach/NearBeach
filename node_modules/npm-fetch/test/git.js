'use strict'

var fs = require('fs')
var assert = require('assert')

var barrage = require('barrage')

var npm = require('../')

var dest = __dirname + '/output/foo.tar.gz'

describe('git', function () {
  // external
  it('downloads archives directly from github', function (done) {
    npm('name', 'git+ssh://git@github.com:ForbesLindesay/npm-fetch.git', {})
      .syphon(barrage(fs.createWriteStream(dest)))
      .wait(function (err) {
        if (err) return done(err)
        fs.exists(dest, function (exists) {
          assert.ok(exists)
          done()
        })
      })
  })
})