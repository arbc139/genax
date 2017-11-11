// Action types.
const SET_QUERY = 'QUERY_BUILDER_SET_QUERY';
const CLEAR_QUERY = 'QUERY_BUILDER_CLEAR_QUERY';
const ADD_CONDITION = 'QUERY_BUILDER_ADD_CONDITION';
const REMOVE_CONDITION = 'QUERY_BUILDER_REMOVE_CONDITION';
const DROP_TYPE_OF_FIRST_CONDITION =
  'QUERY_BUILDER_DROP_TYPE_OF_FIRST_CONDITION';

// Action creators.
function setQuery(query) {
  return {
    type: SET_QUERY,
    query,
  };
}
function clearQuery() {
  return {
    type: CLEAR_QUERY,
  };
}
function addCondition(condition) {
  return {
    type: ADD_CONDITION,
    condition,
  };
}
function removeCondition(index) {
  return {
    type: REMOVE_CONDITION,
    index,
  };
}
function dropTypeOfFirstCondition() {
  return {
    type: DROP_TYPE_OF_FIRST_CONDITION,
  };
}

const actions = {
  SET_QUERY,
  CLEAR_QUERY,
  ADD_CONDITION,
  REMOVE_CONDITION,
  DROP_TYPE_OF_FIRST_CONDITION,
};

const actionCreators = {
  setQuery,
  clearQuery,
  addCondition,
  removeCondition,
  dropTypeOfFirstCondition,
};

export { actions, actionCreators };
