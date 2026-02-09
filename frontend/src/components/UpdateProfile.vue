<template>
  <div class="container mt-5" style="max-width: 500px;">
    <h3 class="mb-4 text-center">Update Profile</h3>
    <form @submit.prevent="updateProfile">
      <div class="mb-3">
        <label>Email</label>
        <input type="email" v-model="email_id" class="form-control" required>
      </div>
      <div class="mb-3">
        <label>Full Name</label>
        <input type="text" v-model="full_name" class="form-control" required>
      </div>
      <div class="mb-3">
        <label>Address</label>
        <textarea v-model="address" class="form-control" rows="2" required></textarea>
      </div>
      <div class="mb-3">
        <label>Pincode</label>
        <input type="text" v-model="pincode" class="form-control" required>
      </div>
      <button type="submit" class="btn btn-primary w-100">Save Changes</button>
      <router-link to="/dashboard" class="btn btn-warning">Back</router-link>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email_id: '',
      full_name: '',
      address: '',
      pincode: ''
    };
  },
  created() {
    this.loadProfile();
  },
  methods: {
    loadProfile() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:5000/profile', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(res => {
        const u = res.data;
        this.email_id = u.email_id;
        this.full_name = u.full_name;
        this.address = u.address;
        this.pincode = u.pincode || '';
      })
      .catch(err => {
        console.error("Error loading profile:", err);
      });
    },
    updateProfile() {
      const token = localStorage.getItem('token');
      axios.put('http://127.0.0.1:5000/profile/update', {
        email_id: this.email_id,
        full_name: this.full_name,
        address: this.address,
        pincode: this.pincode
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        alert("Profile updated successfully! , please login again.");
        localStorage.clear();
        this.$router.push('/login');
      })
      .catch(err => {
        console.error("Update failed:", err);
        alert("Failed to update profile.");
      });
    }
  }
};
</script>
