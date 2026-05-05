import Vue from 'vue'
import App from '@/App'

describe('App.vue', () => {
  it('should have #app div', () => {
    const Constructor = Vue.extend(App)
    const vm = new Constructor().$mount()
    expect(vm.$el.id).toEqual('app')
  })
})

describe('API Configuration', () => {
  it('should export BASE_URL and api object', () => {
    const api = require('@/api')
    expect(api.BASE_URL).toBeDefined()
    expect(api.api).toBeDefined()
    expect(api.api.spider).toBeDefined()
    expect(api.api.compare).toBeDefined()
    expect(api.api.hot).toBeDefined()
  })
})
