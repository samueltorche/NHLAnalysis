<script>
  import {Line} from 'vue-chartjs'

  export default {
    name: "LineChart",
    extends: Line,
    props: ['chartdata', 'options'],
    mounted() {
      this.renderChart(this.chartdata, this.options)
    }
  }
</script>

<style scoped>

</style>
