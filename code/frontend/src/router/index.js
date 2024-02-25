// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../views/LoginPage.vue'; 
import Register from '../views/RegisterPage.vue';  
import ShopPage from '../views/ShopPage.vue';
import BuyProductPage from '../components/BuyProductPage.vue';
import CartPage from '../views/CartPage.vue';
import ManagerLogin from '../views/ManagerLogin.vue';
import ManagerDashboard from '../views/ManagerDashboard.vue'; 
import EditProduct from '../components/EditProduct.vue'; 
import AddProduct from '../components/AddProduct.vue'; 
import SearchResults from '../views/SearchResults.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import ManagerRegister from '../views/ManagerRegister.vue';

const routes = [
  { path: '/', component: LoginPage },
  // Add other routes as needed
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/shop',
    name: 'Shop',
    component: ShopPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/buy/:id',
    name: 'BuyProduct',
    component: BuyProductPage,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/cart',
    name: 'Cart',
    component: CartPage,
    meta: { requiresAuth: true },
  },
  {
    path: '/manager-login',
    name: 'ManagerLogin',
    component: ManagerLogin,
    meta: { requiresAuth: true },
  },
  {
    path: '/manager-dashboard',
    name: 'ManagerDashboard',
    component: ManagerDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/edit-product/:id',
    name: 'EditProduct',
    component: EditProduct,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/add-product/:id',
    name: 'AddProduct',
    component: AddProduct,
    props: true,
    meta: { requiresAuth: true },
  },
  { 
    path: `/search`,
    name: 'Search',
    component: SearchResults,

    props: true,
    meta : { requiresAuth: true },
  },
  {
    path:'/admin-dashboard',
    name:'AdminDashboard',
    component: AdminDashboard,
  },
  {
    path:'/register-manager',
    name:'ManagerRegister',
    component: ManagerRegister,
  }


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
