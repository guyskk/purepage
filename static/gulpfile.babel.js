import del from 'del'
import gulp from 'gulp'
import riot from 'gulp-riot'
import uglify from 'gulp-uglify'
import rename from 'gulp-rename'
import concat from 'gulp-concat'
import browserSync, { reload } from 'browser-sync'
import proxy from 'proxy-middleware'
import url from 'url'
import less from 'gulp-less'
import autoprefixer from 'gulp-autoprefixer'
import CacheBuster from 'gulp-cachebust'
import cleanCSS from 'gulp-clean-css'
import webpack from 'webpack-stream'
import debounce from 'throttle-debounce/debounce'

let cachebust = new CacheBuster()

function handleError(err) {
    console.log(err.toString());
    this.emit('end');
}

gulp.task('clean', (cb) => {
    del(['dist/**'], cb)
})

gulp.task('build:tags', () => {
    return gulp.src('src/tags/*.html')
        .pipe(riot())
        .pipe(concat('tags.js'))
        .pipe(gulp.dest('dist'))
})

gulp.task('build:bundle', ['build:tags'], () => {
    return gulp.src(['dist/tags.js', 'src/index.js'])
        .pipe(webpack({
            entry: ['babel-polyfill', './dist/tags.js', './src/index.js'],
            output: {
                filename: 'bundle.js'
            },
            module: {
                loaders: [{
                    test: /\.js$/,
                    exclude: /node_modules/,
                    loader: 'babel?cacheDirectory'
                }, ]
            }
        }))
        .on("error", handleError)
        .pipe(cachebust.resources())
        .pipe(gulp.dest('dist'))
        .pipe(uglify())
        .pipe(rename('bundle.min.js'))
        .pipe(cachebust.resources())
        .pipe(gulp.dest('dist'))
})

gulp.task('build:style', () => {
    return gulp.src(['src/style/main.less'])
        .pipe(less())
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(rename('style.css'))
        .pipe(cachebust.resources())
        .pipe(gulp.dest('dist'))
        .pipe(cleanCSS())
        .pipe(rename('style.min.css'))
        .pipe(cachebust.resources())
        .pipe(gulp.dest('dist'))
})

gulp.task('build:html', ['build:bundle', 'build:style'], () => {
    return gulp.src('src/*.html')
        .pipe(cachebust.references())
        .pipe(gulp.dest('dist'))
})

gulp.task('build:lib', () => {
    return gulp.src('lib/**')
        .pipe(gulp.dest('dist/lib'))
})

gulp.task('build', ['build:html', 'build:lib'])

gulp.task('dev', ['build'], () => {
    let options = url.parse('http://127.0.0.1:5000')
    options.route = '/api'
    browserSync({
        server: {
            baseDir: 'dist',
            middleware: [proxy(options)]
        }
    })
    gulp.watch('src/**/*', ['build'])
        // 避免短时间内多次reload
    gulp.watch('dist/**/*', debounce(1500, reload))
})

gulp.task('default', ['build'])
