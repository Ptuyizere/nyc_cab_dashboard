<template>
  <div class="container">
    <h1>NYC Taxi Trips (2016)</h1>
    
    <AllDataStats :stats="stats" v-if="stats"/>
    <SummaryCards :trips="trips" v-if="trips.length" />
    <TripCharts :trips="trips" v-if="trips.length" />
    <TripTable :trips="trips" v-if="trips.length" />

    <Pagination
      :limit="limit"
      :offset="offset"
      @next="nextPage"
      @prev="prevPage"
    />

    <p v-if="loading" class="loading">Loading trips...</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { fetchPagedTrips, fetchAllTripsStats } from "../api";
import TripTable from "../components/TripTable.vue";
import Pagination from "../components/Pagination.vue";
import SummaryCards from "../components/SummaryCards.vue";
import TripCharts from "../components/TripCharts.vue";
import AllDataStats from "../components/AllDataStats.vue";

export default {
  components: { TripTable, Pagination, SummaryCards, TripCharts, AllDataStats },
  setup() {
    let trips = ref([]);
    let stats = ref(null)
    let limit = ref(10);
    let offset = ref(0);
    let loading = ref(false);
    let error = ref("");

    async function loadPagedTrips() {
      try {
        loading.value = true;
        let data = await fetchPagedTrips(limit.value, offset.value);
        trips.value = data;
      } catch (err) {
        error.value = "Failed to fetch trips.";
      } finally {
        loading.value = false;
      }
    }

    async function loadTripsStats() {
        try {
            loading.value = true;
            let data = await fetchAllTripsStats();
            stats.value = data;
        } catch (err) {
            error.value = "Failed to fetch trips stats.";
        } finally {
            loading.value = false;
        }
    }

    function nextPage() {
      offset.value += limit.value;
      loadPagedTrips();
    }

    function prevPage() {
      offset.value = Math.max(0, offset.value - limit.value);
      loadPagedTrips();
    }

    onMounted(() => {
      loadPagedTrips();
      loadTripsStats();
    });

    return { trips, stats, limit, offset, loading, error, nextPage, prevPage };
  },
};
</script>
