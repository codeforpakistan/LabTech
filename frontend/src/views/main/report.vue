 <style>
    #container {
      height: 850px;
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
      font-weight: 700;
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
import { readOverAllStatistics, readHospitalsStatistics,
        readAdminHospital, readHospitalDepartments } from '@/store/admin/getters';
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
      departmentId: 0,
    });
    this.calculateTotalSubmissions(false);
    this.constructSurveyChart(this.hospitalStatistics);
  }

  private reset() {
    this.selectedDepartment = {
      id: '',
      name: '',
    };
    this.select = {
      id: '',
      name: '',
    };
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
        departmentId: this.selectedDepartment.id,
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
        // hospitalStatistics[0].by_question = hospitalStatistics[0].by_question.sort((a, b) => 
        //   b.answer_true_perc - a.answer_true_perc);
        hospitalStatistics[0].by_question.forEach((each: any) => {
          if (each.question) {
            pdata.push([each.question, each.answer_true_perc, each.color, each.weightage]);
            ndata.push([each.question, -each.answer_false_perc, each.color, each.weightage]);
          }
        });
        console.log(pdata, 'pd', ndata, 'n')
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
                  fontSize: '9px',
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
              enabled: true,
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
            floor: -210,
          },
          xAxis: {
            labels: {
              enabled: true,
              style: {
                fontSize: '13px',
              },
              formatter () {
                const data = pdata.find(each => each[0] === this.value);
                return `<span style="color: ${data && data[2] ? data[2] : '#000000'}">${this.value.toString().toUpperCase()}</span>`
              }
            },
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
}
</script>
