<template>
  <v-container fluid>
    <highcharts
      class="stock"
      :constructor-type="'stockChart'"
      :options="performanceTimeline"
    ></highcharts>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Highcharts from "highcharts";

export default class Reporting extends Vue {
  results: number[] = [1, 2, 3, 4, 5];
  get performanceTimeline() {
    let ctx = this,
      chartConfig: Highcharts.Options = {
        rangeSelector: {
          selected: 1
        },
        title: {
          text: "Performance Over Time"
        },
        yAxis: {
          labels: {
            formatter: function(
              // this: Highcharts.AxisLabelsFormatterContextObject
            ): string {
              let labels = ["a", "b", "c", "d", "e"];
              let current: number = this.value;
              return labels[current];
            }
          }
        },
        tooltip: {
          formatter: function(
            this: Highcharts.TooltipFormatterContextObject
          ): string {
            return "<b>Status:</b> " + this.y;
          }
        },
        series: [
          {
            type: "bar",
            name: "Status",
            data: this.results.map(test => {
              return [1580315144 + 86000 * test * 1000, test];
            }),
            pointInterval: 1000 * 3600 * 24
          }
        ]
      };
    return chartConfig;
  }
}

</script>