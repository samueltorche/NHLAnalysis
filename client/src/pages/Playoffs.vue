<template>
  <div>
    <h4>Choisissez une saison:</h4>
    <select v-model="current_saison" v-on:change="updateRadarChart()" style="margin-bottom: 21px">
      <option v-for="saison in saisons_options" :value="saison.value">{{saison.text}}</option>
    </select>
    <div class="row">
      <div class="col-md-8">
        <card title="Comparaison match régulier vs playoff pour une saison">

          <!--<BarChart :chartdata="chartRegularPlayoffData" :options="options" v-if="chartRegularPlayoffData != null"/>-->
          <RadarChart :chartdata="chartRegularPlayoffData" :options="options" v-if="chartRegularPlayoff_loaded"/>
        </card>
      </div>
      <div class="col-md-4">
        <card title="Params">
          <div id='example-3'>
            <input type="checkbox" id="Goal" value="Goal" v-model="checkParams"
                   @change="handleChange($event)"><label for="Goal">Goal</label><br/>
            <input type="checkbox" id="Penalty" value="Penalty" v-model="checkParams"
                   @change="handleChange($event)"><label for="Penalty">Penalty</label><br/>
            <input type="checkbox" id="Shot" value="Shot" v-model="checkParams"
                   @change="handleChange($event)"><label for="Shot">Shot</label><br/>
            <input type="checkbox" id="Faceoff" value="Faceoff" v-model="checkParams"
                   @change="handleChange($event)"><label for="Faceoff">Faceoff</label><br/>
            <input type="checkbox" id="Blocked Shot" value="Blocked Shot" v-model="checkParams"
                   @change="handleChange($event)"><label for="Blocked Shot">Blocked Shot</label><br/>
            <input type="checkbox" id="Hit" value="Hit" v-model="checkParams"
                   @change="handleChange($event)"><label for="Hit">Hit</label><br/>
            <input type="checkbox" id="Interference" value="Interference" v-model="checkParams"
                   @change="handleChange($event)"><label for="Interference">Interference</label><br/>
            <input type="checkbox" id="Stoppage" value="Stoppage" v-model="checkParams"
                   @change="handleChange($event)"><label for="Stoppage">Stoppage</label><br/>
          </div>
        </card>
      </div>
    </div>
  </div>
</template>

<script>

  import RadarChart from '@/pages/RadarChart.vue';
  import axios from 'axios';

  export default {
    name: "Playoffs",
    components: {
      RadarChart
    },
    data() {
      return {
        checkParams: ['Goal', 'Penalty', "Shot", "Hit", "Faceoff"],
        chartRegularPlayoffData: {
          labels: ["Moyenne de buts", "Mise en échecs", "Minutes de pénalités", "Nombre de tirs bloqués"],
          datasets: [{}]
        },
        chartRegularPlayoff_loaded: false,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scale: {
            ticks: {
              display: false
            }
          }
        },
        saisons_options: [
          {value: '20102011', text: '2010-2011'},
          {value: '20112012', text: '2011-2012'},
          {value: '20122013', text: '2012-2013'},
          {value: '20132014', text: '2013-2014'},
          {value: '20142015', text: '2014-2015'},
          {value: '20152016', text: '2015-2016'},
          {value: '20162017', text: '2016-2017'},
          {value: '20172018', text: '2017-2018'},
          {value: '20182019', text: '2018-2019'}
        ],
        current_saison: "20182019"
      }
    },
    created() {
      this.fetchData()
    },
    watch: {
      // call again the method if the route changes
      '$route': 'fetchData'
    },
    methods: {
      handleChange: function (e) {
        this.updateRadarChart();
        this.$forceUpdate();
      },
      fetchData() {
        console.log("Fetch data ...");
        // GET PLAYOFF REGULAR COMPARAISON
        this.updateRadarChart();
      },
      updateRadarChart() {
        console.log("Updating chart.... " + this.current_saison);
        // GET PLAYOFF REGULAR COMPARAISON
        this.chartRegularPlayoff_loaded = false;
        let labels = this.checkParams;
        axios.get(this.$serverUrl + '/games_plays/compare/' + this.current_saison)
          .then(response => {
            let rp = response.data['RP'];
            let pp = response.data['PP'];
            let rp2 = response.data['RPSecondary'];
            let pp2 = response.data['PPSecondary'];

            let playoff_data = [];
            let regular_data = [];
            for (let idx in pp) {
              let p_line = pp[idx];
              let i = labels.indexOf(p_line['_id']);
              if (i >= 0) {
                playoff_data[i] = Math.round(p_line['count'] * 100) / 100
              }
            }
            for (let idx in rp) {
              let r_line = rp[idx];
              let i = labels.indexOf(r_line['_id']);
              if (i >= 0) {
                regular_data[i] = Math.round(r_line['count'] * 100) / 100
              }
            }

            for (let idx in rp2) {
              let r_line = rp2[idx];
              let i = labels.indexOf(r_line['_id']);
              if (i >= 0) {
                regular_data[i] = Math.round(r_line['count'] * 100) / 100
              }
            }

            for (let idx in pp2) {
              let r_line = pp2[idx];
              let i = labels.indexOf(r_line['_id']);
              if (i >= 0) {
                playoff_data[i] = Math.round(r_line['count'] * 100) / 100
              }
            }

            let new_data = [
              {
                data: regular_data,
                label: "Match régulier",
                borderColor: "#56B4E9",
                backgroundColor: "#56B4E9",
                fill: false
              },
              {
                data: playoff_data,
                label: "Playoff",
                borderColor: "#E69F00",
                backgroundColor: "#E69F00",
                fill: false
              }
            ];
            this.$set(this.chartRegularPlayoffData, 'datasets', new_data);
            this.$set(this.chartRegularPlayoffData, 'labels', labels);
            this.chartRegularPlayoff_loaded = true;
          });// END AXIOS THEN
      },
    }
  }
</script>

<style scoped>

</style>
