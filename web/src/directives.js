export default {
  "marked": function(el, binding) {
    if (binding.value !== undefined) {
      el.innerHTML = marked(binding.value)
    }
  },
  "highlight": function(el, binding) {
    if (binding.value !== undefined) {
      let value = null
      if (typeof(binding.value) === "string") {
        value = binding.value
      } else {
        value = JSON.stringify(binding.value, null, 4)
      }
      el.innerHTML = hljs.highlight("json", value, true).value
    }
  }
}
