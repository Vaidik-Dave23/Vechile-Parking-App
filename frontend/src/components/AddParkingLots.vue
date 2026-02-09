<template>
  <div class="container mt-5" style="max-width: 600px;">
    <h3 class="text-center mb-4">New Parking Lot</h3>
    <form @submit.prevent="createParkingLot">
      <div class="mb-3">
        <label class="form-label">Prime Location Name</label>
        <input v-model="prime_location_name" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Address</label>
        <textarea v-model="address" class="form-control" rows="3" required></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Pincode</label>
        <input v-model="pincode" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Price (per hour)</label>
        <input v-model="price" type="number" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Maximum Spots</label>
        <input v-model="number_of_spots" type="number" class="form-control" required />
      </div>

      <!-- You can add more fields here -->

      <div class="d-flex justify-content-between">
        <button type="submit" class="btn btn-primary">Add</button>
        <button type="button" @click="backDash" class="btn btn-secondary">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      prime_location_name: '',
      address: '',
      pincode: '',
      price: '',
      number_of_spots: ''
    };
  },
  methods: {
    createParkingLot() {
      const token = localStorage.getItem('token');
      axios.post('http://127.0.0.1:5000/admin/parkinglot', {
        prime_location_name: this.prime_location_name,
        address: this.address,
        pincode: this.pincode,
        price: parseFloat(this.price),
        number_of_spots: parseInt(this.number_of_spots)
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        alert("Parking lot created successfully!");
        this.$router.push('/dashboard'); 
      })
      .catch(err => {
        console.error("Creation failed:", err);
        alert(err.response?.data?.message || "Failed to create parking lot.");
      });
    },
    backDash() {
      this.$router.push('/dashboard');
    }
  }
};
</script>
