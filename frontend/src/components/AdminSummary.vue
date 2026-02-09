<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">Admin Summary</h2>

    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body">
            <h5 class="card-title">Total Reservations</h5>
            <p class="card-text h4">{{ summary.total_reservations }}</p>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card text-white bg-success mb-3">
          <div class="card-body">
            <h5 class="card-title">Total Revenue</h5>
            <p class="card-text h4">₹{{ summary.total_revenue.toFixed(2) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mb-5">
      <h4>Reservations by Location</h4>
      <canvas id="lotChart"></canvas>
    </div>

    <div class="mb-5">
      <h4>Reservations by Date</h4>
      <canvas id="dateChart"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
  name: 'AdminSummary',
  data() {
    return {
      summary: {
        total_reservations: 0,
        total_revenue: 0,
        reservations_by_lot: [],
        reservations_by_date: [],
      },
    };
  },
  methods: {
    async fetchSummary() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/admin/summary', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.summary = response.data;
        this.renderLotChart();
        this.renderDateChart();
      } catch (error) {
        console.error('Failed to fetch summary:', error);
      }
    },

    renderLotChart() {
      const labels = this.summary.reservations_by_lot.map(l => l.lot);
      const data = this.summary.reservations_by_lot.map(l => l.count);

      new Chart(document.getElementById('lotChart'), {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            label: 'Reservations per Location',
            data,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
          }],
        },
      });
    },

    renderDateChart() {
      const labels = this.summary.reservations_by_date.map(d => d.date);
      const data = this.summary.reservations_by_date.map(d => d.count);

      new Chart(document.getElementById('dateChart'), {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Reservations per Date',
            data,
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.3,
            fill: true,
          }],
        },
      });
    },
  },
  mounted() {
    this.fetchSummary();
  },
};
</script>

<style scoped>
.card {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
