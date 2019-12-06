<template>
  <div>
    <div class="row">
      <div class="col-6">
        <card title="Evolution des buts au fil des saisons" subTitle="">
          <LineChart :chartdata="chartButsData" :options="options" v-if="chartButsData != null"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution du nombre de bagarres par saison" subTitle="">
          <LineChart :chartdata="chartBagarresData" :options="options" v-if="chartBagarresData != null"/>
        </card>
      </div>
    </div>
    <div class="row">
      <card title="Comparaison match régulier vs playoff pour une saison">
        Choisissez une saison:
        <select v-model="current_saison">
          <option>2010-2011</option>
          <option>2011-2012</option>
          <option>2012-2013</option>
          <option>2013-2014</option>
          <option>2014-2015</option>
          <option>2015-2016</option>
          <option>2016-2017</option>
          <option>2017-2018</option>
          <option selected>2018-2019</option>
        </select>
        <BarChart :chartdata="chartRegularPlayoffData" :options="options" v-if="chartRegularPlayoffData != null"/>
      </card>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import LineChart from '@/pages/LineChart.vue';
  import BarChart from '@/pages/BarChart.vue';

  export default {
    name: "Saisons",
    components: {
      LineChart,
      BarChart
    },
    data() {
      return {
        chartButsData: null,
        chartBagarresData: null,
        chartRegularPlayoffData: null,
        options: null,
        saisons_options: [
          {value: '2010', text: '2010-2011'},
          {value: '2011', text: '2011-2012'},
          {value: '2012', text: '2012-2013'},
          {value: '2013', text: '2013-2014'},
          {value: '2014', text: '2014-2015'},
          {value: '2015', text: '2015-2016'},
          {value: '2016', text: '2016-2017'},
          {value: '2017', text: '2017-2018'},
          {value: '2018', text: '2018-2019'}
        ],
        current_saison: "2018-2019"
      }
    },
    mounted() {
      this.chartButsData = {
        labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017"],
        datasets: [{
          data: [3.04, 2.13, 2.88, 3.14, 3.30, 3.55],
          label: "Moyenne de buts par match",
          borderColor: "#3e95cd",
          fill: false
        }
        ]
      };
      this.chartBagarresData = {
        labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017"],
        datasets: [{
          data: [279, 254, 248, 244, 220, 198],
          label: "Nombre de bagarres",
          borderColor: "#3e95cd",
          fill: false
        }
        ]
      };
      this.chartRegularPlayoffData = {
        labels: ["Moyenne de buts", "Mise en échecs", "Minutes de pénalités", "Nombre de tirs bloqués"],
        datasets: [{
          data: [279, 254, 248, 244],
          label: "Match régulier",
          borderColor: "#3e95cd",
          fill: false
        },
          {
            data: [279, 254, 248, 244],
            label: "Playoff",
            borderColor: "#3e95cd",
            fill: false
          }
        ]
      };
      this.options = {
        responsive: true,
        maintainAspectRatio: false
      };
    },
    created() {
      this.fetchData()
    },
    watch: {
      // call again the method if the route changes
      '$route': 'fetchData'
    },
    methods: {
      test() {
        console.log(this.$serverUrl);
        axios.get(this.$serverUrl + '/').then(response => {
          console.log(response.data);
        }).catch(error => {
          console.log(error);
        });
      },
      fetchData() {
        axios.get(this.$serverUrl + '/getAvgButs').then(response => {
          console.log(response.data);
          let new_data = [
            response.data[0].avg,
            response.data[1].avg,
            response.data[2].avg,
            response.data[3].avg,
            response.data[4].avg,
            response.data[5].avg,
            response.data[6].avg,
            response.data[7].avg,
            response.data[8].avg,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de buts par match",
            borderColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartButsData, 'datasets', newvalue);
        }).catch(error => {
          console.log(error);
        });
      }
    }
  }
</script>

<style scoped>

</style>
