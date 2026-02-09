<template>
  <div v-if="token">
    <div v-if="role === 'admin'">
      <h2 class="mb-3 text-center">Admin Dashboard</h2>
      

      <div class="lot-container">
        <div v-for="lot in userData.parkinglots" :key="lot.id" class="parking-lot">
          <h3>{{ lot.prime_location_name }}</h3>
          <p>
            <strong>Address:</strong> {{ lot.address }}<br />
            <strong>Spots:</strong> {{ lot.number_of_spots }} total, {{ lot.available_spots }} available<br />
            <strong>Price:</strong> ₹{{ lot.price }}<br />
            <strong>Pincode:</strong> {{ lot.pincode }}
          </p>
          <div class="button-group">
            <button @click="UpdateLot(lot.id)">Edit</button>
            <button @click="DeleteLot(lot.id)">Delete</button>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <button @click="addLot" class="btn btn-primary">+ Add Lot</button>
      </div>
    </div>

    <div v-else-if="role === 'user'">
      <h2 class="mb-3 text-center">User Dashboard</h2>
      <h3>Recent Parking History</h3>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Location</th>
            <th>Vehicle No</th>
            <th>Timestamp</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in userData.parking_history" :key="record.id">
            <td>{{ record.id }}</td>
            <td>{{ record.location }}</td>
            <td>{{ record.vehicle_no }}</td>
            <td>{{ record.timestamp || 'Currently Parked' }}</td>
            <td>
              <router-link
                v-if="record.status === 'Release'"
                :to="`/user/release/${record.id}`"
                class="btn btn-sm btn-danger"
              >
                Release
              </router-link>
              <span v-else class="text-success">Parked Out</span>
            </td>
          </tr>
        </tbody>
      </table>
      <button @click="triggerExport" class="btn btn-primary">Export Parking History</button>



    </div>

    <div v-else>
      <p class="text-danger text-center">Unauthorized access</p>
      
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      token: "",
      role: "",
      userData: {},
    };
  },
  mounted() {
    this.loadToken();
    if (this.token) this.loadUser();
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem("token");
      this.token = token ? token.replace(/^"|"$/g, "") : "";
    },
    loadUser() {
      axios
        .get("http://127.0.0.1:5000/dashboard", {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        })
        .then((res) => {
          this.role = res.data.role;
          this.userData = res.data;
        })
        .catch((err) => {
          console.error("Error fetching user data:", err);
        });
    },
    addLot() {
      this.$router.push("/admin/parkinglot");
    },
    UpdateLot(lotId) {
      this.$router.push(`/admin/parkinglots/${lotId}`);
    },
    async releaseSpot(reservationId) {
      try {
        await axios.post(
          "http://127.0.0.1:5000/user/release",
          { reservation_id: reservationId },
          {
            headers: {
              Authorization: `Bearer ${this.token}`,
            },
          }
        );
        alert("Spot released successfully.");
        this.loadUser();
      } catch (err) {
        console.error("Release failed:", err);
        alert("Failed to release spot. Try again.");
      }
    },
    async DeleteLot(lotId) {
  if (!confirm("Are you sure you want to delete this parking lot?")) return;

  try {
    await axios.delete(`http://127.0.0.1:5000/admin/parkinglots/${lotId}`, {
      headers: {
        Authorization: `Bearer ${this.token}`
      }
    });

    alert("Parking lot deleted successfully.");
    this.loadUser();  // Refresh dashboard data

  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to delete the parking lot.";
    alert(msg);
    console.error("Delete error:", error);
  }


  },
  async triggerExport() {
    console.log("Export button clicked");
    try {
      await axios.get('http://127.0.0.1:5000/export_csv', {}, {
        headers: {
          Authorization: `Bearer ${this.token}`
        }
      });
      alert("Export started! You'll receive an email once done.");
    } catch (err) {
      alert("Error triggering export.");
      console.error(err);
    }
  },
}
  
};
</script>

<style scoped>
.lot-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.parking-lot {
  border: 1px solid #ccc;
  padding: 1rem;
  width: 280px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: white;
  text-align: center;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 1rem;
}

.release {
  color: red;
}

.parked-out {
  color: green;
}

table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 1rem;
}

th,
td {
  padding: 0.5rem;
  border: 1px solid #ddd;
  text-align: center;
}
</style>
