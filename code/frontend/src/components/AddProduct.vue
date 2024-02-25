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
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>
  
<script>
export default {
    data() {
        return {
            productName: '',
            quantity: 0,
            price: 0,
            unit: '',
            categoryId: this.$route.params.id,
        };
    },
    mounted() {
        this.fetchCategories();
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
        submitForm(event) {
            event.preventDefault();

            const authToken = localStorage.getItem('auth-token');
            const requestBody = {
                name: this.productName,
                quantity: this.quantity,
                price: this.price,
                unit: this.unit,
                category_id: this.categoryId,
            };
            fetch(`http://localhost:8000/api/product`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': authToken// Add other headers if needed
                },
                body: JSON.stringify(requestBody),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Product added successfully:', data);
                    this.$router.push({ name: 'ManagerDashboard' });
                })
                .catch(error => {
                    console.error('Error updating product:', error);
                });
        },
    },
};
</script>
  