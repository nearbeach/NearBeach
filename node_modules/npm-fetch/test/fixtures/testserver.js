var http = require('http')

exports.host = 'http://localhost'
exports.port = 1337

exports.createServer = createServer


// basic testserver
function createServer(plugin, test, host, port) {
  var port = port || exports.port
  var host = host || exports.host

  var server = http.createServer(plugin)
    .listen(port, test)

  return server
}

