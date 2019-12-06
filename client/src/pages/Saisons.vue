<template>
  <div class="row">
    <div class="col-12">
      <card title="Evolution des tirs au fil des saisons" subTitle="">
      <LineChart :chartdata="chartData" :options="options" v-if="chartData != null"/>
      </card>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import LineChart from '@/pages/LineChart.vue'

  export default {
    name: "Saisons",
    components: {
      LineChart
    },
    data() {
      return {
        chartData: null,
        options: null
      }
    },
    mounted() {
      this.chartData = {
        labels: [1500, 1600, 1700, 1750, 1800, 1850, 1900, 1950, 1999, 2050],
        datasets: [{
          data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
          label: "Africa",
          borderColor: "#3e95cd",
          fill: false
        }, {
          data: [282, 350, 411, 502, 635, 809, 947, 1402, 3700, 5267],
          label: "Asia",
          borderColor: "#8e5ea2",
          fill: false
        }
        ]
      };
      this.options = {
        responsive: true,
        maintainAspectRatio: false
      };
    },
    methods: {
      test() {
        console.log(this.$serverUrl);
        axios.get(this.$serverUrl + '/').then(response => {
          console.log(response.data);
        }).catch(error => {
          console.log(error);
        });
      }
    }
  }
</script>

<style scoped>

</style>
