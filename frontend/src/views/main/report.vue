 <style>
  #container {
    height: 850px;
  }
  .highcharts-credits {
    display: none;
  }
  text.highcharts-subtitle {
    color: #666666 !important;
    font-weight: bold !important;
    fill: #383131 !important;
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
    <template>
      <v-container fluid style="padding: 10px 0px;">
      <v-layout row xs12>
        <v-flex md6 style="padding-right: 10px">
          <v-select :items="labOpts" v-model="selectedLab" label="Lab Name" dense></v-select>
        </v-flex>
        <v-flex md6 style="padding-left: 10px" v-if="loadedSubmissionNumber && labSubmissionNumbers">
          <v-select :items="labSubmissionNumbers.submission_nos" @change="fetchAccumulative" v-model="selectedSubmission"  filled label="Submission Number" dense></v-select>
        </v-flex>
      </v-layout>
      </v-container>
      <div  v-if="loadedSubmissionNumber && byLabReportAccumulative">
        <div v-for="item in byLabReportAccumulative" :key="item.naame">
          <div class="mt-2" style="display: flex; justify-content: space-between; width: 340px;">
            <div><b>{{item.name}}</b></div>
            <div>{{roundOff(item.data.score)}}</div>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <vue-excel-editor ref="editor" width="400px" :readonly="true" v-model="item.data.indicators" :localized-label="myLabels"></vue-excel-editor>
            <highcharts style="margin-top: -20px;" :options="getHighchartData(item)"></highcharts>
          </div>
        </div>
      </div>
    </template>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import Highcharts from 'highcharts';
import drilldown from 'highcharts/modules/drilldown';
import VueExcelEditor from 'vue-excel-editor';
Vue.use(VueExcelEditor);
drilldown( Highcharts );
import { readOverAllStatistics, readHospitalsStatistics, readlabSubmissionNumbers,
  readAdminHospital, readHospitalDepartments, readByLabReport, readbyLabReportAccumulative } from '@/store/admin/getters';
import { dispatchGetOverAllStatistics, dispatchGetHospitalStatistics, dispatchGetByLabReport, dispatchGetByLabReportAccumulative,
        dispatchGetHospitals, dispatchGetHospitalDepartments, dispatchGetLabSubmissions, } from '@/store/admin/actions';
import { readUserProfile } from '@/store/main/getters';

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
  private submissionOptions: any = [];
  private selectedLab: any = '';
  private selectedSubmission: any = 0;
  private jsondata: any = [];
  private loadedSubmissionNumber: any = false;
  private barChartOptionsTemplate: any = {
    chart: {
      type: 'bar',
      height: 170,
    },
    subtitle: {
      text: '',
    },
    title: {
      text: ''
    },
    series: [{
      showInLegend: false,
      data: []
    }],
    xAxis: {
      categories: [],
      title: {
        text: 'Categories'
      }
    },
    tooltip: {
      shared: true,
      enabled: true,
      valueDecimals: 2,
    },
    yAxis: {
      min: 0,
      max: 100,
      title: {
        text: 'Score',
      },
    },
  };
  private data() {
    return {
      select: '',
      items: [],
      myLabels:  {
        footerLeft: (top, bottom, total) => `Record ${top} to ${bottom} of ${total}`,
        first: 'First',
        previous: 'Previous',
        next: 'Next',
        last: 'Last',
        footerRight: {
            selected: 'Selected:',
            filtered: 'Filtered:',
            loaded: 'Loaded:',
        },
        processing: 'Processing',
        tableSetting: 'Table Setting',
        exportExcel: 'Export Excel',
        importExcel: 'Import Excel',
        back: 'Back',
        reset: 'Default',
        sortingAndFiltering: 'Sorting And Filtering',
        sortAscending: 'Sort Ascending',
        sortDescending: 'Sort Descending',
        near: '≒ Near',
        exactMatch: '= Exact Match',
        notMatch: '≠ Not Match',
        greaterThan: '&gt; Greater Than',
        greaterThanOrEqualTo: '≥ Greater Than or Equal To',
        lessThan: '&lt; Less Than',
        lessThanOrEqualTo: '≤ Less Than Or Equal To',
        regularExpression: '~ Regular Expression',
        customFilter: 'Custom Filter',
        listFirstNValuesOnly: (n) => `List first ${n} values only`,
        apply: 'Apply',
        noRecordIsRead: 'No record is read',
        readonlyColumnDetected: 'Readonly column detected',
        columnHasValidationError: (name, err) => `Column ${name} has validation error: ${err}`,
        noMatchedColumnName: 'No matched column name',
        invalidInputValue: 'Invalid input value',
        missingKeyColumn: 'Missing key column',
        noRecordIndicator: 'No record',
      },
    };
  }

  getHighchartData(data: any) {
    let chartData: any = JSON.parse(JSON.stringify(this.barChartOptionsTemplate))
    data.data.indicators.forEach(item => {
      console.log('item', item);
      chartData.series[0].data.push(parseFloat(item.Score));
      chartData.xAxis.categories.push(item.Indicator);
    });
    chartData.subtitle.text = data.name;
    return chartData;
  } 

  roundOff(num) {		
		return num.toFixed(2);
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

  get byLabReport() {
    return readByLabReport(this.$store);
  }

  get byLabReportAccumulative() {
    return readbyLabReportAccumulative(this.$store);
  }

  get labSubmissionNumbers() {
    return readlabSubmissionNumbers(this.$store);
  }

  private calculateTotalSubmissions(fallback) {
    this.totalSubmissions = this.hospitalStatistics && this.hospitalStatistics[0]
    && this.hospitalStatistics[0].total_submissions
    ? this.hospitalStatistics[0].total_submissions
    : fallback && this.overAllStatistics && this.overAllStatistics[0]
      && this.overAllStatistics[0].total_submissions
      ? this.overAllStatistics && this.overAllStatistics[0].total_submissions
      : 0;
  }

  private refactorByLabReport() {
    console.log('this.byLabReport', this.byLabReport);
    console.log('this.byLabReportAccumulative = ', this.byLabReportAccumulative);
    console.log('this.labSubmissionNumbers = ', this.labSubmissionNumbers);
    this.selectedLab = 'Islamabad Diagnostic Centre';
  }

  get labOpts() {
    return this.hospitals.map((x: any) => x.name);
  }

  private async mounted() {
    await dispatchGetHospitals(this.$store);
    this.consturctOverAllStatistics();
    this.selectedLab = this.hospitals[0].name;
    this.fetchByLabReport();
  }

  private async consturctOverAllStatistics() {
    await dispatchGetOverAllStatistics(this.$store);
    this.calculateTotalSubmissions(true);
    this.constructSurveyChart(this.overAllStatistics);
  }

  async fetchAccumulative() {
    let query = `?apply_filter=1&lab_id=5&submission_no=${this.selectedSubmission}`;
    await dispatchGetByLabReportAccumulative(this.$store, query);
  }

  private async fetchByLabReport() {
    await dispatchGetByLabReport(this.$store);
    let query = '?apply_filter=0&lab_id=5&submission_no=0';
    await dispatchGetByLabReportAccumulative(this.$store, query);
    let labID = '5';
    await dispatchGetLabSubmissions(this.$store, labID);
    this.configureSubmissionListAndSelectedItem();
    this.refactorByLabReport();
    this.loadedSubmissionNumber = true;
  }

  private configureSubmissionListAndSelectedItem() {
    if (this.labSubmissionNumbers && this.labSubmissionNumbers.submission_nos && this.labSubmissionNumbers.submission_nos.length > 0) {
      this.selectedSubmission =  this.labSubmissionNumbers.submission_nos[0];
    }
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
        hospitalStatistics[0].by_question.forEach((each: any) => {
          if (each.question) {
            pdata.push([each.question, each.answer_true_perc, each.color, each.weightage]);
            ndata.push([each.question, -each.answer_false_perc, each.color, each.weightage]);
          }
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
                  fontSize: '9px',
                },
                format: '{y}%',
              },
            },
          },
          credits: {
            text: `<b>Total Survey Submissions  ${this.totalSubmissions}</b>`,
          },
          yAxis: {
            labels: {
              format: '{value}%',
              enabled: true,
            },
            stackLabels: {
              enabled: true,
              formatter() {
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
              formatter() {
                const data = pdata.find((each) => each[0] === this.value);
                return `<span style="color: ${data && data[2] ? data[2] : '#000000'}">${this.value.toString().toUpperCase()}</span>`;
              },
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
            formatter() {
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

  get userProfile() {
    const user = readUserProfile(this.$store);
    return user?.id;
  }

}
</script>
