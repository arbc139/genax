import moment from 'moment';

import { actions } from './PeriodAction';

const { SET_PERIOD } = actions;

function removeTime(momentObject) {
  return moment().set({
    year: momentObject.get('year'),
    month: momentObject.get('month'),
    date: momentObject.get('date'),
  });
}

const start = moment().set({ year: 1900, month: 0, date: 1 });
const now = removeTime(moment());
function period(state = { start, end: now }, action) {
  switch (action.type) {
    case SET_PERIOD:
      return action.period;
    default:
      return state;
  }
}

export default period;
