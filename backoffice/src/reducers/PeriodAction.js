// Action types.
const SET_PERIOD = 'PERIOD_SET_PERIOD';

// Action creators.
function setPeriod(period) {
  return {
    type: SET_PERIOD,
    period,
  };
}

const actions = {
  SET_PERIOD,
};

const actionCreators = {
  setPeriod,
};

export { actions, actionCreators };
