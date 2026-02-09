<template>
  <div class="login-wrapper p-4 bg-light shadow rounded" style="min-width: 300px; width: 100%; max-width: 400px;">
    <h2 class="text-center mb-4">Login</h2>
    <p class="err" v-if="error">{{ error }}</p>
    <form @submit.prevent="loginUser">
      <div class="mb-3">
        <label for="email_id" class="form-label">Email</label>
        <input v-model="formData.email_id" type="text" class="form-control" id="email_id" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="formData.password" type="password" class="form-control" id="password" required />
      </div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
      <router-link to="/register" class="btn btn-warning w-100">New User?</router-link>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
      email_id: '',
      password: ''
      },
      token: '',
      error: ''
    };
  },
  methods: {
    loginUser() {
      const formData = {
        email_id: '',
        password: ''
      };

      const response =axios.post("http://127.0.0.1:5000/login", JSON.stringify(this.formData), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
})
.then(res => {
  if(res.status==200){
    this.token = res.data.access_token;
    localStorage.setItem('token', this.token);
    this.$router.push('/dashboard'); 
  } else {
    this.error =res.response.data.message
  }
})
.catch(err => {
  console.log(err)
  console.error("Login failed:", err.response?.data || err.message);
  if(err.response && err.response.status === 401) {
    console.log(email_id, password);
    alert("Invalid credentials. Please try again.");

  } else {
    alert("An error occurred. Please try again later.");
  }
});

    }
  }
};
</script>

<style scoped>
.login-wrapper {
  background: white;
}
.err {
  color: red;
}

</style>
