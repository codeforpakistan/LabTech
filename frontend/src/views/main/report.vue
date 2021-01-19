 <style>
    #container {
        height: 400px;
    }

    .highcharts-data-table table {
      font-family: Verdana, sans-serif;
      border-collapse: collapse;
      border: 1px solid #EBEBEB;
      margin: 10px auto;
      text-align: center;
      width: 100%;
      max-width: 500px;
    }
    .highcharts-data-table caption {
        padding: 1em 0;
        font-size: 1.2em;
        color: #555;
    }
    .highcharts-data-table th {
      font-weight: 600;
        padding: 0.5em;
    }
    .highcharts-data-table td, .highcharts-data-table th, .highcharts-data-table caption {
        padding: 0.5em;
    }
    .highcharts-data-table thead tr, .highcharts-data-table tr:nth-child(even) {
        background: #f8f8f8;
    }
    .highcharts-data-table tr:hover {
        background: #f1f7ff;
    }
    .highcharts-figure, .highcharts-data-table table {
      min-width: 700px; 
      max-width: 1900px;
      margin: 1em auto;
    }

    #container {
        height: 660px;
    }

    .highcharts-data-table table {
      font-family: Verdana, sans-serif;
      border-collapse: collapse;
      border: 1px solid #EBEBEB;
      margin: 10px auto;
      text-align: center;
      width: 100%;
      max-width: 500px;
    }
    .highcharts-data-table caption {
        padding: 1em 0;
        font-size: 1.2em;
        color: #555;
    }
    .highcharts-data-table th {
      font-weight: 600;
        padding: 0.5em;
    }
    .highcharts-data-table td, .highcharts-data-table th, .highcharts-data-table caption {
        padding: 0.5em;
    }
    .highcharts-data-table thead tr, .highcharts-data-table tr:nth-child(even) {
        background: #f8f8f8;
    }
    .highcharts-data-table tr:hover {
        background: #f1f7ff;
    }
</style>
<template>
  <v-container>
    <v-container fluid>
      <p style="color: red">{{this.totalSubmissions > 0 ? '' : 'No submissions found to aggregate on.'}}</p>
      <v-row align="center">
        <v-col cols="6">
          <v-select
            v-model="select"
            v-on:change="changeValue"
            :items="hospitals"
            item-text="name"
            item-value="id"
            label="Select"
            persistent-hint
            return-object
            single-line
            clearable
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col cols="6">
          <v-select
            v-model="selectedDepartment"
            v-on:change="changeDepartment"
            :items="departments"
            item-text="name"
            item-value="id"
            label="Select"
            persistent-hint
            return-object
            single-line
            clearable
          ></v-select>
        </v-col>
      </v-row>
    </v-container>
    <figure class="highcharts-figure">
      <div id="container"></div>
    </figure>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import Highcharts from 'highcharts';
import drilldown from 'highcharts/modules/drilldown';
drilldown( Highcharts );
import { readOverAllStatistics, readHospitalsStatistics, readAdminHospital, readHospitalDepartments } from '@/store/admin/getters';
import { dispatchGetOverAllStatistics, dispatchGetHospitalStatistics,
        dispatchGetHospitals, dispatchGetHospitalDepartments} from '@/store/admin/actions';

@Component
export default class Reporting extends Vue {
  private select: any = '';
  private y: any;
  private series: any;
  private color: any;
  private key: any;
  private total: any;
  private selectedDepartment: any = '';
  private totalSubmissions: number = 0;
  private data() {
    return {
      select: '',
      items: [],
    };
  }

  get overAllStatistics() {
    return readOverAllStatistics(this.$store);
  }

  get hospitalStatistics() {
    return readHospitalsStatistics(this.$store);
  }

  get hospitals() {
    return readAdminHospital(this.$store);
  }

  get departments() {
    return readHospitalDepartments(this.$store);
  }

  private calculateTotalSubmissions(fallback) {
    this.totalSubmissions = this.hospitalStatistics && this.hospitalStatistics[0]
    && this.hospitalStatistics[0].total_submissions
    ? this.hospitalStatistics[0].total_submissions
    : fallback && this.overAllStatistics && this.overAllStatistics[0].total_submissions
      ? this.overAllStatistics && this.overAllStatistics[0].total_submissions
      : 0;
  }

