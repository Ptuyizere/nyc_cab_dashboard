<template>
    <div class="summary">
        <div class="card">
            <p class="label">Average Trip Speed for table data (km/h)</p>
            <p class="value">{{ avgSpeed.toFixed(2) }}</p>
        </div>
        <div class="card">
            <p class="label">Average Trip Duration for table data (s)</p>
            <p class="value">{{ avgDuration.toFixed(0) }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: ["trips"],
    computed: {
      avgSpeed() {
        let total = this.trips.reduce((sum, t) => sum + (t.speed_kmph || 0), 0);
        return this.trips.length ? total / this.trips.length : 0;
      },
      avgDuration() {
        let total = this.trips.reduce((sum, t) => sum + (t.trip_duration || 0), 0);
        return this.trips.length ? total / this.trips.length : 0;
      },
    },
};
</script>

<style scoped>
.summary {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1rem 0 2rem;
}

.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
    padding: 1rem 2rem;
    text-align: center;
    width: 200px;
}

.label {
    font-size: 0.9rem;
    color: #555;
}

.value {
    font-size: 1.4rem;
    font-weight: bold;
    margin-top: 0.3rem;
}
</style>