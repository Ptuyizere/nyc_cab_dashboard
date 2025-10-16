<template>
    <div class="summary">
        <div class="card">
            <p class="label">Total Number of Trips in 2016</p>
            <p class="value">{{ format_total_trips }}</p>
        </div>
        <div class="card">
            <p class="label">Total Average Speed (km/h)</p>
            <p class="value">{{ format_avg_speed }}</p>
        </div>
        <div class="card">
            <p class="label">Total Average Duration (s)</p>
            <p class="value">{{ format_avg_duration }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        stats: {
            type: Object,
            required: true
        }
    },
    computed: {
        format_total_trips() {
            return this.stats.total_trips;
        },
        format_avg_speed() {
            return this.stats.avg_speed_kmph.toFixed(2);
        },
        format_avg_duration() {
            return this.stats.avg_duration_s.toFixed(0);
        }
    }
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