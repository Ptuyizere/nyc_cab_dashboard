<template>
  <div class="charts-container">
    <div class="chart-box">
      <h3>Average Trip Speed (km/h)</h3>
      <canvas id="speedChart"></canvas>
    </div>

    <div class="chart-box">
      <h3>Trip Duration Distribution (seconds)</h3>
      <canvas id="durationChart"></canvas>
    </div>
  </div>
</template>

<script>
import { onMounted, watch } from 'vue';
import {Chart, registerables} from "chart.js";

Chart.register(...registerables);

export default {
    props: ["trips"],
    setup(props) {
        let speedChartInstance = null;
        let durationChartInstance = null;

        function drawCharts() {
            let ctxSpeed = document.getElementById("speedChart").getContext("2d");
            let ctxDuration = document.getElementById("durationChart").getContext("2d");

            // remove existing charts first
            if (speedChartInstance) speedChartInstance.destroy();
            if (durationChartInstance) durationChartInstance.destroy();

            // speed chart
            let speeds = props.trips.map((t) => t.speed_kmph || 0);
            let distance = props.trips.map((t) => t.trip_distance_km);

            speedChartInstance = new Chart(ctxSpeed, {
                type: "line",
                data: {
                    labels: distance,
                    datasets: [
                        {
                            label: "Speed (km/h)",
                            data: speeds,
                            borderColor: "#007acc",
                            borderWidth: 2,
                            tension: 0.3,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {display: false}
                    },
                    scales: {
                        y: {beginAtZero: true},
                        x: {display: false}
                    }
                }
            });

            // Duration chart
            let durations = props.trips.map((t) => t.trip_duration);
            let bins = [0, 300, 600, 900, 1200, 1800, 2400, 3600];
            let counts = new Array(bins.length - 1).fill(0);

            for (let dur of durations) {
                for (let i = 0; i < bins.length - 1; i++) {
                    if (dur >= bins[i] && dur < bins[i + 1]) counts[i]++
                }
            }

            let labels = bins.slice(0, -1).map(
                (b, i) => `${bins[i] / 60}-${bins[i + 1] / 60} min`
            );

            durationChartInstance = new Chart(ctxDuration, {
                type: "bar",
                data: {
                    labels,
                    datasets: [
                        {
                            label: "Trips",
                            data: counts,
                            backgroundColor: "#42a5f5"
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {display: false}
                    },
                    scales: {
                        y: {beginAtZero: true}
                    }
                }
            });
        }

        onMounted(() => {
            if (props.trips.length) drawCharts();
        });

        watch(
            () => props.trips,
            (newTrips) => {
                if (newTrips.length) drawCharts();
            }
        );
    }
}
</script>

<style scoped>
.charts-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.chart-box {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.1);
  padding: 1rem 1.5rem;
  width: 450px;
  text-align: center;
}

canvas {
  max-width: 100%;
  height: 300px;
}
</style>