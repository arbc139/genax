import { actions } from './StepperAction';

const { SET_PMID_COUNT } = actions;

function pmidCount(state = 0, action) {
  switch (action.type) {
    case SET_PMID_COUNT:
      return action.pmidCount;
    default:
      return state;
  }
}

export default pmidCount;
