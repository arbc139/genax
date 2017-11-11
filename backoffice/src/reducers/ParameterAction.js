// Action types.
const SET_PARAMETERS = 'PARAMETER_SET_PARAMETERS';

// Action creators.
function setParameters(parameters) {
  return {
    type: SET_PARAMETERS,
    parameters,
  };
}

const actions = {
  SET_PARAMETERS,
};

const actionCreators = {
  setParameters,
};

export { actions, actionCreators };
