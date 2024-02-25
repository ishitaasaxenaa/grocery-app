<!-- Register.vue -->
<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h2 class="text-center mb-4">Register</h2>
          <form @submit.prevent="register" class="bg-light p-4 rounded">
            <div class="mb-3">
              <label for="email" class="form-label">Email address</label>
              <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
              <label for="username" class="form-label">Username</label>
              <input type="text" class="form-control" id="username" v-model="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: "",
        username: "",
        password: "",
      };
    },
    methods: {
      async register() {
        try {
          const response = await fetch("http://localhost:8000/register1", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.email,
              username: this.username,
              password: this.password,
            }),
          });
  
          const data = await response.json();
          console.log(data);
          if (response.status === 200) {
            console.log("User registered successfully and assigned to role");
            this.$router.push("/");
          } else {
            console.error("Registration failed");
          }
        } catch (error) {
          console.error("An error occurred during registration", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .col-md-8 {
    max-width: 400px;
    width: 100%;
  }
  </style>
  