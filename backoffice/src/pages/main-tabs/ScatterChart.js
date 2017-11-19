import { Scatter } from 'vue-chartjs/dist/vue-chartjs';

export default {
  extends: Scatter,
  name: 'scatter-chart',
  props: ['data', 'options'],
  mounted() {
    this.renderChart(this.data, this.options);
  },
};
