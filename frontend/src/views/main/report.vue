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
        <v-flex md6 style="padding-left: 10px">
          <v-select :items="submissionNumbers(selectedLab)" v-model="selectedSubmission"  filled label="Submission Number" dense></v-select>
        </v-flex>
      </v-layout>
      </v-container>
      <div  v-if="jsondata && getSelectedReportIndex > -1">
        <div v-for="item in jsondata[getSelectedReportIndex].modules" :key="item.moduleName">
          <div class="mt-2" style="display: flex; justify-content: space-between; width: 340px;">
            <div><b>{{item.moduleName}}</b></div>
            <div>{{item.moduleScore}}</div>
          </div>
          <div style="display: flex; justify-content: space-between;">
            <vue-excel-editor ref="editor" width="400px" :readonly="true" v-model="item.indicators" :localized-label="myLabels"></vue-excel-editor>
            <highcharts style="margin-top: -20px;" :options="item.chartData"></highcharts>
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
import { readOverAllStatistics, readHospitalsStatistics,
        readAdminHospital, readHospitalDepartments, readByLabReport } from '@/store/admin/getters';
import { dispatchGetOverAllStatistics, dispatchGetHospitalStatistics, dispatchGetByLabReport,
        dispatchGetHospitals, dispatchGetHospitalDepartments} from '@/store/admin/actions';
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
    const labs: any = [];
    const submissionOptions = {};
    this.byLabReport.forEach((lab: any) => {
      const modules: any = [];
      const submissionPerModule = {};
      if (lab.name === this.selectedLab) {
        lab.submissions.forEach((sub: any) => {
          if (submissionPerModule[sub.module_name.trim()] && submissionPerModule[sub.module_name.trim()].length > 0) {
            submissionPerModule[sub.module_name.trim()].push(sub);
          } else {
            submissionPerModule[sub.module_name.trim()] = [sub];
          }
        });
        Object.keys(submissionPerModule).forEach((mod: any) => {
          let totalScore = 0;
          const chartData: any = JSON.parse(JSON.stringify(this.barChartOptionsTemplate));
          const indicators: any = [];
          submissionPerModule[mod].forEach((sub: any) => {
            totalScore += sub.score;
            indicators.push({ name: sub.indicator_name, score: parseFloat(sub.score).toFixed(2) });
            chartData.series[0].data.push(parseFloat(sub.score));
            chartData.xAxis.categories.push(sub.indicator_name);
          });
          let moduleScore: any = totalScore / submissionPerModule[mod].length;
          moduleScore = parseFloat(moduleScore).toFixed(2);
          chartData.subtitle.text = mod;
          modules.push({
            moduleName: mod,
            moduleScore,
            indicators,
            chartData,
          });
        });
        if (submissionOptions[lab.name]) {
          if (submissionOptions[lab.name].indexOf(lab.submission_no) < 0) {
            submissionOptions[lab.name].push(lab.submission_no);
          }
        } else {
          submissionOptions[lab.name] = [ lab.submission_no ];
        }
        labs.push({
          name: lab.name,
          submissionNo: lab.submission_no,
          modules,
        });
      }
    });
    this.jsondata = labs;
    // set drop down filter options. submission and submission number
    Object.keys(submissionOptions).forEach((x: any) => {
      this.submissionOptions.push({name: x, submissions: submissionOptions[x]});
    });
    if (this.submissionOptions.length > 0) {
      this.selectedSubmission = this.submissionOptions[0].submissions.length > 0
        ? this.submissionOptions[0].submissions[0]
        : 0;
    }
  }

  get labOpts() {
    return this.hospitals.map((x: any) => x.name);
  }

  private submissionNumbers(labNmae) {
    const found = this.submissionOptions.find((x) => x.name ===  labNmae);
    if (found) {
      return found.submissions;
    } else if (this.submissionOptions.length > 0) {
      return this.submissionOptions[0].submissionOptions;
    } else {
      return [];
    }
  }

  get getSelectedReportIndex() {
    if (this.selectedLab && this.selectedSubmission) {
      const x = this.jsondata.findIndex((y) => {
        return y.name === this.selectedLab && y.submissionNo === this.selectedSubmission;
      });
      return x;
    } else {
      return -1;
    }
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

  private async fetchByLabReport() {
    await dispatchGetByLabReport(this.$store);
    this.refactorByLabReport();
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
