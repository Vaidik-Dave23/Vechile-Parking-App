<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4">
    <router-link class="navbar-brand" to="/">Parking System</router-link>

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">

        <!-- Not Logged In -->
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link to="/login" class="nav-link">Login</router-link>
        </li>
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link to="/register" class="nav-link">Register</router-link>
        </li>

        <!-- User Links -->
        <template v-if="isUser">
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/search" class="nav-link">Search</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/summary" class="nav-link">Summary</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/profile" class="nav-link">Profile</router-link>
          </li>
          <li class="nav-item">
            <button class="btn nav-link" @click="logout">Logout</button>
          </li>
        </template>

        <!-- Admin Links -->
        <template v-if="isAdmin">
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/users" class="nav-link">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/reservations" class="nav-link">Bookings</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/summary" class="nav-link">Summary</router-link>
          </li>
          <li class="nav-item">
            <button class="btn nav-link" @click="logout">Logout</button>
          </li>
        </template>

      </ul>
    </div>
  </nav>
</template>

<script>
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'NavPage',
  data() {
    return {
      email: ''
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token');
    },
    isAdmin() {
      return this.isLoggedIn && this.email === 'admin@email.com';
    },
    isUser() {
      return this.isLoggedIn && this.email !== 'admin@email.com';
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token); 
        this.email = decoded.sub;
      } catch (err) {
        console.error('Token decode failed:', err);
        this.email = '';
      }
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
};
</script>
<!-- 
<style scoped>
.navbar-nav .nav-link {
  margin-left: 0.8rem;
}

.btn.nav-link {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
}
</style> -->
