<template>
    <div class="category-panel">
      <h3 class="category-title">{{ category }}</h3>
      <div class="product-list">
        <div v-for="(product, index) in displayedProducts" :key="index" class="product-item">
          <product-card :product="product"></product-card>
        </div>
      </div>
      <button class="btn" @click="scrollProducts(-1)"><i class="bi bi-arrow-left"></i></button>
      <button class="btn" @click="scrollProducts(1)"><i class="bi bi-arrow-right"></i></button>
    </div>
  </template>
  <script>
  import ProductCard from "@/components/ProductCard.vue";
  
  export default {
    props: {
      category: String, // Category name
      products: Array, // List of products in the category
    },
    data() {
      return {
        currentIndex: 0,
        itemsPerPage: 3,
      };
    },
    computed: {
      displayedProducts() {
        const start = this.currentIndex * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        console.log("hiii",this.products);
        return this.products.slice(start, end);
      },
    },
    methods: {
      scrollProducts(direction) {
        const maxIndex = Math.ceil(this.products.length / this.itemsPerPage) - 1;
  
        if (direction === 1 && this.currentIndex < maxIndex) {
          this.currentIndex++;
        } else if (direction === -1 && this.currentIndex > 0) {
          this.currentIndex--;
        }
      },
    },
    components: {
      ProductCard,
    },
  };
  </script>
  
  <style scoped>
/* Add custom styles if needed */
.category-panel {
  margin-bottom: 20px;
}

.category-title {
  font-size: 18px;
  margin-bottom: 10px;
}

.product-list {
  display: flex;
  overflow-x: auto; /* Allow horizontal scrolling */
}

.product-item {
  flex: 0 0 300px; /* Set a fixed width for the product item, adjust the value as needed */
  margin-right: 10px;
}

.arrow-button {
  font-size: 16px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
