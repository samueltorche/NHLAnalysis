<template>
  <div>
    <h4>Choisissez une saison:</h4>

    <select v-model="current_saison" v-on:change="updateAll()" style="margin-bottom: 21px">
      <option v-for="saison in saisons_options" :value="saison.value">{{saison.text}}</option>
    </select>
    <br>
    <input type="checkbox" id="Normalize" value="Normalize" v-model="normalize"
           @change="handleChange($event)"><label for="Normalize">Normalize</label>
    <div class="row">
      <div class="col-12">
        <card title="Evolution du leaderboard" subTitle="">
          <LineChart :chartdata="chartEvoData" :options="optionLineChart" v-if="chartEvoData_loaded"/>
        </card>
      </div>
    </div>
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
            <input type="checkbox" id="Charging" value="Charging" v-model="checkParams"
                   @change="handleChange($event)"><label for="Charging">Charging</label><br/>
          </div>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6" v-if="playoff_ranking.length > 0">
        <main id="tournament">
          <ul class="round round-1">
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[7].top_wins }">
              {{playoff_ranking[7].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[7].top_wins }">
              {{playoff_ranking[7].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[8].top_wins }">
              {{playoff_ranking[8].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[8].top_wins }">
              {{playoff_ranking[8].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[9].top_wins }">
              {{playoff_ranking[9].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[9].top_wins }">
              {{playoff_ranking[9].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[10].top_wins }">
              {{playoff_ranking[10].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[10].top_wins }">
              {{playoff_ranking[10].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[11].top_wins }">
              {{playoff_ranking[11].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[11].top_wins }">
              {{playoff_ranking[11].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[12].top_wins }">
              {{playoff_ranking[12].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[12].top_wins }">
              {{playoff_ranking[12].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[13].top_wins }">
              {{playoff_ranking[13].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[13].top_wins }">
              {{playoff_ranking[13].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[14].top_wins }">
              {{playoff_ranking[14].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[14].top_wins }">
              {{playoff_ranking[14].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
          </ul>
          <ul class="round round-2">
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[3].top_wins }">
              {{playoff_ranking[3].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[3].top_wins }">
              {{playoff_ranking[3].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[4].top_wins }">
              {{playoff_ranking[4].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom " v-bind:class="{ winner: !playoff_ranking[4].top_wins }">
              {{playoff_ranking[4].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[5].top_wins }">
              {{playoff_ranking[5].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[2].top_wins }">
              {{playoff_ranking[5].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[6].top_wins }">
              {{playoff_ranking[6].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[6].top_wins }">
              {{playoff_ranking[6].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
          </ul>
          <ul class="round round-3">
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[1].top_wins }">
              {{playoff_ranking[1].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[1].top_wins }">
              {{playoff_ranking[1].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
            <li class="game game-top " v-bind:class="{ winner: playoff_ranking[2].top_wins }">
              {{playoff_ranking[2].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[2].top_wins }">
              {{playoff_ranking[2].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
          </ul>
          <ul class="round round-4">
            <li class="spacer">&nbsp;</li>
            <li class="game game-top" v-bind:class="{ winner: playoff_ranking[0].top_wins }">
              {{playoff_ranking[0].top_name}}
            </li>
            <li class="game game-spacer">&nbsp;</li>
            <li class="game game-bottom" v-bind:class="{ winner: !playoff_ranking[0].top_wins }">
              {{playoff_ranking[0].bot_name}}
            </li>
            <li class="spacer">&nbsp;</li>
          </ul>
        </main>
      </div>
    </div>
  </div>
</template>

<script>

  import RadarChart from '@/pages/RadarChart.vue';
  import LineChart from '@/pages/LineChart.vue';
  import axios from 'axios';

  export default {
    name: "Playoffs",
    components: {
      RadarChart,
      LineChart
    },
    data() {
      return {
        chartEvoData: {
          labels: [],
          datasets: [{}]
        },
        chartEvoData_loaded: false,
        normalize: false,
        regularData: [],
        playoffData: [],
        playoff_ranking: [],
        checkParams: ['Goal', 'Penalty', "Shot", "Hit", "Faceoff"],
        chartRegularPlayoffData: {
          labels: ["Moyenne de buts", "Mise en échecs", "Minutes de pénalités", "Nombre de tirs bloqués"],
          datasets: [{}]
        },
        chartRegularPlayoff_loaded: false,
        optionLineChart: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            xAxes: [{
              ticks: {
                autoSkip: true,
                maxTicksLimit: 10
              }
            }]
          }
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scale: {
            ticks: {
              display: false
            }
          },
          tooltips: {
            callbacks: {
              title: function (tooltipItems, data) {
                //Return value for title
                return '' + data.labels[tooltipItems[0].index];
              },
              label: function (tooltipItem, data) {
                var label = data.datasets[tooltipItem.datasetIndex].label || '';

                if (label) {
                  label += ': ';
                }
                label += data.datasets[tooltipItem.datasetIndex + 2].data[tooltipItem.index];
                return label;
              }
            }
          },
          legend: {
            labels: {
              filter: function (item, chart) {
                if (item.text.includes('1')) {
                  return false
                } else if (item.text.includes('2')) {
                  return false
                }
                return true
              }
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
        current_saison: "20182019",
      }
    },
    created() {
      this.fetchData()
    }
    ,
    watch: {
      // call again the method if the route changes
      '$route':
        'fetchData'
    }
    ,
    methods: {
      handleChange: function (e) {
        this.updateRadarChart();
        this.$forceUpdate();
      }
      ,
      fetchData() {
        console.log("Fetch data ...");
        // GET PLAYOFF REGULAR COMPARAISON
        this.updateRadarChart();
        this.updatePlayoffBracket();
        this.updateEvoChart()
      }
      ,
      updateEvoChart() {
        this.chartEvoData_loaded = false;
        axios.get(this.$serverUrl + '/season/' + this.current_saison + '/evolution')
          .then(response => {
            let values = []
            let labels = []


            let colorBlindFriendly = [
              "rgb(230,159,0)",
              "rgb(86,180,233)",
              "rgb(0,158,115)",
              "rgb(240,228,66)",
              "rgb(0,114,178)",
              "rgb(213,94,0)",
              "rgb(204,121,167)"
            ];

            let i = 0;
            let number_of_match = 0;
            for (let res in response.data) {
              number_of_match = response.data[res].length;
              let newvalue = {
                data: response.data[res],
                label: res,
                borderColor: colorBlindFriendly[i],
                backgroundColor: colorBlindFriendly[i],
                fill: false
              }
              values.push(newvalue)
              i++;
            }

            for (let i = 0; i < number_of_match; i++) {
              labels[i] = i + 1
            }

            this.$set(this.chartEvoData, 'labels', labels);
            this.$set(this.chartEvoData, 'datasets', values);
            this.chartEvoData_loaded = true;
          })
      }
      ,
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

            this.regularData = regular_data.slice();
            this.playoffData = playoff_data.slice();

            for (let i in playoff_data) {
              let r = regular_data[i]
              let p = playoff_data[i]

              /*
              if ( r>p) {
                p = 100 * p / r
                r = 100
              } else {
                r = 100 * r / p
                p = 100
              }*/

              if (this.normalize) {
                regular_data[i] = r / (r + p)
                playoff_data[i] = p / (r + p)
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
              },
              {
                data: this.regularData,
                label: "1",
                hidden: true
              },
              {
                data: this.playoffData,
                label: "2",
                hidden: true
              },
            ];
            this.$set(this.chartRegularPlayoffData, 'datasets', new_data);
            this.$set(this.chartRegularPlayoffData, 'labels', labels);
            this.chartRegularPlayoff_loaded = true;
          });// END AXIOS THEN
      }
      ,
      updatePlayoffBracket() {
        console.log("Updating playoff.... " + this.current_saison);
        //GET AVG NBR OF FIGHTS BY SEASON
        axios.get(this.$serverUrl + '/get_playoff/' + this.current_saison).then(response => {
          this.playoff_ranking = response.data;
        }).catch(error => {
          console.log(error);
        });
      }
      ,
      updateAll() {
        this.updateRadarChart();
        this.updatePlayoffBracket();
        this.updateEvoChart();
      }
    }
  }
</script>

<style scoped>
  /*
   *  Flex Layout Specifics
  */
  main {
    display: flex;
    flex-direction: row;
  }

  .round {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 200px;
    list-style: none;
    padding: 0;
  }

  .round .spacer {
    flex-grow: 1;
  }

  .round .spacer:first-child,
  .round .spacer:last-child {
    flex-grow: .5;
  }

  .round .game-spacer {
    flex-grow: 1;
  }

  /*
   *  General Styles
  */
  body {
    font-family: sans-serif;
    font-size: small;
    padding: 10px;
    line-height: 1.4em;
  }

  li.game {
    padding-left: 20px;
  }

  li.game.winner {
    font-weight: bold;
  }

  li.game span {
    float: right;
    margin-right: 5px;
  }

  li.game-top {
    border-bottom: 1px solid #aaa;
  }

  li.game-spacer {
    border-right: 1px solid #aaa;
    min-height: 40px;
  }

  li.game-bottom {
    border-top: 1px solid #aaa;
  }

</style>
