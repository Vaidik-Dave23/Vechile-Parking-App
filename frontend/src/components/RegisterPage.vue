<template>
    <div class="container mt-5" style="min-width: 300px; width: 100%; max-width: 400px;">
    <div class="card shadow p-4">
        <h1 class="mb-4 text-center">REGISTER</h1>
        <form  @submit.prevent="registerUser">
            <div class="form-group mb-3">
                <label for="email_id" class="form-label">Username/Email</label>
                <input type="email" v-model="email_id" required class="form-control">
            </div>
            <div class="form-group mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" v-model="password" required class="form-control">
            </div>
            <div class="form-group mb-3">
                <label for="FullName" class="form-label">Full Name</label>
                <input type="text" v-model="fullName" required class="form-control">
            </div>
            <div class="form-group mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" v-model="address" class="form-control">
            </div>
            <div class="form-group mb-3">
                <label for="pincode" class="form-label">pincode</label>
                <input type="number" v-model="pincode" class="form-control">
            </div>
            <div class="form-group text-center">
                <button type="submit" value="REGISTER" class="btn btn-primary ">REGISTER</button>
                <router-link to="/login" class="btn btn-warning mx-1 ">Already a user?</router-link>
            </div>
        </form>
    </div>
</div>
</template>
<script>
import axios from 'axios';
export default {
  name: "RegisterPage",
  data() {
    return {
      email_id: '',
      password: '',
      fullName: '',
      address: '',
      pincode: 0
    };
  },
  methods: {
    registerUser() {
        const formData = {
            email_id: this.email_id,
            password: this.password,
            full_name: this.fullName,
            address: this.address,
            pincode: this.pincode
        };
    
        res=axios.post('http://127.0.0.1:5000/register', formData, {
            headers: {
                'Content-Type': 'application/json'
            },
            withCredentials: true
        })
        .then(res => {
            console.log("Registration success:", res.data);
            alert("Registration successful! Please login.");
            this.$router.push('/login'); 
        })
    }
  }
};
</script>