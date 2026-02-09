<template>
  <div class="p-4">
    <h3 class="text-danger text-center mb-3">Search parking @location/pin code :</h3>
    <div class="text-center mb-4">
      <input v-model="query" @input="searchLots" class="form-control d-inline-block w-50" placeholder="e.g. Dadar Road or 400028" />
    </div>

    <div v-if="parkingLots.length" class="border p-3 rounded">
      <h4 class="text-primary text-center mb-3">Parking Lots @ {{ query }}</h4>
      <table class="table table-bordered text-center">
        <thead class="table-light">
          <tr>
            <th>ID</th>
            <th>Prime Location</th>
            <th>Price</th>
            <th>Pincode</th>
            <th>Address</th>
            <th>Availability</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lot in parkingLots" :key="lot.id">
            <td>{{ lot.id }}</td>
            <td>{{ lot.prime_location_name }}</td>
            <td>₹{{ lot.price }}</td>
            <td>{{ lot.pincode }}</td>
            <td>{{ lot.address }}</td>
            <td>{{ lot.availability }}</td>
            <td>
  <button class="btn btn-primary btn-sm" @click="bookLot(lot)">Book</button>
</td>

          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';



export default {
  name: "UserSearch",
  data() {
    return {
      query: '',
      parkingLots: []
    };
  },
  methods: {
  async searchLots() {
    if (this.query.length < 2) {
      this.parkingLots = [];
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const res = await axios.get(`http://127.0.0.1:5000/user/search`, {
        params: { query: this.query },
        headers: { Authorization: `Bearer ${token}` }
      });
      this.parkingLots = res.data;
    } catch (err) {
      console.error("Error searching parking lots:", err);
      this.parkingLots = [];
    }
  },

  bookLot(lot) {
  if (lot.availability <= 0) {
    alert("No available spots in this lot!");
    return;
  }

  const token = localStorage.getItem('token');
  if (!token) {
    alert("User not logged in!");
    return;
  }

  let email_id = "";
  try {
    const decoded = jwtDecode(token);
    email_id=decoded.sub;
  } catch (err) {
    console.error("Failed to decode token:", err);
    return;
  }

  this.$router.push({
    path: '/user/reserve',
    query: {
      lot_id: lot.id,
      email_id: email_id
    }
  });
}


}

};
</script>

<style scoped>
input {
  max-width: 300px;
}
</style>
