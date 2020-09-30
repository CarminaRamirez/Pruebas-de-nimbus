const gulp = require('gulp');
const imagemin = require('gulp-imagemin');
const extReplace = require('gulp-ext-replace');
const webp = require('imagemin-webp');

gulp.task('webp', () =>{
    return gulp.src('static/img/banners/*')
        .pipe(imagemin([
            webp({quality: 50})
        ]))
        .pipe(extReplace('.webp'))
        .pipe(gulp.dest('static/img/banners/'))
});