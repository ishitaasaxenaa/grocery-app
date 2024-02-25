import { defineStore } from 'pinia';

export const useProductStore = defineStore('product', {
  state: () => ({
    editingProduct: null,
    searchedProducts: null,
  }),
  actions: {
    setEditingProduct(product) {
      this.editingProduct = product;
    },
    clearEditingProduct() {
      this.editingProduct = null;
    },
    getEditingProduct() {
      return this.editingProduct;
    },
  },
});

export const useSearchStore = defineStore('products', {
  state: () => ({
    searchedProducts: null,
  }), 
  actions: {  
    getSearchedProducts() {
      return this.searchedProducts;
    },
    setSearchedProducts(products) {
      this.searchedProducts = products;
    },
  }
});
