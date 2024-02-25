<template>
    <div class="card mb-3">
        <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">Price: ${{ product.price }}</p>
            <p class="card-quantity">Quantity: {{ product.quantity }}</p>
            <p class="card-unit">Unit: {{ product.unit }}</p>
            <button @click="edit" class="btn btn-warning">Edit</button>
            <button @click="openDeleteConfirmation" class="btn btn-danger" style="margin-left: 5%">Delete</button>

            <!-- Delete Confirmation Modal -->
            <div v-if="showDeleteConfirmation" class="modal" style="display: block; background: rgba(0,0,0,0.5);">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Delete Product</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                                @click="closeDeleteConfirmation"></button>
                        </div>
                        <div class="modal-body">
                            <p>Are you sure you want to delete this product?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-danger" @click="deleteProduct">Yes</button>
                            <button type="button" class="btn btn-secondary" @click="closeDeleteConfirmation">No</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useProductStore } from '@/store/productStore';
export default {
    props: {
        product: Object,
    },

    data() {
        return {
            showDeleteConfirmation: false,
        };
    },

    methods: {
        edit() {
            const productStore = useProductStore();
            productStore.setEditingProduct(this.product);
            this.$router.push({ name: 'EditProduct', params: { id: this.product.id }});
        },

        openDeleteConfirmation() {
            this.showDeleteConfirmation = true;
        },

        closeDeleteConfirmation() {
            this.showDeleteConfirmation = false;
        },

        deleteProduct() {
            if (this.product) {
                const authToken = localStorage.getItem('auth-token');

                // Close the confirmation dialog
                this.closeDeleteConfirmation();

                // Proceed with deletion
                fetch(`http://localhost:8000/api/product?id=${this.product.id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authentication-Token': authToken,
                    },
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log('Product deleted successfully:', data);
                        window.location.reload();
                        this.$router.push({ name: 'ManagerDashboard' });
                    })
                    .catch(error => {
                        console.error('Error deleting product:', error);
                    });
            }
        },
    },
};
</script>

<style scoped></style>
