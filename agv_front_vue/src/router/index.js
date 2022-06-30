import Vue from 'vue'
import Router from 'vue-router'
/* Layout */
import Layout from '@/layout'

Vue.use(Router)

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/test',
    component: () => import('@/views/test/index')
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  }
  // 404 page must be placed at the end !!!
]

export const asyncRoutes = [
  {
    path: '/example',
    component: Layout,
    redirect: '/example/table',
    alwaysShow: true,
    name: 'Example',
    meta: { title: 'Example', icon: 'el-icon-s-help', roles: ['admin', 'client'] },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: '综合订单统计表', icon: 'table', roles: ['client'] }
      },
      {
        path: 'goodsList',
        name: 'goodsList',
        component: () => import('@/views/goodsList/index'),
        meta: { title: '商品管理', icon: 'tree', roles: ['client'] }

      },
      {
        path: 'order',
        name: 'adminOrder',
        component: () => import('@/views/adminOrder/index'),
        meta: { title: '订单管理', icon: 'tree', roles: ['admin'] }

      },
      {
        path: 'equipments',
        name: 'equipments',
        component: () => import('@/views/equipments/index'),
        meta: { title: '设备管理', icon: 'el-icon-s-shop', roles: ['admin'] }

      },

      {
        path: 'order',
        name: 'clientOrder',
        component: () => import('@/views/clientOrder/index'),
        meta: { title: '订单管理', icon: 'el-icon-s-order', roles: ['client'] }

      },
      {
        path: 'dispatch',
        name: 'dispatch',
        component: () => import('@/views/dispatch/index'),
        meta: { title: '订单调度', icon: 'tree', roles: ['admin'] }

      },

      {
        path: 'goodsList/add',
        name: 'add',
        component: () => import('@/views/goodsList/add'),
        hidden: true

      },
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/user/index'),
        meta: { title: '用户管理', icon: 'el-icon-s-custom', roles: ['admin'] }

      }
    ]
  },
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
