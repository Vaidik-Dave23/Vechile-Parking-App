<template>
  <div class="container-fluid forms">
    <div class="container text-center my-5">
      <div class="d-flex flex-column align-items-center">
        <!-- Use new URL for Vite asset resolution -->
        <div
          class="content mb-4"
          :style="{ backgroundImage: `url(${imageUrl})` }"
        ></div>
        <div>
          <router-link to="/login" class="btn btn-secondary mx-2">Login</router-link>
          <router-link to="/register" class="btn btn-success mx-2">Register</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Landing',
  data() {
    return {
      imageUrl: new URL('../assets/landing.png', import.meta.url).href,
    };
  },
};
</script>

<style scoped>
.content {
  background-size: cover;
  background-position: center;
  width: 100vw;         /* Nearly full viewport width */
  max-width: 700px;   /* Larger max width for big screens */
  height: 70vh;        /* Taller for more image area */
  border-radius: 32px;
  margin: 0 auto;
  box-shadow: 0 8px 48px rgba(0,0,0,0.14);
}
</style>