import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from "../views/Home";
import Ranobe from "../views/Ranobe";
import RanobeDetail from "../views/RanobeDetail";
import RanobeRead from "../views/RanobeRead";
import Profile from "../views/Profile";
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/ranobe',
    name: 'Ranobe',
    component: Ranobe
  },
  {
    path: '/ranobe/:ranobeId/details',
    name: 'RanobeDetail',
    component: RanobeDetail,
    props: true
  },
  {
    path: '/ranobe/:ranobeId/read',
    name: 'RanobeRead',
    component: RanobeRead,
    props: true
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../components/Login.vue')
  }
];

const router = new VueRouter({
  routes
});

export default router
