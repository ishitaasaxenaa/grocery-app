<template>
  <div id="app">
    <NavBar v-if="!isLoginPage" class="navbar navbar-expand-lg navbar-dark bg-info">
    </NavBar>

    <router-view></router-view>
  </div>
</template>


<script>
import NavBar from "./components/NavBar.vue";
export default {
  components: {
    //
    NavBar

  },
computed: {
      isLoginPage() {
        return this.$route.path === '/' || this.$route.path === '/manager-login' || this.$route.path === '/register' || this.$route.path === '/register-manager'  ;
      },
    },
}
</script>

<style>
</style>
