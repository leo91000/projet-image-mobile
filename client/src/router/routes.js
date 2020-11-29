
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/image-search/:id', component: () => import('pages/ImageSearchView.vue') },
      { path: '/add-image-to-database', component: () => import('pages/AddImageToDatabase.vue') },
      { path: '/add-image-search', component: () => import('pages/SimilarImageSearch.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
