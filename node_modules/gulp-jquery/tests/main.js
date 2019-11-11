
var GJQ = require('../');
var gutil = require('gulp-util');
var builder = require('jquery-custom');


exports['default run from internal jquery.2 source path'] = function (test) {
	var file = GJQ._jQuery2Source();

	var src = file.path;
	var expected;

	var stream = GJQ();
	stream.on('data', function (file) {
		test.equal(file.path, process.cwd() + '/jquery.custom.js');
		test.ok(file.isBuffer());
		test.equal(file.contents.toString(), expected);

		test.done();
	});
	stream.on('error', function (err) {
		test.ok(false, 'Triggered an error');
		test.done();
	});

	builder({src: src}, function (err, contents) {
		if (err) {
			test.ok(false, 'builder threw an error creating fixture data');
			test.done();
			return;
		}

		expected = contents;
		stream.write(file);
	});

};

exports['stream.src with defaults'] = function (test) {
	builder(function (err, expected) {
		if (err) {
			test.ok(false, 'builder threw an error creating fixture data');
			test.done();
			return;
		}


		var stream = GJQ().src();
		stream.on('data', function (file) {
			test.equal(file.path, process.cwd() + '/jquery.custom.js');
			test.ok(file.isBuffer());
			test.equal(file.contents.toString(), expected);

			test.done();
		});
		stream.on('error', function (err) {
			console.error(e);
			test.ok(false, 'Triggered an error');
			test.done();
		});

	});

};

exports['stream.src with release 1'] = function (test) {
	builder({release: 1}, function (err, expected) {
		if (err) {
			test.ok(false, 'builder threw an error creating fixture data');
			test.done();
			return;
		}


		var stream = GJQ({release: 1}).src();
		stream.on('data', function (file) {
			test.equal(file.path, process.cwd() + '/jquery.custom.js');
			test.ok(file.isBuffer());
			test.equal(file.contents.toString(), expected);

			test.done();
		});
		stream.on('error', function (err) {
			console.error(e);
			test.ok(false, 'Triggered an error');
			test.done();
		});

	});

};

exports['GJQ.src with release 1'] = function (test) {
	builder({release: 1}, function (err, expected) {
		if (err) {
			test.ok(false, 'builder threw an error creating fixture data');
			test.done();
			return;
		}


		var stream = GJQ.src({release: 1});
		stream.on('data', function (file) {
			test.equal(file.path, process.cwd() + '/jquery.custom.js');
			test.ok(file.isBuffer());
			test.equal(file.contents.toString(), expected);

			test.done();
		});
		stream.on('error', function (err) {
			console.error(e);
			test.ok(false, 'Triggered an error');
			test.done();
		});

	});

};