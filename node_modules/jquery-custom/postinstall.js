
var range = require('npm-fetch').npm.range;
var tar = require('tar');
var zlib = require('zlib');
var path = require('path');

function fetch (pkg, ver, dest, callback) {
	range(pkg, ver)
		.pipe(zlib.Unzip())
		.pipe(tar.Extract({ path: dest, strip: 1 }))
		.on('error', function (err) { callback(err); })
		.on('end', function () { callback(); });
}

fetch('jquery', '<1.12', path.resolve(__dirname, './jquery.1'), dlfinished);
fetch('jquery', '<2.2', path.resolve(__dirname, './jquery.2'), dlfinished);
// fetch('jquery', '3', path.resolve(__dirname, './jquery.3'), dlfinished);




var total = 3;
function dlfinished (err) {
	if (err) {
		console.error(err);
		process.exit(-1);
	}
	total--;

	if (total < 1) {
		process.exit(0);
	}
}