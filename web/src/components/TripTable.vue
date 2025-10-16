<template>
  <div class="table-container">
    <table>
      <thead>
        <tr>
          <th>Trip ID</th>
          <th>Vendor ID</th>
          <th>Passengers</th>
          <th>Duration (s)</th>
          <th>Speed (km/h)</th>
          <th>Distance (km)</th>
          <th>Pickup</th>
          <th>Dropoff</th>
          <th>Round Trip?</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trip in trips" :key="trip.id">
          <td>{{ trip.numeric_id }}</td>
          <td>{{ trip.vendor_id }}</td>
          <td>{{ trip.passenger_count }}</td>
          <td>{{ trip.trip_duration }}</td>
          <td>{{ trip.speed_kmph?.toFixed(1) }}</td>
          <td>{{ trip.trip_distance_km }}</td>
          <td>{{ trip.pickup_datetime }}</td>
          <td>{{ trip.dropoff_datetime }}</td>
          <td :class="{
            'round_trip_true': trip.is_round_trip === true,
            'round_trip_false': trip.is_round_trip === false
            }">{{ trip.is_round_trip ? 'Yes' : 'No' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ["trips"],
};
</script>

<style scoped>
.table-container {
  overflow-x: auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
}
table {
  width: 100%;
  /*border-collapse: collapse;*/
}
th, td {
  padding: 0.6rem 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}
th {
  background-color: #f4f4f4;
  font-weight: 600;
}
tr:hover {
  background-color: #fafafa;
}

.round_trip_true {
  background-color: #c8f7c5;
  color: #056608;
  font-family: bold;
}

.round_trip_false {
  background-color: #ffcccc;
  color: #a10000;
  font-family: bold;
}

tr:hover {
  background-color: #f9f9f9;
}
</style>
