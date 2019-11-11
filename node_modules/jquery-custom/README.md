jquery-custom
===
A node module for compiling custom jQuery builds programatically for use with local workflows (grunt and gulp). This package is a port of the jQuery project's custom grunt task, extracted to run without a grunt dependency.

## WARNING: As of jQuery 1.12 and 2.2.0 the jQuery project is now using a completely different build process. As a result, this library no longer works, so I have hard capped the source downloader to jQuery 1.11.3 and 2.1.4, and removed support for jQuery 3.0 alphas until such a time that I can rewrite this builder for the newer versions.

##Installation

NPM: `npm install jquery-custom`

##Usage: `builder(options, callback)`

```js
var fs = require('fs');
var builder = require('jquery-custom');
builder({
	flags: ['-sizzle', '-effects', '-event/alias'],
}, function (err, compiledContent) {
	if (err) return console.error(err);
	fs.writeFile('jquery.js', compiledContent, function (err) {
		if (err) return console.error(err);
	})
})
```

The above example will generate a custom build of jQuery 2 that lacks the sizzle engine, all effects functions, and the event binding shortcuts.

###Options

- `release`: The major version number of jQuery that you want, 1 or 2. (Default is 2)
- `src`: The path to the /src folder of the jQuery package. If left blank, the builder will use the latest version available when the package was installed, for the release selected.
- `amdName`: The name to be used for jQuery on the AMD definition (Default is 'jquery').
- `flags`: An array of modules to be excluded or included. Prefix a module name with a hyphen (-) to exclude. Pass '-all' as the first flag to  exclude all modules except for core. Defining excludes and includes on this array will also exclude or include dependencies.
- `include`: Array of explicit module includes. Bypasses the dependency tree.
- `exclude`: Array of explicit module excludes. Bypasses the dependency tree.
- `version`: The version number provided in the source.  If left undefined, the builder will attempt to fetch the version number from the `package.json` file in the jquery source.

The options object may also be an array of flags, if none of the other options are needed.