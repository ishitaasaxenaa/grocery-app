<!-- Login.vue -->
<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <h2 class="text-center mb-4">Manager/Admin Login</h2>
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
                <p class="mt-3">New manager? <router-link to="/register-manager">Register as Manager here</router-link> <router-link
                    to="/">User Login</router-link></p>
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
                    const authToken = localStorage.getItem("auth-token");
                    const response = await fetch("http://localhost:8000/api/checkrole", {
                        headers: {
                            "Authentication-Token": authToken,
                        },
                    });
                    const role = await response.json();
                    console.log(role);
                    if (role !== null) {
                        localStorage.setItem("role", role);
                        if (role == 3) {
                            this.$router.push("/manager-dashboard");
                        } 
                        else if (role == 2){
                            this.$router.push("/admin-dashboard");
                        }else {
                            this.$router.push("/shop");
                        }
                    }
                } else {
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
  