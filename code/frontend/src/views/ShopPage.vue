<template>
  <div class="container mt-5">
    <h2 class="mb-4">Shop</h2>

    <CategoryPanel v-for="category in uniqueCategories" :key="category" :category="category" :products="getProductsByCategory(category)"></CategoryPanel>
  </div>
</template>

<script>
import CategoryPanel from "@/components/CategoryPanel.vue";

export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    // ... (existing methods)
    async fetchProducts() {
      try {
        const authToken = localStorage.getItem("auth-token");
        const response = await fetch("http://localhost:8000/api/get_cached_products", {
          headers: {
            "Authentication-Token": authToken,
          },
        });

        if (response.ok) {
          this.products = await response.json();
          console.log("Fetched products:", this.products);
        } else {
          console.error("Error fetching products:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Error fetching products", error);
      }
    },
    getProductsByCategory(category) {
      return this.products.filter(product => product.category === category);
    },
  },
  computed: {
    uniqueCategories() {
      return Array.from(new Set(this.products.map(product => product.category)));
    },
  },
  components: {
    CategoryPanel,
  },
};
</script>
