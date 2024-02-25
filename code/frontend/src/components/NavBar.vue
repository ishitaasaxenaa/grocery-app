<template>
    <div class="container">
        <a class="navbar-brand" :href="getDashboardLink()">Your Shop</a>

        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#nav-collapse"
            aria-controls="nav-collapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="nav-collapse">
            <ul class="navbar-nav ml-auto">
                
                <li class="nav-item">
                    <a v-if="role == 3" class="nav-link" @click="getReport">Get Report</a>
                    <a v-if="role == 1" class="nav-link" @click="goToCart">Cart</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" @click="logout">Logout</a>
                </li>
            </ul>

            <!-- Search bar -->
            <div v-if="role==3 || role==1" class="search-bar">
                <input v-model="searchTerm" type="text" placeholder="Search by product or category" />
                <input v-model.number="maxPrice" type="number" placeholder="Max Price Filter" />
                <button @click="filterResults">Search</button>
            </div>
        </div>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            username: "", 
            searchTerm: "", 
            maxPrice: null, 
            role: localStorage.getItem("role"),
        };
    },
    computed: {
        isLoginPage() {
            return this.$route.path === '/' || this.$route.path === '/manager-login' || this.$route.path === '/register' || this.$route.path === '/register-manager';   
        },
    },

    methods: {
        goToCart() {
            this.$router.push("/cart");
        },
        logout() {
            this.$router.push("/");
        },
        filterResults() {

            this.$router.push({
                name: 'Search',
                query: {
                    q: this.searchTerm,
                    max_price: this.maxPrice,
                },
            });
        },
        getDashboardLink() {
            console.log(this.role);
            if (this.role == 3) {
                return "/manager-dashboard";
            } else if (this.role == 2) {
                return "/admin-dashboard";
            } else {
                return "/shop";
            }
        },

        async getReport() {
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/send_csv", {
                    methods: "GET",
                    headers: {
                        "Authentication-Token": authToken,
                    },
                });
                const data = await response.json();
                console.log(data);
                if (response.status === 200) {
                    alert("Report has been sent to your email")
                    console.log("Report generated successfully");
                } else {
                    console.error("Report generation failed");
                }
            } catch (error) {
                console.error("An error occurred during report generation", error);
            }
        },

    },
};
</script>
  
<style>
/* Add custom styles if needed */
.search-bar {
    display: flex;
    width: 150%;
    align-items: center;
}

.search-bar input {
    margin-right: 10px;
    width: 70%;
}

.search-bar input[type="number"] {
    width: 20%;
}
</style>
  