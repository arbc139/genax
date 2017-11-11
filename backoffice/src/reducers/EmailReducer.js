import { actions } from './EmailAction';

const { SET_EMAIL } = actions;

function email(state = '', action) {
  switch (action.type) {
    case SET_EMAIL:
      return action.email;
    default:
      return state;
  }
}

export default email;
