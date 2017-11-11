import _ from 'lodash';
import { actions } from './QueryBuilderAction';

import { Condition } from '../structures/QueryConditionObject';

const {
  SET_QUERY,
  CLEAR_QUERY,
  ADD_CONDITION,
  REMOVE_CONDITION,
  DROP_TYPE_OF_FIRST_CONDITION,
} = actions;

function query(state = '', action) {
  switch (action.type) {
    case SET_QUERY:
      return action.query;
    case CLEAR_QUERY:
      return '';
    default:
      return state;
  }
}

function conditions(state = [new Condition('', '')], action) {
  switch (action.type) {
    case CLEAR_QUERY:
      return [new Condition('', '')];
    case ADD_CONDITION:
      return [...state, action.condition];
    case REMOVE_CONDITION:
      return _.filter(state, (condition, index) => index !== action.index);
    case DROP_TYPE_OF_FIRST_CONDITION:
      return [_.defaults({ type: '' }, state[0]), ..._.drop(state)];
    default:
      return state;
  }
}

export { query, conditions };