  private async mounted() {
    await dispatchGetHospitals(this.$store);
    this.consturctOverAllStatistics();      
  }

  private async consturctOverAllStatistics() {
    await dispatchGetOverAllStatistics(this.$store);
    this.calculateTotalSubmissions(true);
    this.constructSurveyChart(this.overAllStatistics);
  }

  private async constructSelectedHospitalStatistics(hospital) {
    this.totalSubmissions = 0;
    this.selectedDepartment = {
      id: '',
      name: '',
    };
    await dispatchGetHospitalDepartments(this.$store, hospital.id);
    await dispatchGetHospitalStatistics(this.$store, {
      hospitalId: this.select.id, 
      departmentId: 0
    });
    this.calculateTotalSubmissions(false);
    this.constructSurveyChart(this.hospitalStatistics);
  }

  private reset() {
    this.selectedDepartment = {
      id: '',
      name: '',
    }
    this.select = {
      id: '',
      name: ''
    }
  }

  private async changeDepartment(value) {
    if (!value && !this.select.id) {
      this.reset();
      this.consturctOverAllStatistics();
      return;
    } else if (this.select.id && !value) {
      this.constructSelectedHospitalStatistics(this.select);
    } else {
      this.totalSubmissions = 0;
      await dispatchGetHospitalStatistics(this.$store, {
        hospitalId: this.select.id, 
        departmentId: this.selectedDepartment.id
      });
      this.calculateTotalSubmissions(false);
      this.constructSurveyChart(this.hospitalStatistics);
    }

  }

  private async changeValue(value) {
    if (!value) {
      this.reset();
      this.consturctOverAllStatistics();
      return;
    } else {
      this.constructSelectedHospitalStatistics(value);
    }
  }
  

  private constructSurveyChart(hospitalStatistics) {
    const vm = this;
    const pdata: any = [];
    const ndata: any = [];
    
    if (hospitalStatistics && hospitalStatistics[0] && hospitalStatistics[0].by_question) {
        hospitalStatistics[0].by_question.forEach((each: any) => {
          pdata.push([each.question, each.answer_true_perc]);
          ndata.push([each.question, -each.answer_false_perc]);
        });
        Highcharts.chart({
          chart: {
            renderTo: 'container',
            type: 'column',
            inverted: true,
          },
          plotOptions: {
            series: {
              stacking: 'normal',
              dataLabels: {
                style: {
                  fontSize: '8px',
                },
                format: '{y}%',
              },
            },
          },
          credits: {
            // href: 'http://www.bcogris.ca/sites/default/files/documents/RA2010-02' +
            // '_Public_Opinion_Survey_final-report_public_Feb_8_12.pdf',
            text: `<b>Total Survey Submissions  ${this.totalSubmissions}</b>`,
          },
          yAxis: {
            labels: {
              format: '{value}%',
              enabled: false,
            },
            stackLabels: {
              enabled: true,
              formatter: function() {
                return Math.abs(this.total) + '%';
              },
            },
            gridLineWidth: 0,
            title: {
              text: null,
            },
            floor: -80,
          },
          xAxis: {
            lineWidth: 0,
            tickLength: 0,
            type: 'category',
          },
          exporting: {
            enabled: false,
          },
          title: {
            text: `Each Survey Question Response by <b>${this.selectedDepartment.name ? this.select.name + ' '
            + this.selectedDepartment.name : this.select.name ? this.select.name : 'all hospitals'} ${this.selectedDepartment.name ? 'Department' : 'Departments'}</b>`,
          },
          tooltip: {
            formatter: function() {
              return '<span style="font-size: 10px">' + this.key + '</span><br/>' +
                '<span style="color:' + this.color + '">\u25CF </span>' + this.series.name + ': <b>'
                + Math.abs(this.y) + '%</b><br/>';
            },
          },
          series: [{
            type: 'column',
            index: 0,
            color: '#dd4532',
            name: 'Strongly Distrust',
            data: ndata,
           }, {
            type: 'column',
            index: 1,
            color: '#2eae94',
            name: 'Strongly Trust',
            data: pdata,
          }],
        });
    } else {
      // alert('error');
    }
  }

