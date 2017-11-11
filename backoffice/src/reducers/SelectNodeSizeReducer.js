import { actions } from './SelectNodeSizeAction';

const { SET_NODE_SIZE, SET_METRIC_SCORE } = actions;

export function nodeSize(state = 1, action) {
  switch (action.type) {
    case SET_NODE_SIZE:
      return action.nodeSize;
    default:
      return state;
  }
}

export function metricScore(state = 0.001, action) {
  switch (action.type) {
    case SET_METRIC_SCORE:
      return action.metricScore;
    default:
      return state;
  }
}
