import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '@/utils/supabase'
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
import DashboardLayout from '@/components/layout/DashboardLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import ProfileView from '@/views/system/ProfileView.vue'
import AboutView from '@/views/system/Aboutview.vue'

const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
  {
    path: '/',
    component: DashboardLayout,
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView,
      },
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
      },
      {
        path: 'about',
        name: 'about',
        component: AboutView,
      },
      // 404 ROUTE — KEEP THIS LAST
      {
        path: '/:pathMatch(.*)*',
        name: 'not-found',
        component: () => import('@/views/system/NotFoundView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Protect all routes except Login and Register (Route Guard or Navigation Guard)
router.beforeEach(async (to) => {
  const {
    data: { user },
  } = await supabase.auth.getUser()

  // Login and Register are public
  if (to.name === 'login' || to.name === 'register') {
    return true
  }

  // Everything else requires authentication
  if (!user) {
    return { name: 'login' }
  }

  return true
})

export default router

