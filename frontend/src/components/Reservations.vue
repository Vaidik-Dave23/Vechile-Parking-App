<template>
  <div class="container my-5">
    <h2 class="mb-4 text-center">All Reservations</h2>
    <table class="table table-bordered table-hover shadow">
      <thead class="table-dark">
        <tr>
          <th>#</th>
          <th>User Name</th>
          <th>Email</th>
          <th>Vehicle Number</th>
          <th>Spot ID</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(res, index) in reservations" :key="res.id">
          <td>{{ index + 1 }}</td>
          <td>{{ res.user_name }}</td>
          <td>{{ res.email }}</td>
          <td>{{ res.vehicle_number }}</td>
          <td>{{ res.parking_spot_id }}</td>
          <td>{{ res.start_time }}</td>
          <td>{{ res.end_time }}</td>
          <td>{{ res.cost }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Reservations',
  data() {
    return {
      reservations: []
    };
  },
  mounted() {
    this.fetchReservations();
  },
  methods: {
    async fetchReservations() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/admin/reservations', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.reservations = response.data;
      } catch (error) {
        console.error('Failed to fetch reservations:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 95%;
}
</style>