  // public constructCombinationChart(hospitalStatistics) {
  //   Highcharts.chart({
  //     chart: {
  //       renderTo: 'container',
  //     },
  //     title: {
  //         text: 'Combination chart'
  //     },
  //     xAxis: {
  //         categories: hospitalStatistics[0].by_question.map((each: any) => each.question)
  //     },
  //     labels: {
  //         items: [{
  //             html: 'Total fruit consumption',
  //             style: {
  //                 left: '50px',
  //                 top: '18px',
  //                 color: ( // theme
  //                     Highcharts.defaultOptions.title.style &&
  //                     Highcharts.defaultOptions.title.style.color
  //                 ) || 'black'
  //             }
  //         }]
  //     },
  //     series: [{
  //         type: 'column',
  //         name: 'Jane',
  //         data: [1]
  //     }, {
  //         type: 'column',
  //         name: 'John',
  //         data: [2, 3, 5, 7, 6]
  //     }, {
  //         type: 'column',
  //         name: 'Joe',
  //         data: [4, 3, 3, 9, 0]
  //     }, {
  //         type: 'spline',
  //         name: 'Average',
  //         data: [3, 2.67, 3, 6.33, 3.33],
  //         marker: {
  //             lineWidth: 2,
  //             lineColor: Highcharts.getOptions().colors[3],
  //             fillColor: 'white'
  //         }
  //     }, {
  //         type: 'pie',
  //         name: 'Total consumption',
  //         data: [{
  //             name: 'Jane',
  //             y: 13,
  //             color: Highcharts.getOptions().colors[0] // Jane's color
  //         }, {
  //             name: 'John',
  //             y: 23,
  //             color: Highcharts.getOptions().colors[1] // John's color
  //         }, {
  //             name: 'Joe',
  //             y: 19,
  //             color: Highcharts.getOptions().colors[2] // Joe's color
  //         }],
  //         center: [100, 80],
  //         size: 100,
  //         showInLegend: false,
  //         dataLabels: {
  //             enabled: false
  //         }
  //     }]
  //   });

  // }

