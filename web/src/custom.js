import directives from './directives'

export default {
  install(Vue, options) {
    // 2. 添加全局资源
    for (let name in directives) {
      Vue.directive(name, directives[name])
    }
    // 4. 添加事例方法
    Vue.prototype.go = function(url) {
      options.router.push(url)
    }
  }
}
