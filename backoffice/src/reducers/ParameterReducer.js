import { actions } from './ParameterAction';

const { SET_PARAMETER } = actions;

function parameters(
  state = {
    MIN_SUP: 0.0001,
    MAX_PVAL: 0.05,
    COOC_EM: 0,
  },
  action,
) {
  switch (action.type) {
    case SET_PARAMETER:
      return action.parameter;
    default:
      return state;
  }
}

export default parameters;
