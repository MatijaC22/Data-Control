import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import PostsList from '../views/PostsList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/postsList',
      name: 'postsList',
      component: () => import(/* webpackChunkName: "Posts" */ '../views/PostsList.vue'),
      // component: PostsList
    },
    {
      path: '/postsListSearch',
      name: 'postsListSearch',
      component: () => import(/* webpackChunkName: "PostsSearch" */ '../views/PostsListSearch.vue'),
    },
    {
      path: '/dataList',
      name: 'dataList',
      component: () => import(/* webpackChunkName: "Data" */ '../views/DataList.vue')
    },
    {
      path: '/post/:id',
      name: 'post',
      component: () => import(/* webpackChunkName: "Post" */ '../views/PostPage.vue')
    },
    {
      path: '/user/:id',
      name: 'user',
      component: () => import(/* webpackChunkName: "User" */ '../views/UserProfile.vue')
    },
    {
      path: '/database/:type',
      name: 'databaseFull',
      component: () => import(/* webpackChunkName: "DatabaseFull" */ '../views/DatabaseFull.vue')
    },
    {
      path: '/priceCalculator',
      name: 'PriceCalculator',
      component: () => import(/* webpackChunkName: "PriceCalculator" */ '../views/PriceCalculator.vue')
    }
  ]
})

export default router
