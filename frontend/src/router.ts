import Vue from 'vue';
import Router from 'vue-router';
import RouterComponent from '@/components/RouterComponent.vue';
Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import(/* webpackChunkName: 'start' */ './views/main/Start.vue'),
      children: [
        {
          path: 'login',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () => import(/* webpackChunkName: 'login' */ './views/Login.vue'),
        },
        {
          path: 'recover-password',
          component: () => import(/* webpackChunkName: 'recover-password' */ './views/PasswordRecovery.vue'),
        },
        {
          path: 'reset-password',
          component: () => import(/* webpackChunkName: 'reset-password' */ './views/ResetPassword.vue'),
        },
        {
          path: 'main',
          component: () => import(/* webpackChunkName: 'main' */ './views/main/Main.vue'),
          children: [
            {
              path: 'dashboard',
              component: () => import(/* webpackChunkName: 'main-dashboard' */ './views/main/Dashboard.vue'),
            },
            {
              path: 'reporting',
              component: () => import(/* webpackChunkName: "main-reporting" */ './views/main/report.vue'),
            },
            {
              path: 'profile',
              component: RouterComponent,
              redirect: 'profile/view',
              children: [
                {
                  path: 'view',
                  component: () => import(
                    /* webpackChunkName: 'main-profile' */ './views/main/profile/UserProfile.vue'),
                },
                {
                  path: 'edit',
                  component: () => import(
                    /* webpackChunkName: 'main-profile-edit' */ './views/main/profile/UserProfileEdit.vue'),
                },
                {
                  path: 'password',
                  component: () => import(
                    /* webpackChunkName: 'main-profile-password' */ './views/main/profile/UserProfileEditPassword.vue'),
                },
              ],
            },
            {
              path: 'admin',
              component: () => import(/* webpackChunkName: 'main-admin' */ './views/main/admin/Admin.vue'),
              children: [
                {
                  path: 'users',
                  component: RouterComponent,
                  redirect: 'users/all',
                  children: [
                    {
                      path: 'all',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-users' */ './views/main/admin/AdminUsers.vue'),
                    },
                    {
                      path: 'edit/:id',
                      name: 'main-admin-users-edit',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-users-edit' */ './views/main/admin/EditUser.vue'),
                    },
                    {
                      path: 'create',
                      name: 'main-admin-users-create',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-users-create' */ './views/main/admin/CreateUser.vue'),
                    },
                  ],
                },
                {
                  path: 'lab',
                  component: RouterComponent,
                  redirect: 'lab/all',
                  children: [
                    {
                      path: 'all',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-hospitals' */ './views/main/admin/hospital/allHospitals.vue'),
                    },
                    {
                      path: 'departments',
                      component: RouterComponent,
                      redirect: 'departments',
                      children: [
                        {
                          path: 'departments',
                          component: () => import(
                            /* webpackChunkName: 'main-admin-hospitals-departments' */ './views/main/admin/hospital/departments/allDepartments.vue'),
                        },
                      ],
                    },
                    {
                      path: 'edit/:id',
                      name: 'main-admin-hospitals-edit',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-hospitals-edit' */ './views/main/admin/hospital/EditHospital.vue'),
                    },
                    {
                      path: 'create',
                      name: 'main-admin-hospitals-create',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-hospitals-create' */ './views/main/admin/hospital/CreateHospital.vue'),
                    },
                  ],
                },
                {
                  path: 'lab/:id',
                  component: RouterComponent,
                  props: true,
                  children: [
                    {
                      path: '',
                      name: 'main-admin-hospitals-departments',
                      component: () => import(
                      /* webpackChunkName: 'main-admin-hospitals-departments' */ './views/main/admin/hospital/departments/allDepartments.vue'),
                      props: {
                        default: true,
                        id: (route) => ({ search: route.query.id }),
                      },
                    },
                    {
                      path: 'department/create',
                      name: 'main-admin-hospital-department-create',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-hospital-department-create' */ './views/main/admin/hospital/departments/CreateDepartment.vue'),
                    },
                    {
                      path: 'department/edit/:departmentId',
                      name: 'main-admin-hospital-department-edit',
                      component: () => import(
                        /* webpackChunkName: 'main-admin-hospital-department-edit' */ './views/main/admin/hospital/departments/EditDepartment.vue'),
                    },
                    {
                      path: 'department/:id',
                      component: RouterComponent,
                      props: true,
                      redirect: 'department/:id/all',
                      children: [
                        {
                          path: 'all',
                          name: 'main-admin-hospital-department-survey',
                          component: () => import(
                          /* webpackChunkName: 'main-admin-hospital-department-survey' */ './views/main/admin/hospital/departments/survey/allSurveys.vue'),
                        },
                        {
                          path: 'survey/create',
                          name: 'main-admin-hospital-department-survey-create',
                          component: () => import(
                            /* webpackChunkName: 'main-admin-hospital-department-survey-create' */ './views/main/admin/hospital/departments/survey/createSurvey.vue'),
                        },
                        {
                          path: 'survey/edit/:id',
                          name: 'main-admin-hospital-department-survey-edit',
                          component: () => import(
                            /* webpackChunkName: 'main-admin-hospital-department-survey-edit' */ './views/main/admin/hospital/departments/survey/editSurvey.vue'),
                        },
                      ],
                    },
                  ],
                },
              ],
            },
          ],
        },
      ],
    },
    {
      path: '/*', redirect: '/',
    },
  ],
});
