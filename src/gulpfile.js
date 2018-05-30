
////////////////////////////////
		//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
      pjson = require('./package.json'),
      gutil = require('gulp-util'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      rename = require('gulp-rename'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      runSequence = require('run-sequence'),
      sourcemaps = require('gulp-sourcemaps');


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);

  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/static/sass/**',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
  }
};

var paths = pathsConfig();

var sassOptions = {
  errLogToConsole: true,
  outputStyle: 'compact'
};

////////////////////////////////
		//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 versions']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.css));
    // .pipe(rename({ suffix: '.min' }))
    // .pipe(cssnano()) // Minifies the result
    // .pipe(gulp.dest(paths.css));
});

// Watch
gulp.task('watch', function() {
  gulp.watch(paths.sass + '/*.scss', ['styles'])
  .on('change', function(event) {
    console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
  });

  // gulp.watch(paths.js + '/*.js', ['scripts']).on("change", reload);
  // gulp.watch(paths.images + '/*', ['imgCompression']);
  // gulp.watch(paths.templates + '/**/*.html').on("change", reload);
});

// Default task
gulp.task('default', function() {
    runSequence(['styles'], 'watch');
});
