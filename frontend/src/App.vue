<template>
<div class="main-container">
  <div class="d-flex flex-column min-vh-100" >

    <Navbar />
    <main class="flex-grow-1 d-flex justify-content-center align-items-center">
      <router-view />
    </main>
  </div>
</div>
</template>

<script>
import Navbar from './components/NavPage.vue';

export default {
  components: {
    Navbar,
  },
};
</script>
<!-- <style>
body, html {
  /* overflow: hidden; */
  /* height: 100%; */
}

</style> -->
