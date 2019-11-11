#!/usr/bin/env node

/// <reference path="typings/main.d.ts" />
var through = require("through2");
var path = require("path");
module.exports = function (myArg1, myArg2) {
    if (myArg1 === void 0) { myArg1 = "undefined"; }
    if (myArg2 === void 0) { myArg2 = true; }
    return through.obj(function (file, enc, cb) {
        return cb(null, file);
    });
};
