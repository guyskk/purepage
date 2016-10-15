# Vue-Waves

将[Waves](https://github.com/fians/Waves)封装为Vue插件。

## 用法

开始:
```
import VueWaves from './vue-waves'
Vue.use(VueWaves)
```

配置:
```
Vue.use(VueWaves, {
  name: 'waves'   // Vue指令名称
  duration: 500,  // 涟漪效果持续时间
  delay: 200      // 延时显示涟漪效果
})
```

使用:
```
<button v-waves.button>Vue-Waves</button>
```

指令参数:
```
v-waves.button  按钮
v-waves.circle  圆形
v-waves.block   块
v-waves.float   阴影效果
v-waves.light   亮色涟漪
v-waves.classic ??
```
