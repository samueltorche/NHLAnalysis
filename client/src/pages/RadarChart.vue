<script>
  import {Radar} from 'vue-chartjs'

  export default {
    name: "RadarChart",
    extends: Radar,
    props: ['chartdata', 'options'],
    mounted() {
      this.renderChart(this.chartdata, this.options)
    }
  }
</script>

<style scoped>

</style>
