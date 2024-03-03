import { defineComponent } from 'vue'
import { DateTime } from 'luxon'

export default defineComponent({
  data () {
    return {
      now: DateTime.now(),
      $nowMixinInterval: null as null | number
    }
  },
  mounted () {
    this.$nowMixinInterval = setInterval(() => {
      this.now = DateTime.now()
    }, 1000)
  },
  beforeUnmount () {
    if (this.$nowMixinInterval) {
      clearInterval(this.$nowMixinInterval)
    }
  }
})
