<template>
  <div class="container text-center mt-5">
    <h2 class="mb-3">Release Reservation</h2>

    <div v-if="loading">Loading reservation details...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>
    <div v-else-if="reservation">
      <div class="card shadow p-4">
        <p><strong>Prime Location:</strong> {{ reservation.Prime_Location }}</p>
        <p><strong>Address:</strong> {{ reservation.address }}</p>
        <p><strong>Pincode:</strong> {{ reservation.pincode }}</p>
        <p><strong>Per Hour Price:</strong>{{ reservation.price_per_hour }}</p>
        <p><strong>Vehicle Number:</strong> {{ reservation.Vehicle_Number }}</p>
        <p><strong>Start Time:</strong> {{ reservation.start_time }}</p>
        <p><strong>End Time:</strong> {{ reservation.end_time || "Not Released Yet" }}</p>
        <p><strong>Duration:</strong> {{ reservation.duration_minutes }} minutes</p>
        <p><strong>Charges:</strong> ₹{{ reservation.cost || "Pending" }}</p>

        <button @click="releaseReservation" class="btn btn-danger mt-3">Confirm Release</button>
      </div>
    </div>
    <div v-else>
      <p class="text-muted">No reservation found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Release",
  data() {
    return {
      reservation: {},
      loading: true,
      error: null,
    };
  },
  methods: {
    async fetchReservation() {
      try {
        const id = this.$route.params.id;
        const response = await axios.get(`http://127.0.0.1:5000/reservations/${id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        
        this.reservation = response.data;
        this.loading = false;
      } catch (err) {
        this.error = "Reservation not found.";
        this.loading = false;
      }
    },
    async releaseReservation() {
      console.log("button clicked");
      try {
        const id = this.$route.params.id;
        const token = localStorage.getItem("token");
        const response = await axios.post(`http://127.0.0.1:5000/release/${id}`,null,{
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log("Release response:", response.data);
        alert(response.data.message);
        this.$router.push("/dashboard");
      } catch (err) {
        console.log(err);
        alert("Error releasing reservation.");
      }
    },
  },
  mounted() {
    this.fetchReservation();
  },
};
</script>

<style scoped>
.card {
  max-width: 500px;
  margin: 0 auto;
  border-radius: 1rem;
}
</style>
