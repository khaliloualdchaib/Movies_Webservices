import { createRouter, createWebHistory } from 'vue-router'
import search from '../views/SearchPage.vue'
import barplot from '../views/BarplotPage.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'search',
      component: search
    },
    {
      path:'/barplot',
      name:'barplot',
      component: barplot
    },
  ]
})

export default router
