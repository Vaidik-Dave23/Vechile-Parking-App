<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center">Edit Parking Lot</h2>

    <div v-if="loading">Loading parking lot details...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>
    <div v-else>
      <form @submit.prevent="updateLot">
        <div class="mb-3">
          <label class="form-label">Prime Location</label>
          <input type="text" class="form-control" v-model="lot.prime_location_name" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Address</label>
          <input type="text" class="form-control" v-model="lot.address" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input type="number" class="form-control" v-model="lot.pincode" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Price Per Hour</label>
          <input type="number" class="form-control" v-model="lot.price" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Number of Spots</label>
          <input type="number" class="form-control" v-model="lot.number_of_spots" required />
        </div>
        <button class="btn btn-primary">Update</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const lot = ref({});
    const loading = ref(true);
    const error = ref(null);

    const fetchLot = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:5000/admin/parkinglots/${route.params.lot_id}`, {
          headers: {
            
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        lot.value = res.data;
      } catch (err) {
        error.value = 'Failed to load parking lot.';
      } finally {
        loading.value = false;
      }
    };

    const updateLot = async () => {
      try {
        await axios.put(`http://127.0.0.1:5000/admin/parkinglots/${route.params.lot_id}`, lot.value, {
          headers: {
            // "content-type": "application/json",
            // "Access-Control-Allow-Origin": "*",
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert('Parking lot updated successfully!');
        router.push('/dashboard');
      } catch (err) {
        console.error('Update failed:', err.status);
        if (err.status==400){
          alert("Only unreserved spots can be deleted.");
          router.push('/dashboard');
        } else {
          alert('Failed to update parking lot. Please try again.');
          router.push('/dashboard');
        }
      }
    };

    onMounted(fetchLot);

    return { lot, loading, error, updateLot };
  }
};
</script>
