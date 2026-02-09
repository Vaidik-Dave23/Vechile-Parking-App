<template>
  <div class="container my-5">
    <div class="d-flex gap-2 mb-3">
      <select class="form-select w-auto" v-model="searchType">
        <option value="user">User</option>
        <option value="location">Location</option>
        <option value="spot">Spot</option>
      </select>
      <input v-model="query" type="text" class="form-control" placeholder="Search..." />
      <button class="btn btn-primary" @click="search">Search</button>
    </div>

    <div class="d-flex flex-wrap gap-3">
      <div v-for="item in results" :key="item.id" class="card p-3 shadow-sm" style="width: 300px;">
        <template v-if="searchType === 'user'">
          <h5>{{ item.full_name }}</h5>
          <p><strong>Email:</strong> {{ item.email_id }}</p>
          <p><strong>Address:</strong> {{ item.address }}</p>
          <p><strong>Pincode:</strong> {{ item.pincode }}</p>
          <p><strong>Admin:</strong> {{ item.is_admin ? 'Yes' : 'No' }}</p>
        </template>

        <template v-else-if="searchType === 'location'">
          <h5>{{ item.prime_location_name }}</h5>
          <p><strong>Address:</strong> {{ item.address }}</p>
          <p><strong>Pincode:</strong> {{ item.pincode }}</p>
          <p><strong>Price:</strong> ₹{{ item.price }}</p>
          <p><strong>Total Spots:</strong> {{ item.number_of_spots }}</p>
          <p><strong>Occupied:</strong> {{ item.occupied }}</p>
          <p><strong>Available:</strong> {{ item.available }}</p>
        </template>

        <template v-else-if="searchType === 'spot'">
          <h5>Spot ID: {{ item.id }}</h5>
          <p><strong>Parkinglot ID:</strong> {{ item.parkinglot_id }}</p>
          <p><strong>Available:</strong> {{ item.is_available ? 'Yes' : 'No' }}</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      searchType: 'user',
      query: '',
      results: []
    }
  },
  methods: {
    async search() {
      if (!this.query.trim()) return
      try {
        const token = localStorage.getItem("token")  // Ensure token is stored
        const res = await axios.get(`http://127.0.0.1:5000/admin/search`, {
          params: {
            type: this.searchType,
            query: this.query.trim()
          },
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.results = res.data.results
      } catch (err) {
        console.error(err)
        this.results = []
      }
    }
  }
}
</script>


<style scoped>
.card {
  border-radius: 15px;
  border: 1px solid #ccc;
}
</style>
