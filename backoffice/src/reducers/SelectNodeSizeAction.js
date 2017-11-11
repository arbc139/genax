// Action types.
const SET_NODE_SIZE = 'SELECT_NODE_SIZE_SET_NODE_SIZE';
const SET_METRIC_SCORE = 'SELECT_NODE_SIZE_SET_METRIC_SCORE';

// Action creators.
// period: PeriodType.
function setNodeSize(nodeSize) {
  return {
    type: SET_NODE_SIZE,
    nodeSize,
  };
}

function setMetricScore(metricScore) {
  return {
    type: SET_METRIC_SCORE,
    metricScore,
  };
}

const actions = {
  SET_NODE_SIZE, SET_METRIC_SCORE,
};

const actionCreators = {
  setNodeSize, setMetricScore,
};

export { actions, actionCreators };
