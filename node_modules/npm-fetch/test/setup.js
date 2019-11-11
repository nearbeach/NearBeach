'use strict'

var mkdir = retry(require('mkdirp'))
var rimraf = retry(require('rimraf'))

beforeEach(function (callback) {
  rimraf(__dirname + '/output/', function (err) {
    if (err) return callback(err)
    mkdir(__dirname + '/output/', callback)
  })
})
afterEach(function (callback) {
  rimraf(__dirname + '/output/', callback)
})

function retry(fn) {
  return function () {
    var args = Array.prototype.slice.call(arguments)
    var cb = args.pop()
    var attemptNo = 0
    function attempt() {
      fn.apply(null, args.concat([function (err, res) {
        if (err && 4 > attemptNo++) {
          return setTimeout(attempt, 100)
        }
        cb(err, res)
      }]))
    }
    attempt()
  }
}