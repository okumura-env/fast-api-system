import { createRouter, createWebHistory } from "vue-router"

const routes = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/recipes",
    name: "recipes",
    component: () => import("@/views/recipes/Index.vue"),
  },
  {
    path: "/recipes/create",
    name: "recipes-create",
    component: () => import("@/views/recipes/Form.vue"),
  },
  {
    path: "/recipes/:id/edit",
    name: "recipes-edit",
    component: () => import("@/views/recipes/Form.vue"),
    props: true,
  },
  {
    path: "/ingredients",
    name: "ingredients",
    component: () => import("@/views/ingredients/Index.vue"),
  },
  {
    path: "/ingredients/create",
    name: "ingredients-create",
    component: () => import("@/views/ingredients/Form.vue"),
  },
  {
    path: "/ingredients/:id/edit",
    name: "ingredients-edit",
    component: () => import("@/views/ingredients/Form.vue"),
    props: true,
  },
  {
    path: "/tags",
    name: "tags",
    component: () => import("@/views/tags/Index.vue"),
  },
  {
    path: "/tags/create",
    name: "tags-create",
    component: () => import("@/views/tags/Form.vue"),
  },
  {
    path: "/tags/:id/edit",
    name: "tags-edit",
    component: () => import("@/views/tags/Form.vue"),
    props: true,
  },
  {
    path: "/users",
    name: "users",
    component: () => import("@/views/users/Index.vue"),
  },
  {
    path: "/users/create",
    name: "users-create",
    component: () => import("@/views/users/Form.vue"),
  },
  {
    path: "/users/:id/edit",
    name: "users-edit",
    component: () => import("@/views/users/Form.vue"),
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router