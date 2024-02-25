<!-- CartPage.vue -->
<template>
  <div class="cart-page">
    <h2>Your Cart</h2>
    <div v-if="productsInCart.length === 0">
      <p>Your cart is empty.</p>
    </div>
    <div v-else>
      <CartProduct
      v-for="product in productsInCart"
      :key="product.product_id"
      :product="product"
      @cart-item-deleted="onCartItemDeleted"
    />
      <div class="total-price">Total Price: ${{ totalCartPrice }}</div>
      <button @click="buyAll" :disabled="productsInCart.length === 0" class="btn btn-primary">Buy All</button>
    </div>
  </div>
</template>

<script>
import CartProduct from '@/components/CartProduct.vue';

export default {
  components: {
    CartProduct,
  },
  data() {
    return {
      productsInCart: [],
    };
  },
  computed: {
    totalCartPrice() {
      return this.productsInCart.reduce((total, product) => total + product.totalPrice, 0);
    },
  },
  methods: {
    async fetchCartItems() {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch('http://localhost:8000/api/cart', {
          headers: {
            'Authentication-Token': authToken,
          },
        });

        if (response.ok) {
          const data = await response.json();
          console.log(data)
          this.productsInCart = data.products_in_cart.map(product => ({
            ...product,
            totalPrice: product.price * product.quantity,
          }));
        } else {
          console.error('Failed to fetch cart items:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching cart items:', error);
      }
    },
    onCartItemDeleted() {
      this.fetchCartItems();
    },
    async buyAll() {
      const authToken = localStorage.getItem('auth-token');
      const response = await fetch('http://localhost:8000/api/buy_all', {
        method: 'GET',
        headers: {
          'Authentication-Token': authToken,
        },
      })
      console.log(response)
      if (response.ok){
        console.log("All items bought")
        alert("All items bought")
        this.$router.push({ name: 'Shop' });
      }
      else{
        console.error('Failed to buy all items:', response.statusText);
      }
      console.log('Buying all items in the cart');
    },
  },
  mounted() {
    this.fetchCartItems();
  },
};
</script>

<style scoped>
/* Add custom styles if needed */
.cart-page {
  max-width: 800px;
  margin: 20px auto;
}

.total-price {
  margin-top: 20px;
  font-size: 1.5em;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 16px;
  cursor: pointer;
  margin-top: 10px;
}
</style>