  // public constructBarChart() {
  //    Highcharts.chart({
  //     chart: {
  //       renderTo: 'container',
  //       type: 'column'
  //     },
  //     title: {
  //       text: 'Browser market shares. January, 2018'
  //     },
  //     subtitle: {
  //       text: 'Click the columns to view versions. Source:
  //        <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
  //     },
  //     accessibility: {
  //       announceNewData: {
  //           enabled: true
  //       }
  //     },
  //     xAxis: {
  //       type: 'category'
  //     },
  //     yAxis: {
  //       title: {
  //           text: 'Total percent market share'
  //       }
  //     },
  //     legend: {
  //        enabled: false
  //     },
  //     plotOptions: {
  //       series: {
  //         borderWidth: 0,
  //         dataLabels: {
  //             enabled: true,
  //             format: '{point.y:.1f}%'
  //         }
  //       }
  //     },
  //     tooltip: {
  //         headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
  //         pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
  //     },
  //     series: [
  //       {
  //         name: "Browsers",
  //         colorByPoint: true,
  //         data: [
  //             {
  //                 name: "Chrome",
  //                 y: 62.74,
  //                 drilldown: "Chrome"
  //             },
  //             {
  //                 name: "Firefox",
  //                 y: 10.57,
  //                 drilldown: "Firefox"
  //             },
  //             {
  //                 name: "Internet Explorer",
  //                 y: 7.23,
  //                 drilldown: "Internet Explorer"
  //             },
  //             {
  //                 name: "Safari",
  //                 y: 5.58,
  //                 drilldown: "Safari"
  //             },
  //             {
  //                 name: "Edge",
  //                 y: 4.02,
  //                 drilldown: "Edge"
  //             },
  //             {
  //                 name: "Opera",
  //                 y: 1.92,
  //                 drilldown: "Opera"
  //             },
  //             {
  //                 name: "Other",
  //                 y: 7.62,
  //                 drilldown: null
  //             }
  //         ]
  //       }
  //     ],
  //     drilldown: {
  //         series: [
  //             {
  //                 name: "Chrome",
  //                 id: "Chrome",
  //                 data: [
  //                     [
  //                         "v65.0",
  //                         0.1
  //                     ],
  //                     [
  //                         "v64.0",
  //                         1.3
  //                     ],
  //                     [
  //                         "v63.0",
  //                         53.02
  //                     ],
  //                     [
  //                         "v62.0",
  //                         1.4
  //                     ],
  //                     [
  //                         "v61.0",
  //                         0.88
  //                     ],
  //                     [
  //                         "v60.0",
  //                         0.56
  //                     ],
  //                     [
  //                         "v59.0",
  //                         0.45
  //                     ],
  //                     [
  //                         "v58.0",
  //                         0.49
  //                     ],
  //                     [
  //                         "v57.0",
  //                         0.32
  //                     ],
  //                     [
  //                         "v56.0",
  //                         0.29
  //                     ],
  //                     [
  //                         "v55.0",
  //                         0.79
  //                     ],
  //                     [
  //                         "v54.0",
  //                         0.18
  //                     ],
  //                     [
  //                         "v51.0",
  //                         0.13
  //                     ],
  //                     [
  //                         "v49.0",
  //                         2.16
  //                     ],
  //                     [
  //                         "v48.0",
  //                         0.13
  //                     ],
  //                     [
  //                         "v47.0",
  //                         0.11
  //                     ],
  //                     [
  //                         "v43.0",
  //                         0.17
  //                     ],
  //                     [
  //                         "v29.0",
  //                         0.26
  //                     ]
  //                 ]
  //             },
  //             {
  //                 name: "Firefox",
  //                 id: "Firefox",
  //                 data: [
  //                     [
  //                         "v58.0",
  //                         1.02
  //                     ],
  //                     [
  //                         "v57.0",
  //                         7.36
  //                     ],
  //                     [
  //                         "v56.0",
  //                         0.35
  //                     ],
  //                     [
  //                         "v55.0",
  //                         0.11
  //                     ],
  //                     [
  //                         "v54.0",
  //                         0.1
  //                     ],
  //                     [
  //                         "v52.0",
  //                         0.95
  //                     ],
  //                     [
  //                         "v51.0",
  //                         0.15
  //                     ],
  //                     [
  //                         "v50.0",
  //                         0.1
  //                     ],
  //                     [
  //                         "v48.0",
  //                         0.31
  //                     ],
  //                     [
  //                         "v47.0",
  //                         0.12
  //                     ]
  //                 ]
  //             },
  //             {
  //                 name: "Internet Explorer",
  //                 id: "Internet Explorer",
  //                 data: [
  //                     [
  //                         "v11.0",
  //                         6.2
  //                     ],
  //                     [
  //                         "v10.0",
  //                         0.29
  //                     ],
  //                     [
  //                         "v9.0",
  //                         0.27
  //                     ],
  //                     [
  //                         "v8.0",
  //                         0.47
  //                     ]
  //                 ]
  //             },
  //             {
  //                 name: "Safari",
  //                 id: "Safari",
  //                 data: [
  //                     [
  //                         "v11.0",
  //                         3.39
  //                     ],
  //                     [
  //                         "v10.1",
  //                         0.96
  //                     ],
  //                     [
  //                         "v10.0",
  //                         0.36
  //                     ],
  //                     [
  //                         "v9.1",
  //                         0.54
  //                     ],
  //                     [
  //                         "v9.0",
  //                         0.13
  //                     ],
  //                     [
  //                         "v5.1",
  //                         0.2
  //                     ]
  //                 ]
  //             },
  //             {
  //                 name: "Edge",
  //                 id: "Edge",
  //                 data: [
  //                     [
  //                         "v16",
  //                         2.6
  //                     ],
  //                     [
  //                         "v15",
  //                         0.92
  //                     ],
  //                     [
  //                         "v14",
  //                         0.4
  //                     ],
  //                     [
  //                         "v13",
  //                         0.1
  //                     ]
  //                 ]
  //             },
  //             {
  //                 name: "Opera",
  //                 id: "Opera",
  //                 data: [
  //                     [
  //                         "v50.0",
  //                         0.96
  //                     ],
  //                     [
  //                         "v49.0",
  //                         0.82
  //                     ],
  //                     [
  //                         "v12.1",
  //                         0.14
  //                     ]
  //                 ]
  //             }
  //         ]
  //     }
  //   });
  // }
}
</script>
