import palette from 'vue-material/src/core/components/mdTheme/palette';

const rawData = [
  { x: 1, y: 1177 },
  { x: 2, y: 1190 },
  { x: 3, y: 1220 },
  { x: 4, y: 1230 },
  { x: 5, y: 1238 },
];
/* exact equation is y = 16.2 x + 1,162.4 */
const linearGraphData = [
  { x: 1, y: 1178.6 },
  { x: 5, y: 1243.4 },
];

export const data = {
  datasets: [
    {
      data: rawData,
      borderColor: palette.pink[200],
      pointBackgroundColor: palette.pink[200],
    },
    {
      showLine: true,
      fill: false,
      pointRadius: 0,
      data: linearGraphData,
      borderColor: palette.pink[200],
    },
  ],
};

export const options = {
  maintainAspectRatio: false,
  title: {
    display: true,
    position: 'top',
    text: 'Running Time by Absolute Log10(support)',
    fontSize: 20,
  },
  legend: {
    display: false,
  },
  scales: {
    xAxes: [{
      type: 'linear',
      position: 'bottom',
      scaleLabel: {
        display: true,
        labelString: '&#124;log<sub>10</sub>(support)&#124;',
      },
    }],
    yAxes: [{
      type: 'linear',
      position: 'left',
      scaleLabel: {
        display: true,
        labelString: 'Time (s)',
      },
    }],
  },
};

export default {
  data,
  options,
};
