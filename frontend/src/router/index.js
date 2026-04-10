import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/tags",
    name: "tag",
    component: () => import("../views/tags/Index.vue"),
  },
  {
    path: "/tags/create",
    name: "tags-create",
    component: () => import("../views/tags/Form.vue"),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router