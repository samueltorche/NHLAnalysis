<script>
  import {HorizontalBar} from 'vue-chartjs'

  export default {
    name: "BarChart",
    extends: HorizontalBar,
    props: ['chartdata', 'options'],
    mounted() {
      this.renderChart(this.chartdata, this.options)
    }
  }
</script>

<style scoped>

</style>
