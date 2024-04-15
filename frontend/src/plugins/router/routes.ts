export const routes = [
  { path: '/', redirect: '/getting-started' },
  {
    path: '/',
    component: () => import('@/layouts/default.vue'),
    children: [
      {
        path: 'getting-started',
        component: () => import('@/pages/getting-started.vue')
      },
      {
        path: 'settings',
        component: () => import('@/pages/settings.vue')
      },
      {
        path: 'accounts',
        component: () => import('@/pages/accounts.vue')
      }
    ]
  },
  {
    path: '/',
    component: () => import('@/layouts/blank.vue'),
    children: [
      {
        path: 'login',
        component: () => import('@/pages/login.vue')
      },
      {
        path: 'register',
        component: () => import('@/pages/register.vue')
      },
      {
        path: '/:pathMatch(.*)*',
        component: () => import('@/pages/[...error].vue')
      }
    ]
  }
]
