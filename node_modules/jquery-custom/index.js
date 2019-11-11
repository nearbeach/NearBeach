
var extend = require('util')._extend;
var requirejs = require('requirejs');
var fs = require( "fs" );
var pjoin = require('path').join;

var build = module.exports = function build (opts, cb) {
	var options = {
		release: 2,
		src: '',
		amdName: 'jquery',
		flags: [],
		include: [],
		exclude: [],
		version: null
	};

	var minimum = ["core", "selector"];
	var removeWith = {
		ajax: [ "manipulation/_evalUrl", "event/ajax" ],
		callbacks: [ "deferred" ],
		css: [ "effects", "dimensions", "offset" ],
		sizzle: [ "css/hiddenVisibleSelectors", "effects/animatedSelector" ]
	};


	if (Array.isArray(opts)) {
		// first argument is an array of flags
		options.flags = opts;

	} else if (typeof opts === 'object') {
		// first argument is an options object
		extend(options, opts);

	} else if (typeof opts === 'function') {
		// first argument is a callback. no options defined
		cb = opts;

	} else if (typeof opts === 'string' && arguments.length > 2) {
		// arguments are a series of flags, assume last argument is a callback.
		options.flags = Array.prototype.slice.call(arguments);
		cb = options.flags.pop();
	}

	if (typeof cb !== 'function') throw new Error('You must provide a callback function.');

	if (!options.src) {
		switch (options.release) {
		case 1:         options.src = pjoin(__dirname, "jquery.1/src/"); break;
		case 2:default: options.src = pjoin(__dirname, "jquery.2/src/"); break;
		case 3:         options.src = pjoin(__dirname, "jquery.3/src/"); break;
		}
	}

	var version = options.version;
	if (!version && fs.statSync(pjoin(options.src, '/../package.json'))) {
		var pkg = require(pjoin(options.src, '/../package.json'));
		version = pkg.version;
	}

	var output;
	var config = {
		baseUrl: options.src,
		name: "jquery",
		out: function( compiled ) {
			compiled = compiled
				// Embed Version
				.replace( /@VERSION/g, version )
				// Embed Date
				// yyyy-mm-ddThh:mmZ
				.replace( /@DATE/g, ( new Date() ).toISOString().replace( /:\d+\.\d+Z$/, "Z" ) );

			// Write concatenated source to file
			output = compiled;
		},
		// We have multiple minify steps
		optimize: "none",
		// Include dependencies loaded with require
		findNestedDependencies: true,
		// Avoid inserting define() placeholder
		skipModuleInsertion: true,
		// Avoid breaking semicolons inserted by r.js
		skipSemiColonInsertion: true,
		wrap: {
			startFile: pjoin(options.src, "intro.js"),
			endFile: pjoin(options.src, "outro.js")
		},
		paths: {
			sizzle: pjoin(options.src, "sizzle/dist/sizzle")
		},
		rawText: {},
		onBuildWrite: convert
	};

	var included = [].concat(options.include),
		excluded = [].concat(options.exclude);

	//loop through all the arguments.
	options.flags.filter(Boolean).forEach(excluder);

	// Handle Sizzle exclusion
	// Replace with selector-native
	if ( (index = excluded.indexOf( "sizzle" )) > -1 ) {
		config.rawText.selector = "define(['./selector-native']);";
		excluded.splice( index, 1 );
	}

	// Replace exports/global with a noop noConflict
	if ( (index = excluded.indexOf( "exports/global" )) > -1 ) {
		config.rawText[ "exports/global" ] = "define(['../core']," +
			"function( jQuery ) {\njQuery.noConflict = function() {};\n});";
		excluded.splice( index, 1 );
	}

	// append excluded modules to version
	if ( excluded.length ) {
		version += " -" + excluded.join( ",-" );
		
		// Have to use shallow or core will get excluded since it is a dependency
		config.excludeShallow = excluded;
	}
	config.include = included;

	// Turn off opt-in if necessary
	if ( options.flags.indexOf('-all') !== -1 ) {
		// Overwrite the default inclusions with the explicit ones provided
		config.rawText.jquery = "define([" +
			(included.length ? included.join(",") : "") +
		"]);";
	}

	requirejs.optimize( config, function( response ) {
		cb(null, output);
	}, cb);

	/**
	 * Recursively calls the excluder to remove on all modules in the list
	 * @param {Array} list
	 * @param {String} [prepend] Prepend this to the module name.
	 *  Indicates we're walking a directory
	 */
	function excludeList ( list, prepend ) {
		if ( list ) {
			prepend = prepend ? prepend + "/" : "";
			list.forEach(function( module ) {
				// Exclude var modules as well
				if ( module === "var" ) {
					excludeList(
						fs.readdirSync( pjoin(options.src, prepend, module) ), pjoin(prepend, module)
					);
					return;
				}
				if ( prepend ) {
					// Skip if this is not a js file and we're walking files in a dir
					if ( !(module = /([\w-\/]+)\.js$/.exec( module )) ) {
						return;
					}
					// Prepend folder name if passed
					// Remove .js extension
					module = prepend + module[1];
				}

				// Avoid infinite recursion
				if ( excluded.indexOf( module ) === -1 ) {
					excluder( "-" + module );
				}
			});
		}
	}

	/**
	 * Adds the specified module to the excluded or included list, depending on the flag
	 * @param {String} flag A module path relative to
	 *  the src directory starting with + or - to indicate
	 *  whether it should included or excluded
	 */
	function excluder ( flag ) {
		var m = /^(\+|\-|)([\w\/-]+)$/.exec( flag ),
			exclude = m[ 1 ] === "-",
			module = m[ 2 ];

		if (module === 'all') return;

		if ( exclude ) {
			// Can't exclude certain modules
			if ( minimum.indexOf( module ) === -1 ) {
				// Add to excluded
				if ( excluded.indexOf( module ) === -1 ) {
					excluded.push( module );
					// Exclude all files in the folder of the same name
					// These are the removable dependencies
					// It's fine if the directory is not there
					try {
						excludeList( fs.readdirSync( pjoin(options.src, module) ), module );
					} catch ( e ) {
						
					}
				}
				// Check removeWith list
				excludeList( removeWith[ module ] );
			} else {
				throw new Error( "Module \"" + module + "\" is a minimum requirement.");
			}
		} else {
			included.push( module );
		}
	}

	/**
	 * Strip all definitions generated by requirejs
	 * Convert "var" modules to var declarations
	 * "var module" means the module only contains a return
	 * statement that should be converted to a var declaration
	 * This is indicated by including the file in any "var" folder
	 * @param {String} name
	 * @param {String} path
	 * @param {String} contents The contents to be written (including their AMD wrappers)
	 */
	function convert( name, path, contents ) {
		var rdefineEnd = /\}\);[^}\w]*$/;
		var amdName;
		// Convert var modules
		if ( /.\/var\//.test( path ) ) {
			contents = contents
				.replace( /define\([\w\W]*?return/, "var " + (/var\/([\w-]+)/.exec(name)[1]) + " =" )
				.replace( rdefineEnd, "" );

		// Sizzle treatment
		} else if ( /^sizzle$/.test( name ) ) {
			contents = "var Sizzle =\n" + contents
				// Remove EXPOSE lines from Sizzle
				.replace( /\/\/\s*EXPOSE[\w\W]*\/\/\s*EXPOSE/, "return Sizzle;" );

		} else {

			if ( name !== "jquery" ) {
				contents = contents
					.replace( /\s*return\s+[^\}]+(\}\);[^\w\}]*)$/, "$1" )
					// Multiple exports
					.replace( /\s*exports\.\w+\s*=\s*\w+;/g, "" );
			}

			// Remove define wrappers, closure ends, and empty declarations
			contents = contents
				.replace( /define\([^{]*?{/, "" )
				.replace( rdefineEnd, "" );

			// Remove anything wrapped with
			// /* ExcludeStart */ /* ExcludeEnd */
			// or a single line directly after a // BuildExclude comment
			contents = contents
				.replace( /\/\*\s*ExcludeStart\s*\*\/[\w\W]*?\/\*\s*ExcludeEnd\s*\*\//ig, "" )
				.replace( /\/\/\s*BuildExclude\n\r?[\w\W]*?\n\r?/ig, "" );

			// Remove empty definitions
			contents = contents
				.replace( /define\(\[[^\]]*\]\)[\W\n]+$/, "" );
		}
		// AMD Name
		if ( options.amdName && /^exports\/amd$/.test( name ) ) {
			// Remove the comma for anonymous defines
			contents = contents
				.replace( /(\s*)"jquery"(\,\s*)/, options.amdName ? "$1\"" + options.amdName + "\"$2" : "" );

		}
		return contents;
	}

};

