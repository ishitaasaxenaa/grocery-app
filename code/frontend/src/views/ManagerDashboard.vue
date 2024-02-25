<template>
    <div class="container mt-5">
        <h2 class="mb-4">Shop</h2>
        <div v-if="uniqueCategories.length > 0">
            <ManagerPanel v-for="category in uniqueCategories" :key="category.id" :id="category.id"
                :category="category.name" :products="getProductsByCategory(category.name)"></ManagerPanel>
        </div>
        <button @click="openAddCategoryPopup" class="btn btn-info">
            <i class="fas fa-plus"></i> Request Changes in Category
        </button>

        <!-- Add Category Popup -->
        <div v-if="showAddCategoryPopup" class="modal" style="display: block; background: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Request Category</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                            @click="closeAddCategoryPopup"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitCategory">
                            <div class="form-group">
                                <label for="categoryName">Add a new Category</label>
                                <input type="text" class="form-control" id="categoryName" v-model="newCategoryName"
                                    required>
                            </div>
                            <button type="submit" class="btn btn-primary mt-1">Submit</button>
                        </form>
                        <hr>
                        <h5>Category List</h5>
                        <ul class="list-group">
                            <li v-for="category in uniqueCategories" :key="category.id"
                                class="list-group-item d-flex justify-content-between align-items-center">
                                {{ category.name }}
                                <div>
                                    <button type="button" class="btn btn-danger" style="margin-right:5px"
                                        @click="deleteItem(category.name, category.id)">Delete</button>
                                    <button type="button" class="btn btn-warning"
                                        @click="editItem(category.name, category.id)">Edit</button>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showDeleteCategory" class="modal" style="display: block; background: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete Category</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                            @click="closeDeleteCategory"></button>
                    </div>
                    <div class="modal-body">
                        <p>Are you sure you want to delete {{ selectedCategoryForDelete }}?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" @click="submitDeleteCategory">Yes</button>
                        <button type="button" class="btn btn-secondary" @click="closeDeleteCategory">No</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="showEditCategoryPopup" class="modal" style="display: block; background: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Category</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                        @click="closeEditCategoryPopup"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitEditCategory">
                        <div class="form-group">
                            <label for="editedCategoryName">Edit Category Name</label>
                            <input type="text" class="form-control" id="editedCategoryName" v-model="editedCategoryName"
                                required>
                        </div>
                        <button type="submit" class="btn btn-primary mt-1">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    </div>
</template>
<script>
import ManagerPanel from "@/components/ManagerPanel.vue";

export default {
    data() {
        return {
            products: [],
            showAddCategoryPopup: false,
            newCategoryName: "",
            uniqueCategories: [],
            showEditCategoryPopup: false,
            selectedCategoryForEdit: null,
            editedCategoryName: "",
            editedCategoryId: null,
            showDeleteCategory: false,
            selectedCategoryForDelete: null,
            selectedCategoryIdForDelete: null,
        };
    },
    mounted() {
        this.fetchProducts();
        this.getUniqueCategories();
    },
    methods: {
        async fetchProducts() {
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/allproducts", {
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

        openAddCategoryPopup() {
            this.showAddCategoryPopup = true;
        },

        closeAddCategoryPopup() {
            this.showAddCategoryPopup = false;
            this.newCategoryName = ""; // Clear the input field
        },
        editItem(categoryName, categoryId) {
            this.selectedCategoryForEdit = categoryName;
            this.editedCategoryId = categoryId;
            this.editedCategoryName = categoryName;
            this.showEditCategoryPopup = true;
        },

        openEditCategoryPopup() {
            this.showEditCategoryPopup = true;
        },

        closeEditCategoryPopup() {
            this.showEditCategoryPopup = false;
            this.selectedCategoryForEdit = null;
            this.editedCategoryName = "";
        },

        deleteItem(categoryName, categoryId) {
            this.selectedCategoryForDelete = categoryName;
            this.selectedCategoryIdForDelete = categoryId;
            this.showDeleteCategory = true;
        },

        openDeleteCategoryPopup() {
            this.showDeleteCategory = true;
        },

        closeDeleteCategoryPopup() {
            this.showDeleteCategory = false;
            this.selectedCategoryForDelete = null;
            this.selectedCategoryIdForDelete = null;
        },

        async submitDeleteCategory(){
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/category_approve", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": authToken,
                    },
                    body:JSON.stringify({
                        name: this.selectedCategoryForDelete,
                        action: 2,
                        categoryid: this.selectedCategoryIdForDelete,
                    })
                });

                if (response.ok){
                    console.log("Category deleted successfully");
                    this.closeDeleteCategoryPopup();
                    this.fetchProducts();
                } else {
                    console.error("Error deleting category:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error deleting category:", error);
            }
        },
        async submitEditCategory() {
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/category_approve", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": authToken,
                    },
                    body:JSON.stringify({
                        name: this.editedCategoryName,
                        action: 1,
                        categoryid: this.editedCategoryId,
                    })
                });

                if (response.ok) {
                    console.log("Category edited successfully");
                    this.closeEditCategoryPopup();
                    this.fetchProducts();
                } else {
                    console.error("Error editing category:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error editing category:", error);
            }
        },

        async submitCategory() {
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/category_approve", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": authToken,
                    },
                    body: JSON.stringify({ name: this.newCategoryName , action: 0, categoryid: null}),
                });

                if (response.ok) {
                    console.log("Category added successfully");
                    this.closeAddCategoryPopup();
                    this.fetchProducts();
                } else {
                    console.error("Error adding category:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error adding category:", error);
            }
        },
        async getUniqueCategories() {
            try {
                const authToken = localStorage.getItem("auth-token");
                const response = await fetch("http://localhost:8000/api/category", {
                    headers: {
                        "Authentication-Token": authToken,
                    },
                });

                if (response.ok) {
                    this.uniqueCategories = await response.json();
                    console.log("Fetched categories:", this.categories);
                } else {
                    console.error("Error fetching categories:", response.status, response.statusText);
                }
            } catch (error) {
                console.error("Error fetching categories", error);
            }
        }
    },

    components: {
        ManagerPanel
    },
};
</script>