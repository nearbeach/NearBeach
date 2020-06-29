var gulp = require('gulp'),
    browserSync = require('browser-sync').create(),
    rename = require('gulp-rename'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean'),
    notify = require('gulp-notify'),
    minify = require('gulp-minify'),
    cleanCSS = require('gulp-clean-css'),
    sass = require('gulp-sass');


// Clean
gulp.task('clean', function() {
  return gulp.src([
      './NearBeach/static/NearBeach/js',
      './NearBeach/static/NearBeach/css',
      './NearBeach/static/NearBeach/whiteboard',
    ], {read: false, allowEmpty: true})
    .pipe(clean());
});

// Scripts
gulp.task('scripts', function() {
  return gulp.src([
      './NearBeach/build_static/javascript/*.js'
  ])
    .pipe(concat('NearBeach.js'))
    .pipe(minify())
    .pipe(gulp.dest('./NearBeach/static/NearBeach/js'))
    .pipe(notify({ message: 'JavaScript Task Complete' }));
});

gulp.task('js', function() {
    return gulp.src([
        'node_modules/jquery/dist/jquery.min.js',
        'node_modules/d3/dist/d3.min.js',
        'node_modules/popper.js/dist/umd/popper.min.js',
        'node_modules/bootstrap/dist/js/bootstrap.min.js',
        'node_modules/jquery-datetimepicker/build/jquery.datetimepicker.full.min.js',
        'node_modules/mxgraph/javascript/mxClient.min.js',
    ])
    .pipe(gulp.dest('./NearBeach/static/NearBeach/js'))
    .pipe(notify({ message: 'Moved JQuery Task Complete' }));
});

//mxGraph
//gulp.src(['input/folder/**/*']).pipe(gulp.dest('output/folder'));
gulp.task('mxgraph', function() {
    return gulp.src([
        './node_modules/mxgraph/javascript/src/**/*',
        './NearBeach/build_static/whiteboard/**/*',
        './NearBeach/build_static/whiteboard/*'
    ])
    .pipe(gulp.dest('./NearBeach/static/NearBeach/whiteboard'))
    .pipe(notify({ message: 'Implemented Whiteboard module from mxgraph' }));
});

// Styles
gulp.task('styles', function() {
    return gulp.src([
            './NearBeach/build_static/css/*.css',
            './node_modules/jquery-datetimepicker/jquery.datetimepicker.css',
        ])
        .pipe(concat('NearBeach.css'))
        .pipe(minify())
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(rename({extname: ".min.css"}))
        .pipe(gulp.dest('./NearBeach/static/NearBeach/css'))
        .pipe(notify({ message: 'Styles task complete' }));
});

// SASS (bootstrap)
gulp.task('sass', function() {
    return gulp.src([
            'node_modules/bootstrap/scss/bootstrap.scss',
        ])
        .pipe(sass())
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(concat('bootstrap.css'))
        .pipe(rename({extname: ".min.css"}))
        .pipe(gulp.dest('./NearBeach/static/NearBeach/css'))
        .pipe(notify({ message: 'Bootstrap styles task complete' }));
});

// Default Task
gulp.task('default', gulp.series('clean','styles','scripts','sass','js','mxgraph', function(done) {
    console.log("Completed GULP");
    done();
}));

/*

// Static Server + watching scss/html files
gulp.task('serve', gulp.series( 'sass', function() {

browserSync.init({
server: "./src"
});

gulp.watch(['node_modules/bootstrap/scss/bootstrap.scss', 'src/scss/*.scss'], gulp.series('sass'));
gulp.watch("src/*.html").on('change', browserSync.reload);
}));
 */