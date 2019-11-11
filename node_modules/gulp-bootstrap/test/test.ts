import "typings-global"
var plugins = {
    gulp: require("gulp"),
    gulpBootstrap: require("../index.js"),
    gulpFunction: require("gulp-function")
};

console.log("test now executing");

describe("gulp-bootstrap",function(){
    it("should run through smoothly",function(done){
        plugins.gulp.src("./test/test.md")
            .pipe(plugins.gulpBootstrap())
            .pipe(plugins.gulpFunction(done));
    })
});
