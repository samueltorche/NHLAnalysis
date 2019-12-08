<template>
  <div>
    <div class="row">
      <div class="col-6">
        <card title="Evolution des buts au fil des saisons" subTitle="">
          <LineChart :chartdata="chartButsData" :options="options" v-if="chartButs_loaded"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution du nombre de tirs au fil des saisons" subTitle="">
          <LineChart :chartdata="chartShotsData" :options="options" v-if="chartShots_loaded"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution des bagarres au fil des saisons" subTitle="">
          <LineChart :chartdata="chartBagarresData" :options="options" v-if="chartBagarres_loaded"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution des pénalités au fil des saisons" subTitle="">
          <LineChart :chartdata="chartPenaltiesData" :options="options" v-if="chartPenalties_loaded"/>
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
        <!--<BarChart :chartdata="chartRegularPlayoffData" :options="options" v-if="chartRegularPlayoffData != null"/>-->
        <RadarChart :chartdata="chartRegularPlayoffData" :options="options" v-if="chartRegularPlayoff_loaded"/>
      </card>
    </div>
    <div class="row">
      <div class="col-6">
        <card title="Evolution des buts des meilleurs joueurs" subTitle="">
          <LineChart :chartdata="chartPlayerData" :options="options" v-if="chartPlayerData_loaded"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution du temps de jeu des joueurs" subTitle="">
          <LineChart :chartdata="chartPlayerTimeData" :options="options" v-if="chartPlayerTimeData_loaded"/>
        </card>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import LineChart from '@/pages/LineChart.vue';
  import BarChart from '@/pages/BarChart.vue';
  import RadarChart from '@/pages/RadarChart.vue';

  export default {
    name: "Saisons",
    components: {
      LineChart,
      BarChart,
      RadarChart
    },
    data() {
      return {
        chartButsData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPlayerData_loaded: false,
        chartPlayerData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPlayerTimeData_loaded: false,
        chartPlayerTimeData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartButs_loaded: false,
        chartShotsData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartShots_loaded: false,
        chartBagarresData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartBagarres_loaded: false,
        chartPenaltiesData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPenalties_loaded: false,
        chartRegularPlayoffData: {
          labels: ["Moyenne de buts", "Mise en échecs", "Minutes de pénalités", "Nombre de tirs bloqués"],
          datasets: [{}]
        },
        chartRegularPlayoff_loaded: false,
        options: {
          responsive: true,
          maintainAspectRatio: false
        },
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
        console.log("Fetch data ...");
        // GET AVG SEASON GOALS
        axios.get(this.$serverUrl + '/season/avg_goal').then(response => {
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
          this.chartButs_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        // GET AVG SEASON SHOTS
        axios.get(this.$serverUrl + '/season/avg_shots').then(response => {
          console.log(response.data);
          let new_data = [
            response.data[0].shots_avg,
            response.data[1].shots_avg,
            response.data[2].shots_avg,
            response.data[3].shots_avg,
            response.data[4].shots_avg,
            response.data[5].shots_avg,
            response.data[6].shots_avg,
            response.data[7].shots_avg,
            response.data[8].shots_avg,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de tirs par match",
            borderColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartShotsData, 'datasets', newvalue);
          this.chartShots_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        //GET AVG NBR OF FIGHTS BY SEASON
        axios.get(this.$serverUrl + '/season/avg_fights').then(response => {
          console.log(response.data);
          let new_data = [
            response.data[0].fights_avg,
            response.data[1].fights_avg,
            response.data[2].fights_avg,
            response.data[3].fights_avg,
            response.data[4].fights_avg,
            response.data[5].fights_avg,
            response.data[6].fights_avg,
            response.data[7].fights_avg,
            response.data[8].fights_avg,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de bagarres par match",
            borderColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartBagarresData, 'datasets', newvalue);
          this.chartBagarres_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        //GET AVG PENALTIES PER SEASON
        axios.get(this.$serverUrl + '/season/avg_penalties').then(response => {
          console.log(response.data);
          let new_data = [
            response.data[0].penalties_avg,
            response.data[1].penalties_avg,
            response.data[2].penalties_avg,
            response.data[3].penalties_avg,
            response.data[4].penalties_avg,
            response.data[5].penalties_avg,
            response.data[6].penalties_avg,
            response.data[7].penalties_avg,
            response.data[8].penalties_avg,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de pénalités par match",
            borderColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartPenaltiesData, 'datasets', newvalue);
          this.chartPenalties_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        // GET PLAYOFF REGULAR COMPARAISON
        let labels = ['Goal', 'Penalty', 'Shot', 'Faceoff', 'Blocked Shot', 'Hit',"Interference"]
        axios.get(this.$serverUrl + '/games_plays/compare/20102011')
        .then(response => {
            let rp = response.data['RP']
            let pp = response.data['PP']
            let rp2 = response.data['RPSecondary']
            let pp2 = response.data['PPSecondary']

            let playoff_data = []
            let regular_data = []
            for(let idx in pp) {
              let p_line = pp[idx]
              let i = labels.indexOf(p_line['_id'])
              if(i>=0) {
                playoff_data[i] = p_line['count']
              }
            }
            for(let idx in rp) {
              let r_line = rp[idx]
              let i = labels.indexOf(r_line['_id'])
              if(i>=0) {
                regular_data[i] = r_line['count']
              }
            }

            for(let idx in rp2) {
              let r_line = rp2[idx]
              let i = labels.indexOf(r_line['_id'])
              if(i>=0) {
                regular_data[i] = r_line['count']
              }
            }

            for(let idx in pp2) {
              let r_line = pp2[idx]
              let i = labels.indexOf(r_line['_id'])
              if(i>=0) {
                playoff_data[i] = r_line['count']
              }
            }


            let new_data = [{
                data: regular_data,
                label: "Match régulier",
                borderColor: "#3e95cd",
                fill: false
              },
              {
                data: playoff_data,
                label: "Playoff",
                borderColor: "#7c0a02",
                fill: false
              }
            ]
            this.$set(this.chartRegularPlayoffData, 'datasets' , new_data);
            this.$set(this.chartRegularPlayoffData, 'labels' , labels);
            this.chartRegularPlayoff_loaded = true;
            

        })  // END AXIOS THEN 


        // GET PLAYERS STATS
        axios.get(this.$serverUrl + '/player_stats')
        .then(response => {
            let players_data = []
            let goals = []
            let timeOnIce = []

            for(let s in response.data){
              let players = response.data[s]
              for(let p in players) {
                let player = players[p][0]
                let pid = player['_id']
                players_data[pid] = {
                  "time": [], 
                  "goals": [],
                  "color": ""
                }
              }
            }

            var rcolor = function() {
              var r = Math.floor(Math.random() * 255);
              var g = Math.floor(Math.random() * 255);
              var b = Math.floor(Math.random() * 255);
              return "rgb(" + r + "," + g + "," + b + ")";
            }

            for(let s in response.data){
              let players = response.data[s]
              for(let p in players) {
                let player = players[p][0]
                let pid = player['_id']
                players_data[pid]['time'].push(
                player['timeOnIce'])
                players_data[pid]['color'] = rcolor()
                players_data[pid]['goals'].push(player['goals'])
              }
            }

            console.log(players_data)

            let datas = []
            for(let p in players_data){
              let player_data = players_data[p]
              let d = {
                "data": player_data['goals'],
                "label": p,
                "borderColor": player_data['color'],
                "fill": false
              }
              datas.push(d)
            }

            this.$set(this.chartPlayerData, 'datasets' , datas);
            this.chartPlayerData_loaded = true;

            datas = []
            for(let p in players_data){
              let player_data = players_data[p]
              let d = {
                "data": player_data['time'],
                "label": p,
                "borderColor": player_data['color'],
                "fill": false
              }
              datas.push(d)
            }

            this.$set(this.chartPlayerTimeData, 'datasets' , datas);
            this.chartPlayerTimeData_loaded = true;
            
        })



      }
    }
  }
</script>

<style scoped>

</style>
