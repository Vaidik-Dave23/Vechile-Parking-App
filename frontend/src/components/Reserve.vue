<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4 text-success">Reserve Your Parking</h2>

    <form @submit.prevent="reserveSpot" class="border p-4 rounded shadow-sm">
      <div class="mb-3">
        <label class="form-label">Lot ID</label>
        <input type="text" class="form-control" :value="lot_id" disabled />
      </div>

      <div class="mb-3">
        <label class="form-label">Email ID</label>
        <input type="text" class="form-control" :value="email_id" disabled />
      </div>

      <div class="mb-3">
        <label class="form-label">Vehicle Number</label>
        <input v-model="vehicle_number" class="form-control" required />
      </div>

      <div class="text-center mt-4">
        <button type="submit" class="btn btn-success me-2">Reserve</button>
        <button type="button" class="btn btn-secondary" @click="cancelReservation">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script>
import { jwtDecode } from 'jwt-decode';
import axios from 'axios';

export default {
  data() {
    return {
      lot_id: this.$route.query.lot_id,
      email_id: '',
      vehicle_number: ''
    };
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        this.email_id = decoded.sub;
      } catch (error) {
        console.error("Failed to decode token:", error);
      }
    }
  },
  methods: {
    async reserveSpot() {
      const token = localStorage.getItem('token');
      try {
        await axios.post(
          'http://127.0.0.1:5000/user/reserve',
          {
            lot_id: this.lot_id,
            vehicle_number: this.vehicle_number
          },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );
        alert("Reservation successful!");
        this.$router.push("/dashboard");
      } catch (err) {
        alert("Reservation failed.");
        console.error(err);
      }
    }
  }
};
</script>


<style scoped>
.container {
  max-width: 500px;
}
</style>
