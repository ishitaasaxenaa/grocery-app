<template>
    <form @submit="submitForm" class="mt-4" style="max-width: 400px; margin: 0 auto;">
        <div class="mb-3">
            <label for="productName" class="form-label">Product Name:</label>
            <input type="text" id="productName" class="form-control" v-model="productName" required>
        </div>
        <div class="mb-3">
            <label for="quantity" class="form-label">Quantity:</label>
            <input type="number" id="quantity" class="form-control" v-model="quantity" required>
        </div>
        <div class="mb-3">
            <label for="price" class="form-label">Price:</label>
            <input type="number" id="price" class="form-control" v-model="price" required>
        </div>
        <div class="mb-3">
            <label for="unit" class="form-label">Unit:</label>
            <input type="text" id="unit" class="form-control" v-model="unit" required>
        </div>
        <div class="mb-3">
            <label for="category" class="form-label">Category:</label>
            <select id="category" class="form-select" v-model="categoryId" required>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
            </select>
        </div>
        <button type="submit" :disabled="quantity < 0" class="btn btn-primary">Submit</button>
        
    </form>
</template>
  
<script>
import { useProductStore } from '../store/productStore';

export default {
    data() {
        return {
            productName: '',
            quantity: 0,
            price: 0,
            categoryId: '',
            unit: '',
            categories: [],
            categoryName: '',
        };
    },
    mounted() {
        this.fetchCategories();
        this.prefillForm();
    },
    methods: {
        fetchCategories() {
            const authToken = localStorage.getItem('auth-token');

            fetch('http://localhost:8000/api/category', {
                headers: {
                    'Authentication-Token': authToken// Add other headers if needed
                },
            })
                .then(response => response.json())
                .then(data => {
                    this.categories = data;
                    console.log('Categories fetched successfully:', data);
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                });
        },
        prefillForm() {
            const productStore = useProductStore();
            const editingProduct = productStore.getEditingProduct();
            if (editingProduct) {
                this.productName = editingProduct.name;
                this.quantity = editingProduct.quantity;
                this.price = editingProduct.price;
                this.categoryName = editingProduct.category;
                this.categoryId = editingProduct.category_id;
                this.unit = editingProduct.unit;
            }
            console.log("Editin", editingProduct);
        },
        submitForm(event) {
            event.preventDefault();

            const authToken = localStorage.getItem('auth-token');

            const requestBody = {
                name: this.productName,
                quantity: this.quantity,
                price: this.price,
                category_id: this.categoryId,
                unit: this.unit,
            };
            console.log("request", requestBody);
            const productId = this.$route.params.id;
            fetch(`http://localhost:8000/api/product?id=${productId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': authToken// Add other headers if needed
                },
                body: JSON.stringify(requestBody),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Product updated successfully:', data);
                    this.$router.push({ name: 'ManagerDashboard' });

                    })
                .catch(error => {
                    console.error('Error updating product:', error);
                });
        },
    },
};
</script>
  