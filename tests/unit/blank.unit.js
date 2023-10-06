// Vitest
import { test } from "vitest";

test('blank', () => {});


// MyComponent.spec.js
// import { describe, it, expect, vi } from 'vitest'
// import { mount } from '@vue/test-utils'
// import { createStore } from 'vuex'
// import MyComponent from '../MyComponent.vue'

// describe('MyComponent', () => {
//   it('button calls doAction', async () => {
//     const actions = {
//       doAction: vi.fn(),
//     }
//     const mockStore = createStore({
//       modules: {
//         myModule: {
//           namespaced: true,
//           actions,
//         },
//       },
//     })
//     const wrapper = mount(MyComponent, {
//       global: {
//         plugins: [mockStore], // 👈
//       },
//     })
//     await wrapper.find("button").trigger("click")
//     expect(actions.doAction).toHaveBeenCalled()
//   })
// })


// import { createStore } from 'vuex'
//
// const store = createStore({
//   state() {
//     return {
//       count: 0
//     }
//   },
//   mutations: {
//     increment(state: any) {
//       state.count += 1
//     }
//   }
// })
//
// test('vuex', async () => {
//   const wrapper = mount(App, {
//     global: {
//       plugins: [store]
//     }
//   })
//
//   await wrapper.find('button').trigger('click')
//
//   expect(wrapper.html()).toContain('Count: 1')
// })


// import { createStore } from 'vuex'
//
// export default createStore({
//   state: {
//     count: 0
//   },
//   getters: {
//     getCount(state) {
//       return state.count
//     }
//   },
//   mutations: {
//     increment(state) {
//       state.count++
//     }
//   }
// })