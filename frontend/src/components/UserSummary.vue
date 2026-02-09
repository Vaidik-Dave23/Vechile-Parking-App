<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">User Summary</h2>

    <div v-if="loading">Loading summary...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>
    <div v-else>
      <div class="row mb-4">
        <div class="col-md-6">
          <div class="card text-center p-3 shadow-sm">
            <h5>Total Reservations</h5>
            <p class="display-6">{{ summary.total_reservations }}</p>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card text-center p-3 shadow-sm">
            <h5>Total Spent</h5>
            <p class="display-6">₹ {{ summary.total_spent.toFixed(2) }}</p>
          </div>
        </div>
      </div>

      <div class="card p-4 shadow-sm">
        <canvas id="reservationChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      summary: null,
      loading: true,
      error: null,
      chart: null
    };
  },
  methods: {
    async fetchSummary() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Authentication token not found.';
          return;
        }

        const response = await axios.get('http://127.0.0.1:5000/user/summary', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        this.summary = response.data;
        this.loading = false;
        this.$nextTick(this.renderChart);
      } catch (err) {
        this.error = 'Failed to load summary.';
        this.loading = false;
      }
    },
    renderChart() {
      if (this.chart) {
        this.chart.destroy();
      }

      const dates = this.summary.reservations_by_date.map(entry => entry.date);
      const counts = this.summary.reservations_by_date.map(entry => entry.count);

      const ctx = document.getElementById('reservationChart');
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: dates,
          datasets: [{
            label: 'Reservations by Date',
            data: counts,
            backgroundColor: 'rgba(54, 162, 235, 0.6)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              precision: 0
            }
          }
        }
      });
    }
  },
  mounted() {
    this.fetchSummary();
  }
};
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>
