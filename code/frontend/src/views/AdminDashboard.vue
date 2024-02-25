<!-- src/components/CategoryApprovals.vue -->

<template>
  <div class="container mt-4">
    <h2 class="mb-4">Pending Category Approvals</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Action</th>
          <th>Category ID</th>
          <th>Approve/ Deny</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="approval in approvals" :key="approval.id">
          <td>{{ approval.id }}</td>
          <td>{{ approval.name }}</td>
          <td>{{ getActionText(approval.action) }}</td>
          <td>{{ approval.categoryid }}</td>
          <td>
            <button v-if="approval.action === 0" @click="handleAction(approval.id, 'add')"
              class="btn btn-success">Approve</button>
            <button v-else-if="approval.action === 1" @click="handleAction(approval.id, 'edit')"
              class="btn btn-success">Approve</button>
            <button v-else-if="approval.action === 2" @click="handleAction(approval.id, 'delete')"
              class="btn btn-success">Approve</button>
          </td>
          <td>
            <button @click="deleteApproval(approval.id)" class="btn btn-danger">Deny</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="container mt-4">
    <h2 class="mb-4">Pending User Approvals</h2>
    <table class="table">
      <thead>
        <tr>
          <th>User Name</th>
          <th>Approve/ Deny</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.user_name }}</td>
          <td>
            <button @click="handleUserAction(user.user_id, user.id)" class="btn btn-success">Approve</button>
          </td>
          <td>
            <button @click="denyUserApproval(user.id)" class="btn btn-danger">Deny</button>
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="openAddCategoryPopup" class="btn btn-info">
      <i class="fas fa-plus"></i> Category Management
    </button>
  </div>

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
              <input type="text" class="form-control" id="categoryName" v-model="newCategoryName" required>
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
                <button type="button" class="btn btn-warning" @click="editItem(category.name, category.id)">Edit</button>
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
            @click="closeDeleteCategoryPopup"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete {{ selectedCategoryForDelete }}?</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="submitDeleteCategory">Yes</button>
          <button type="button" class="btn btn-secondary" @click="closeDeleteCategoryPopup">No</button>
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
          <form @submit.prevent="submitEditCategory()">
            <div class="form-group">
              <label for="editedCategoryName">Edit Category Name</label>
              <input type="text" class="form-control" id="editedCategoryName" v-model="editedCategoryName" required>
            </div>
            <button type="submit" class="btn btn-primary mt-1">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      approvals: [],
      users: [],
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
    this.fetchApprovals();
    this.getUserRequest();
    this.getUniqueCategories();
  },
  methods: {
    async fetchApprovals() {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch('http://localhost:8000/api/category_approve', {
          headers: {
            'Authentication-Token': authToken,
          },
        });
        const data = await response.json();
        this.approvals = data;
        console.log('Fetched approvals:', this.approvals);
      } catch (error) {
        console.error('Error fetching approvals', error);
      }
    },
    getActionText(action) {
      switch (action) {
        case 0:
          return 'Add';
        case 1:
          return 'Edit';
        case 2:
          return 'Delete';
        default:
          return 'Unknown';
      }
    },
    async handleAction(approvalId, actionType) {
      try {
        const authToken = localStorage.getItem('auth-token');
        let method = '';
        let endpoint = 'http://localhost:8000/api/category';
        let body = null;

        if (actionType === 'add') {
          method = 'POST';
          body = { name: this.approvals.find(approval => approval.id === approvalId).name };
        } else if (actionType === 'edit') {
          method = 'PUT';
          const existingCategory = this.approvals.find(approval => approval.id === approvalId);
          if (existingCategory) {
            endpoint += `?id=${existingCategory.categoryid}&name=${existingCategory.name}`;
          } else {
            console.error('Category not found for editing');
            return;
          }
        } else if (actionType === 'delete') {
          method = 'DELETE';
          const deletedCategory = this.approvals.find(approval => approval.id === approvalId).categoryid;
          endpoint += `?id=${deletedCategory}`;
        }

        const response = await fetch(endpoint, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': authToken,
          },
          // Add body for POST, PUT, and DELETE
          body: JSON.stringify(body),
        });

        if (response.ok) {
          this.deleteApproval(approvalId);
          console.log(`Category ${actionType} request successful`);
          this.fetchApprovals();
        } else {
          console.error(`Error ${actionType}ing category: ${response.statusText}`);
        }
      } catch (error) {
        console.error('Error handling action:', error);
      }
    },

    async deleteApproval(approvalId) {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch(`http://localhost:8000/api/category_approve?id=${approvalId}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': authToken,
          },
        });
        const data = await response.json();
        console.log('Deleted approval:', data);
        this.fetchApprovals();
      } catch (error) {
        console.error('Error deleting approval:', error);
      }
    },

    async getUserRequest() {
      try {
        const authToken = localStorage.getItem('auth-token');

        const response = await fetch('http://localhost:8000/api/manager_approval', {
          methods: 'GET',
          headers: {
            'Authentication-Token': authToken,
          },
        });
        const data = await response.json();
        this.users = data;
        console.log('Fetched user request:', data);
      } catch (error) {
        console.error('Error fetching user request', error);
      }
    },

    async handleUserAction(user_id, id) {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch("http://localhost:8000/api/checkrole", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authToken
          },
          body: JSON.stringify({
            user_id: user_id,
            role: "manager"
          })
        })

        if (response.ok) {
          console.log('User added to manager successfully');
          this.denyUserApproval(id);
        } else {
          console.error('Failed to add user to manager:', response.statusText);
        }
      }
      catch (error) {
        console.error('Error handling user action:', error);
      }
    },

    async denyUserApproval(id) {
      try {
        const authToken = localStorage.getItem('auth-token');
        const response = await fetch(`http://localhost:8000/api/manager_approval?id=${id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': authToken,
          },
        });
        const data = await response.json();
        console.log('Deleted approval:', data);
        this.getUserRequest();
      } catch (error) {
        console.error('Error deleting approval:', error);
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
    async submitEditCategory() {
      try {
        const authToken = localStorage.getItem("auth-token");
        const response = await fetch(`http://localhost:8000/api/category?id=${this.editedCategoryId}&name=${this.editedCategoryName}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authToken,
          },
          body: JSON.stringify({
            name: this.editedCategoryName,
          })
        });

        if (response.ok) {
          console.log("Category edited successfully");
          this.closeEditCategoryPopup();
          this.getUniqueCategories();
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
        const response = await fetch("http://localhost:8000/api/category", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authToken,
          },
          body: JSON.stringify({ name: this.newCategoryName }),
        });

        if (response.ok) {
          console.log("Category added successfully");
          this.closeAddCategoryPopup();
          this.getUniqueCategories();
          this.fetchProducts();
        } else {
          console.error("Error adding category:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Error adding category:", error);
      }
    },

    async submitDeleteCategory() {
      try {
        const authToken = localStorage.getItem("auth-token");
        const response = await fetch(`http://localhost:8000/api/category?id=${this.selectedCategoryIdForDelete}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": authToken,
          },

        });

        if (response.ok) {
          console.log("Category deleted successfully");
          this.getUniqueCategories();
          this.closeDeleteCategoryPopup();
          this.fetchProducts();
        } else {
          console.error("Error deleting category:", response.status, response.statusText);
        }
      } catch (error) {
        console.error("Error deleting category:", error);
      }
    },

  },
};
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
