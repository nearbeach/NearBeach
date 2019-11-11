// Load plugins
var gulp = require('gulp'),
    sass = require('gulp-stylus'),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean'),
    notify = require('gulp-notify'),
    minify = require('gulp-minify'),
    cleanCSS = require('gulp-clean-css'),
    jquery = require('jquery'),
    popper = require('popper.js'),
    bootstrap = require('bootstrap');

import 'jquery';
// Styles
gulp.task('styles', function() {
  return gulp.src('./NearBeach/build/css/*.css')
    .pipe(concat('NearBeach.css'))
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(rename({extname: ".min.css"}))
    .pipe(gulp.dest('./NearBeach/static/NearBeach/css'))
    .pipe(notify({ message: 'Styles task complete' }));
});

// Scripts
gulp.task('scripts', function() {
  return gulp.src([
      './NearBeach/build/javascript/*.js',
      './node_modules/jquery/dist/jquery.min.js',

  ])
    .pipe(concat('NearBeach.js'))
    .pipe(minify())
    .pipe(gulp.dest('./NearBeach/static/NearBeach/js'))
    .pipe(notify({ message: 'JavaScript Task Complete' }));
});

// Clean
gulp.task('clean', function() {
  return gulp.src(['./NearBeach/static/NearBeach/js', './NearBeach/static/NearBeach/css'], {read: false, allowEmpty: true})
    .pipe(clean());
});

// Default task
gulp.task('default', gulp.series('clean','styles','scripts', function(done) {
    console.log("Completed GULP");
    done();
}));


