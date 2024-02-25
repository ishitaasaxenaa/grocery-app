<template>
    <div class="container mt-5">
        <h2 class="mb-4">Shop</h2>
        <div v-if="uniqueCategories.length > 0 && isManager">
            <ManagerPanel v-for="category in uniqueCategoriesUsers" :key="category.id" :id="category.id"
                :category="category" :products="getProductsByCategory(category)"></ManagerPanel>
        </div>
        <div v-else-if="uniqueCategoriesUsers.length > 0 && isManager === false">
            <CategoryPanel v-for="category in uniqueCategoriesUsers" :key="category" :category="category"
                :products="getProductsByCategory(category)"></CategoryPanel>
        </div>

        <!-- Add Category Popup -->
        <div v-if="showAddCategoryPopup" class="modal fade show" style="display: block; background: rgba(0,0,0,0.5);">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Add Category</h5>
                        <button type="button" class="close" @click="closeAddCategoryPopup">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitCategory">
                            <div class="form-group">
                                <label for="categoryName">Category Name</label>
                                <input type="text" class="form-control" id="categoryName" v-model="newCategoryName"
                                    required>
                            </div>
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import ManagerPanel from "@/components/ManagerPanel.vue";
import CategoryPanel from "@/components/CategoryPanel.vue";

export default {
    data() {
        return {
            products: [],
            query: this.$route.query.q,
            maxPrice: this.$route.query.max_price,
            isManager: Boolean,
        };
    },
    mounted() {
        this.searchProducts();
        this.getRole();
    },
    watch: {
        $route(to) {
    
            this.query = to.query.q;
            this.maxPrice = to.query.max_price;
            this.searchProducts();
        },
    },
    methods: {
        getRole(){
            if (localStorage.getItem("role") === '3') {
                this.isManager = true;
            }
            else {
                this.isManager = false;
            }
        },
        async searchProducts() {
            try {
                const authToken = localStorage.getItem("auth-token");
                let apiUrl = ''
                if (this.maxPrice === null || this.maxPrice === undefined || this.maxPrice === "") {
                    apiUrl = "http://localhost:8000/api/search?q=" + this.query;
                }
                else {
                    apiUrl = "http://localhost:8000/api/search?q=" + this.query + "&max_price=" + this.maxPrice;
                }
                const response = await fetch(apiUrl, {
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
    },
    computed: {
        uniqueCategories() {
            const categorySet = new Set();

            this.products.forEach(product => {
                categorySet.add({
                    id: product.category_id,
                    name: product.category
                });
            });

            return Array.from(categorySet);
        },
        uniqueCategoriesUsers(){
            console.log(Array.from(new Set(this.products.map(product => product.category))));
            return Array.from(new Set(this.products.map(product => product.category)));
        }
    },
    components: {
        ManagerPanel,
        CategoryPanel
    },
};
</script>