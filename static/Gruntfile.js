/*global module:false*/
module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    // Metadata.
    pkg: grunt.file.readJSON('package.json'),
    banner: '/*! <%= pkg.title || pkg.name %> - v<%= pkg.version %> - ' +
      '<%= grunt.template.today("yyyy-mm-dd") %>\n' +
      '<%= pkg.homepage ? "* " + pkg.homepage + "\\n" : "" %>' +
      '* Copyright (c) <%= grunt.template.today("yyyy") %> <%= pkg.author.name %>;' +
      ' Licensed <%= _.pluck(pkg.licenses, "type").join(", ") %> */\n',
    // Task configuration.
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      dist: {
        src: ['src/js/*.js'],
        dest: 'js/<%= pkg.name %>.js'
      }
    },
    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      dist: {
        src: ['<%= concat.dist.dest %>'],
        dest: 'js/<%= pkg.name %>.min.js'
      }
    },
    jshint: {
      dist:{
        src: ['Gruntfile.js','src/js/*.js']
      }
    },
    less: {
      options: {
          paths:['src/less']
        },
      dist:{
        src:['src/less/<%= pkg.name %>.less'],
        dest:'css/<%= pkg.name %>.css'
      }
    },
    csslint: {
      dist: {
        src:['css/<%= pkg.name %>.css']
      }
    },
    cssmin: {
      dist: {
        src: 'css/<%= pkg.name %>.css',
        dest: 'css/<%= pkg.name %>.min.css'
      }
    },
    qunit: {
      dist:{
        src: ['*.html']
      }
    },
    watch: {
      js:{
        files: ['src/js/*.js'],
        tasks: ['jshint','concat','uglify']
      },
      less:{
        files: ['src/less/*.less'],
        tasks: ['less','csslint','cssmin']
      }
    }
  });

  // These plugins provide necessary tasks.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-watch');
  // Default task.
  grunt.registerTask('default', ['jshint','concat', 'uglify','less','csslint','cssmin','qunit']);

};
