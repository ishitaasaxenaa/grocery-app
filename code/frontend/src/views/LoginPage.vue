<!-- Login.vue -->
<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <h2 class="text-center mb-4">Welcome to the Shop</h2>
        <form @submit.prevent="login" class="bg-light p-4 rounded">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" v-model="email" required>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <p class="mt-3">New User? <router-link to="/register">Register here</router-link> <router-link
            to="/manager-login">Manager Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch("http://localhost:8000/login?include_auth_token=", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        const data = await response.json();

        if (data.meta && data.meta.code === 200 && data.response.csrf_token) {
          // Successful login
          localStorage.setItem("auth-token", data.response.user.authentication_token);
          console.log(data.response.user)
          localStorage.setItem("role", 1);
          this.$router.push("/shop");
        } else {
          alert(data.response.errors[0])
          console.log(data.response.errors[0])
          console.error("Login failed");
        }
          
      } catch (error) {
        console.error("An error occurred during login", error);
      }
    },
  },
};
</script>

<style scoped>
.col-md-8 {
  max-width: 400px;
}
</style>
