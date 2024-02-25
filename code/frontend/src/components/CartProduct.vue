<template>
  <div class="card mb-3">
    <div class="card-body d-flex justify-content-between align-items-center">
      <div>
        <h5 class="card-title">{{ product.name }}</h5>
        <p class="card-text">Price: ${{ product.price }}</p>
        <p class="card-quantity">Quantity: {{ product.quantity }}</p>
      </div>
      <button @click="deleteCartItem(product.cart_item_id)" class="btn btn-danger">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    product: Object,
  },
  methods: {
    async deleteCartItem(cartItemId) {
      try {
        const apiUrl = `http://localhost:8000/api/cart?cart_item_id=${cartItemId}`;
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch(apiUrl, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': authToken,
          },
        });

        if (response.ok) {
          console.log("Item deleted");
          this.$emit('cart-item-deleted');
          
        } else {
          console.error('Failed to delete cart item:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting cart item:', error);
      }
    },
  },
};
</script>

<style scoped>
</style>
