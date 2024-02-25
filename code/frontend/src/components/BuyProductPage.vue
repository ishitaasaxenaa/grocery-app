<template>
  <div class="buy-product-page">
    <h2>{{ product ? product.name : 'Product Not Available' }}</h2>
    <div>
      <p>Availability: {{ product && product.quantity > 0 ? 'In stock' : 'Out of Stock' }} [{{ product ? product.quantity : 'N/A' }} {{ product ? product.unit : 'N/A' }} available]</p>
      <label for="quantity">Quantity:</label>
      <input type="number" id="quantity" v-model="quantity" :max="maxQuantity">

      <p>Unit Price: ${{ product ? product.price : 0 }}</p>
      <p>Total Price: ${{ totalPrice }}</p>
    </div>
    <button @click="buy" :disabled="quantity <= 0 || !product || quantity > product.quantity" class="btn btn-primary">Buy</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      availability: 'In stock', 
      quantity: 0,
      product: null,
    };
  },
  computed: {
    totalPrice() {
      return this.quantity * (this.product ? this.product.price : 0);
    },
    maxQuantity() {
    return this.product ? parseInt(this.product.quantity) : 10;
  },
  },
  methods: {
    async fetchData(productId) {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch(`http://localhost:8000/api/product?id=${productId}`, {
          headers: {
            'Authentication-Token': authToken,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.product = data;
        } else {
          console.error('Failed to fetch product details');
        }
      } catch (error) {
        console.error('Error fetching product details:', error);
      }
    },
    updateTotalPrice() {
      // You can leave this method empty or add any specific logic if needed
    },
    async buy() {
      if (this.product) {
        try {
          const authToken = localStorage.getItem('auth-token');
          const response = await fetch('http://localhost:8000/api/cart', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authentication-Token': authToken,
            },
            body: JSON.stringify({
              product_id: this.product.id,
              quantity: this.quantity,
            }),
          });

          if (response.ok) {
            console.log('Product added to cart successfully');
            this.$router.push('/cart');
          } else {
            console.error('Failed to add product to cart:', response.statusText);
          }
        } catch (error) {
          console.error('Error adding product to cart:', error);
        }
      }
    },
  },
  mounted() {
    // Access the productId from route parameters
    const productId = this.$route.params.id;
    console.log('ProductId:', productId);

    // Fetch product details using the API
    this.fetchData(productId);
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
.buy-product-page {
  max-width: 400px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
}
</style>
