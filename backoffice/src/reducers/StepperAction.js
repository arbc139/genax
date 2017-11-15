// Action types.
const SET_PMID_COUNT = 'MAIN_STEPPER_SET_PMID_COUNT';

// Action creators.
function setPmidCount(pmidCount) {
  return {
    type: SET_PMID_COUNT,
    pmidCount,
  };
}

const actions = {
  SET_PMID_COUNT,
};

const actionCreators = {
  setPmidCount,
};

export { actions, actionCreators };
