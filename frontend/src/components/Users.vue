<template>
  <div class="container my-5">
    <h2 class="mb-4 text-center">All Users</h2>

    <div class="table-responsive">
      <table class="table table-striped table-hover shadow-sm rounded">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Email</th>
            <th>Address</th>
            <th>Pincode</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.pincode }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Users',
  data() {
    return {
      users: []
    };
  },
  mounted() {
    const token = localStorage.getItem('token');
    axios.get('http://127.0.0.1:5000/admin/users', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      this.users = response.data;
    })
    .catch(error => {
      console.error('Error loading users:', error);
    });
  }
};
</script>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}
</style>
