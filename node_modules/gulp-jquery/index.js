var PLUGIN_NAME = require('./package.json').name;

var extend = require('util')._extend;
var through = require('through2');
var gutil = require('gulp-util');
var PluginError = gutil.PluginError;
var fs = require('fs');
var join = require('path').join;
var builder = require('jquery-custom');

function plugin (opts) {
	var stream = through.obj(function(file, enc, next) {
		if (!file.isNull()) {
			this.emit('error', new PluginError(PLUGIN_NAME, 'Can only operate on directories. You must provide a jquery src folder.'));
			return next();
		}

		var self = this;
		var options = extend({}, opts || {});

		if (file.path) {
			var stats = fs.statSync(file.path);

			if (!stats.isDirectory()) {
				this.emit('error', new PluginError(PLUGIN_NAME, 'Can only operate on directories. You must provide a jquery src folder.'));
				return next();
			}

			if (!fs.existsSync(join(file.path, 'jquery.js'))) {
				this.emit('error', new PluginError(PLUGIN_NAME, 'Could not locate the base jquery.js file in the received directory.'));
				return next();
			}

			options.src = file.path;
		}

		builder(options, function (err, result) {
			if (err) {
				this.emit('error', err);
				return next();
			}

			file.contents = new Buffer(result);
			file.base = '.';
			file.path = join(file.cwd, 'jquery.custom.js');

			self.push(file);
			next();
		});
	});

	stream.src = function () {
		setTimeout(function () {
			var blankFile = new gutil.File();

			stream.write(blankFile);
			stream.end();
		}, 1);
		return stream;
	};

	return stream;
}

module.exports = plugin;

module.exports.src = function () {
	var stream = plugin.apply(null, arguments);
	return stream.src();
}

module.exports._jQuery1Source = function () {
	var base = join(__dirname, '/node_modules/jquery-custom/jquery.1/');
	var filePath = join(base, '/src');

	return new gutil.File({
		cwd: __dirname,
		base: base,
		path: filePath
	});
};

module.exports._jQuery2Source = function () {
	var base = join(__dirname, '/node_modules/jquery-custom/jquery.2/');
	var filePath = join(base, '/src');

	return new gutil.File({
		cwd: __dirname,
		base: base,
		path: filePath
	});
};

module.exports._jQuery3Source = function () {
	var base = join(__dirname, '/node_modules/jquery-custom/jquery.3/');
	var filePath = join(base, '/src');

	return new gutil.File({
		cwd: __dirname,
		base: base,
		path: filePath
	});
};