import Vue from 'vue';
import Revue from 'revue';
import { combineReducers, createStore, applyMiddleware } from 'redux';

import _ from 'lodash';

import { actionCreators as emailActions } from './EmailAction';
import { actionCreators as stepperActions } from './StepperAction';
import { actionCreators as parameterActions } from './ParameterAction';
import { actionCreators as periodActions } from './PeriodAction';
import { actionCreators as queryBuilderActions } from './QueryBuilderAction';
import {
  actionCreators as selectNodeSizeActions,
} from './SelectNodeSizeAction';

import email from './EmailReducer';
import parameters from './ParameterReducer';
import period from './PeriodReducer';
import pmidCount from './StepperReducer';
import { metricScore, nodeSize } from './SelectNodeSizeReducer';
import { query, conditions } from './QueryBuilderReducer';

const reducers = combineReducers({
  query,
  conditions,
  period,
  parameters,
  metricScore,
  nodeSize,
  email,
  pmidCount,
});
const actions = _.defaults(
  {},
  queryBuilderActions,
  periodActions,
  parameterActions,
  selectNodeSizeActions,
  emailActions,
  stepperActions,
);

const reduxStore = createStore(reducers, applyMiddleware());
const store = new Revue(Vue, reduxStore, actions);

export default store;
