'use strict'

var path = require('path')
var url = require('url')
var fs = require('fs')
var PassThrough = require('barrage').PassThrough

exports = (module.exports = fetch)

exports.tarball = require('./lib/tarball')
exports.npm = require('./lib/npm')
exports.local = require('./lib/local')
exports.github = require('./lib/github')
exports.git = require('./lib/git')

//pkg must be one of:
//
//['pkg', 'version']
//['pkg', 'url']
//['pkg', 'local-path']
//['pkg', 'git/hub#specifier']
//
// This is tricky, because urls can contain @
// Also, in some cases we get [name, null] rather
// that just a single argument.

function fetch(name, spec, options) {
  if (typeof spec === 'object' && options === undefined) {
    options = spec
    spec = undefined
  }
  spec = spec || '*'

  var p = url.parse(spec) || {}

  switch (p.protocol) {
    case 'http:':
    case 'https:':
      return exports.tarball(name, spec, options)
    case "git:":
    case "git+http:":
    case "git+https:":
    case "git+rsync:":
    case "git+ftp:":
    case "git+ssh:":
      return exports.git(name, spec, options)
    default:
      var result = new PassThrough()
      fs.stat(spec, function (err, stat) {
        if (err === null && stat.isDirectory()) {
          exports.local.dir(name, spec, options)
            .on('end', result.end.bind(result))
            .syphon(result)
        } else if (err === null && stat.isFile()) {
          exports.local.file(name, spec, options)
            .on('end', result.end.bind(result))
            .syphon(result)
        } else if (/^([^\/]+)\/([^\/#]+)(?:#(.+))?$/.test(spec)) {
          exports.github(name, spec, options)
            .on('end', result.end.bind(result))
            .syphon(result)
        } else {
          exports.npm(name, spec, options)
            .on('end', result.end.bind(result))
            .syphon(result)
        }
      })
      return result
  }
}
