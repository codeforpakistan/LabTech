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
          <v-select :items="labOpts" v-model="selectedLab" @change="setLabID" label="Lab Name" dense></v-select>
        </v-flex>
        <v-flex md6 style="padding-left: 10px" v-if="loadedSubmissionNumber && labSubmissionNumbers">
          <v-select :items="submissionOpts" @change="fetchAccumulative" v-model="selectedSubmission"  filled label="Submission Number" dense></v-select>
        </v-flex>
      </v-layout>
      </v-container>
      <div v-if="loadedSubmissionNumber && byLabReportAccumulative">
        <div v-for="item in byLabReportAccumulative" :key="item.name">
          <div class="mt-2" style="display: flex; justify-content: space-between; width: 340px;">
            <div><b>{{item.name}}</b></div>
            <div>{{roundOff(item.data.score)}}</div>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <vue-excel-editor ref="editor" width="400px" :readonly="true" v-model="item.data.indicators" :localized-label="myLabels"></vue-excel-editor>
            <highcharts v-if="item.data.indicators && item.data.indicators.length > 0" style="margin-top: -20px;" :options="getHighchartData(item)"></highcharts>
          </div>
        </div>
      </div>
    </template>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Highcharts from 'highcharts';
import VueExcelEditor from 'vue-excel-editor';
Vue.use(VueExcelEditor);
import { readOverAllStatistics, readHospitalsStatistics, readlabSubmissionNumbers,
  readAdminHospital, readHospitalDepartments, readByLabReport, readbyLabReportAccumulative } from '@/store/admin/getters';
import { dispatchGetOverAllStatistics, dispatchGetHospitalStatistics, dispatchGetByLabReport,
  dispatchGetByLabReportAccumulative, dispatchGetHospitals, dispatchGetHospitalDepartments,
  dispatchGetLabSubmissions } from '@/store/admin/actions';
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
  private labID: any = '';
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
      text: '',
    },
    series: [{
      showInLegend: false,
      data: [],
    }],
    xAxis: {
      categories: [],
      title: {
        text: 'Categories',
      },
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

  private roundOff(num) {
    return num.toFixed(2);
  }

  private getHighchartData(data: any) {
    const chartData: any = JSON.parse(JSON.stringify(this.barChartOptionsTemplate));
    data.data.indicators.forEach((item) => {
      chartData.series[0].data.push(parseFloat(item.Score));
      chartData.xAxis.categories.push(item.Indicator);
    });
    chartData.subtitle.text = data.name;
    return chartData;
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

  get labOpts() {
    return this.hospitals.map((x: any) => x.name);
  }

  get submissionOpts() {
    return ['All', ...this.labSubmissionNumbers.submission_nos];
  }

  private async mounted() {
    await dispatchGetHospitals(this.$store);
    this.selectedLab = this.hospitals[0].name;
    this.setLabID();
  }

  private async fetchAccumulative() {
    let query = `?apply_filter=1&lab_id=${this.labID}&submission_no=${this.selectedSubmission}`;
    if (this.selectedSubmission === 'All') {
      query = `?apply_filter=1&lab_id=${this.labID}&submission_no=0`;
    }
    await dispatchGetByLabReportAccumulative(this.$store, query);
  }

  private async setLabID() {
    const lab = this.hospitals.find((l) => l.name === this.selectedLab);
    this.labID = lab ? lab.id : '1';
    this.fetchByLabReport();
  }

  private async fetchByLabReport() {
    await dispatchGetByLabReport(this.$store);
    await dispatchGetLabSubmissions(this.$store, this.labID);
    this.configureSubmissionListAndSelectedItem();
    const query = `?apply_filter=0&lab_id=${this.labID}&submission_no=${this.selectedSubmission}`;
    await dispatchGetByLabReportAccumulative(this.$store, query);
    this.loadedSubmissionNumber = true;
  }

  private configureSubmissionListAndSelectedItem() {
    if (this.labSubmissionNumbers && this.labSubmissionNumbers.submission_nos
      && this.labSubmissionNumbers.submission_nos.length > 0) {
      this.selectedSubmission =  this.labSubmissionNumbers.submission_nos[0];
    }
  }

  get userProfile() {
    const user = readUserProfile(this.$store);
    return user?.id;
  }

}
</script>
