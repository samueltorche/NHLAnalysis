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
      <div class="col-4">
        <card title="Evolution des pénalités au fil des saisons" subTitle="">
          <LineChart :chartdata="chartPenaltiesData" :options="options" v-if="chartPenalties_loaded"/>
        </card>
      </div>
      <div class="col-4">
        <card title="Evolution des hits au fil des saisons" subTitle="">
          <LineChart :chartdata="chartHitsData" :options="options" v-if="chartHits_loaded"/>
        </card>
      </div>
      <div class="col-4">
        <card title="Evolution des bagarres au fil des saisons" subTitle="">
          <LineChart :chartdata="chartBagarresData" :options="options" v-if="chartBagarres_loaded"/>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-6">
        <card title="Evolution des buts des meilleurs joueurs" subTitle="">
          <LineChart :chartdata="chartPlayerData" :options="optionsButeurs" v-if="chartPlayerData_loaded"/>
        </card>
      </div>
      <div class="col-6">
        <card title="Evolution du temps de jeu des joueurs" subTitle="">
          <LineChart :chartdata="chartPlayerTimeData" :options="optionsTempsJeu" v-if="chartPlayerTimeData_loaded"/>
        </card>
      </div>
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
        chartButsData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPlayerData_loaded: false,
        chartPlayerData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPlayerTimeData_loaded: false,
        chartPlayerTimeData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartButs_loaded: false,
        chartShotsData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartHits_loaded: false,
        chartHitsData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartShots_loaded: false,
        chartBagarresData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartBagarres_loaded: false,
        chartPenaltiesData: {
          labels: ["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018", "2018-2019"],
          datasets: [{}]
        },
        chartPenalties_loaded: false,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Nombre moyen par match'
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Saison'
              }
            }],
          }
        },
        optionsButeurs: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Nombre de buts'
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Saison'
              }
            }],
          }
        },
        optionsTempsJeu: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Temps de jeu (en heure)'
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Saison'
              }
            }],
          }
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
      fetchData() {
        console.log("Fetch data ...");
        // GET AVG SEASON GOALS
        axios.get(this.$serverUrl + '/season/avg_goal').then(response => {
          console.log(response.data);
          let new_data = [
            Math.round(response.data[0].avg * 100) / 100,
            Math.round(response.data[1].avg * 100) / 100,
            Math.round(response.data[2].avg * 100) / 100,
            Math.round(response.data[3].avg * 100) / 100,
            Math.round(response.data[4].avg * 100) / 100,
            Math.round(response.data[5].avg * 100) / 100,
            Math.round(response.data[6].avg * 100) / 100,
            Math.round(response.data[7].avg * 100) / 100,
            Math.round(response.data[8].avg * 100) / 100,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de buts par match ",
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd",
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
            Math.round(response.data[0].shots_avg * 100) / 100,
            Math.round(response.data[1].shots_avg * 100) / 100,
            Math.round(response.data[2].shots_avg * 100) / 100,
            Math.round(response.data[3].shots_avg * 100) / 100,
            Math.round(response.data[4].shots_avg * 100) / 100,
            Math.round(response.data[5].shots_avg * 100) / 100,
            Math.round(response.data[6].shots_avg * 100) / 100,
            Math.round(response.data[7].shots_avg * 100) / 100,
            Math.round(response.data[8].shots_avg * 100) / 100,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de tirs par match",
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartShotsData, 'datasets', newvalue);
          this.chartShots_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        // GET AVG SEASON HITS
        axios.get(this.$serverUrl + '/season/avg_hits').then(response => {
          console.log(response.data);
          let new_data = [
            Math.round(response.data[0].hits_avg * 100) / 100,
            Math.round(response.data[1].hits_avg * 100) / 100,
            Math.round(response.data[2].hits_avg * 100) / 100,
            Math.round(response.data[3].hits_avg * 100) / 100,
            Math.round(response.data[4].hits_avg * 100) / 100,
            Math.round(response.data[5].hits_avg * 100) / 100,
            Math.round(response.data[6].hits_avg * 100) / 100,
            Math.round(response.data[7].hits_avg * 100) / 100,
            Math.round(response.data[8].hits_avg * 100) / 100,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de mises en échecs par match ",
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartHitsData, 'datasets', newvalue);
          this.chartHits_loaded = true;
        }).catch(error => {
          console.log(error);
        });
        //GET AVG NBR OF FIGHTS BY SEASON
        axios.get(this.$serverUrl + '/season/avg_fights').then(response => {
          console.log(response.data);
          let new_data = [
            Math.round(response.data[0].fights_avg * 100) / 100,
            Math.round(response.data[1].fights_avg * 100) / 100,
            Math.round(response.data[2].fights_avg * 100) / 100,
            Math.round(response.data[3].fights_avg * 100) / 100,
            Math.round(response.data[4].fights_avg * 100) / 100,
            Math.round(response.data[5].fights_avg * 100) / 100,
            Math.round(response.data[6].fights_avg * 100) / 100,
            Math.round(response.data[7].fights_avg * 100) / 100,
            Math.round(response.data[8].fights_avg * 100) / 100,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de bagarres par match",
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd",
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
            Math.round(response.data[0].penalties_avg * 100) / 100,
            Math.round(response.data[1].penalties_avg * 100) / 100,
            Math.round(response.data[2].penalties_avg * 100) / 100,
            Math.round(response.data[3].penalties_avg * 100) / 100,
            Math.round(response.data[4].penalties_avg * 100) / 100,
            Math.round(response.data[5].penalties_avg * 100) / 100,
            Math.round(response.data[6].penalties_avg * 100) / 100,
            Math.round(response.data[7].penalties_avg * 100) / 100,
            Math.round(response.data[8].penalties_avg * 100) / 100,
          ];
          let newvalue = [{
            data: new_data,
            label: "Moyenne de pénalités par match",
            borderColor: "#3e95cd",
            backgroundColor: "#3e95cd",
            fill: false
          }];
          this.$set(this.chartPenaltiesData, 'datasets', newvalue);
          this.chartPenalties_loaded = true;
        }).catch(error => {
          console.log(error);
        });

        // GET PLAYERS STATS
        axios.get(this.$serverUrl + '/player_stats')
          .then(response => {
            let players_data = []
            let goals = []
            let timeOnIce = []

            for (let s in response.data) {
              let players = response.data[s]
              for (let p in players) {
                let player = players[p][0]
                let pid = player['_id']
                players_data[pid] = {
                  "time": [],
                  "goals": [],
                  "color": ""
                }
              }
            }

            let colorBlindFriendly = [
              "rgb(230,159,0)",
              "rgb(86,180,233)",
              "rgb(0,158,115)",
              "rgb(240,228,66)",
              "rgb(0,114,178)",
              "rgb(213,94,0)",
              "rgb(204,121,167)"
            ];

            for (let s in response.data) {
              let players = response.data[s]
              let i = 0;
              for (let p in players) {
                let player = players[p][0]
                let pid = player['_id']
                players_data[pid]['time'].push(Math.round((player['timeOnIce']/3600)*100)/100)
                players_data[pid]['color'] = colorBlindFriendly[i]
                players_data[pid]['goals'].push(player['goals'])
                i++;
              }
            }

            console.log(players_data)

            let datas = []
            for (let p in players_data) {
              let player_data = players_data[p]
              let d = {
                "data": player_data['goals'],
                "label": p,
                "borderColor": player_data['color'],
                "backgroundColor": player_data['color'],
                "fill": false
              }
              datas.push(d)
            }

            this.$set(this.chartPlayerData, 'datasets', datas);
            this.chartPlayerData_loaded = true;

            datas = []
            for (let p in players_data) {
              let player_data = players_data[p]
              let d = {
                "data": player_data['time'],
                "label": p,
                "borderColor": player_data['color'],
                "backgroundColor": player_data['color'],
                "fill": false
              }
              datas.push(d)
            }

            this.$set(this.chartPlayerTimeData, 'datasets', datas);
            this.chartPlayerTimeData_loaded = true;

          })
      }
    }
  }
</script>

<style scoped>

</style>
