<template>
  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">{{ product.name }}</h5>
      <p class="card-text">Price: ${{ product.price }}</p>
      <p class="card-quantity">Quantity: {{ product.quantity }}</p>
      <p class="card-unit">Unit: {{ product.unit }}</p> 
      <button @click="handleBuy" :disabled="product.quantity === 0" class="btn btn-primary">Buy</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    product: Object, 
  },
  methods: {
    handleBuy() {
      if (this.product && this.product.quantity > 0) {
        this.$router.push({ name: 'BuyProduct', params: { id: this.product.id, product: this.product}});
      }
    },
  },
};
</script>

<style scoped>
</style>
