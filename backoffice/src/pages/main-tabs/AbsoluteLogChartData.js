const rawData = [
  { x: 1, y: 1177 },
  { x: 2, y: 1190 },
  { x: 3, y: 1220 },
  { x: 4, y: 1230 },
  { x: 5, y: 1238 },
];

const linearGraphData = [
  { x: 1, y: 1178 },
  { x: 5, y: 1243 },
];

export const data = {
  datasets: [
    {
      label: 'measurement data',
      data: rawData,
    },
    {
      label: 'linear',
      showLine: true,
      fill: false,
      data: linearGraphData,
    },
  ],
};

export const option = {
  scales: {
    xAxes: [{
      type: 'linear',
      position: 'bottom',
    }],
  },
};

export default {
  data,
  option,
};
