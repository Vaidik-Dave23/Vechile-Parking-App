<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow rounded">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">👤 User Profile</h4>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center text-muted py-3">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <div v-else>
              <ul class="list-group list-group-flush">
                <li class="list-group-item"><strong>Email:</strong> {{ profile.email }}</li>
                <li class="list-group-item"><strong>Full Name:</strong> {{ profile.full_name }}</li>
                <li class="list-group-item"><strong>Address:</strong> {{ profile.address }}</li>
                <li class="list-group-item"><strong>Pincode:</strong> {{ profile.pincode }}</li>
              </ul>
            </div>
          </div>
          <div class="card-footer text-center">
            <router-link to="/profile/update" class="btn btn-warning">Update Profile</router-link>
            <router-link to="/dashboard" class="btn btn-secondary">Back to Dashboard</router-link>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
  return {
    token: "",
    profile: {},
    loading: true,
    error: ""
  };
},
  mounted() {
    this.loadToken();
    if (this.token) this.loadProfile();
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem("token");
      this.token = token ? token.replace(/^"|"$/g, "") : "";
    },
    loadProfile() {
  this.loading = true;
  axios
    .get("http://127.0.0.1:5000/profile", {
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Authorization": `Bearer ${this.token}`,
        
      }
    })
    .then((res) => {
      this.profile = res.data;
      this.loading = false;
    })
    .catch((err) => {
      this.error = "Failed to fetch user profile.";
      console.error("Error fetching user data:", err);
      this.loading = false;
    });
}
  }
}
</script>

<style scoped>
.card {
  border-radius: 1rem;
}

.card-header {
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}
</style>
