import "typings-global"
var through = require("through2");
var path = require("path");

module.exports = (myArg1 = "undefined",myArg2 = true) => {
    return through.obj(function(file, enc, cb){
        return cb(null, file);
    });
};
