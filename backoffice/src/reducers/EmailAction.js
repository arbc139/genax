// Action types.
const SET_EMAIL = 'EMAIL_SET_EMAIL';

// Action creators.
function setEmail(email) {
  return {
    type: SET_EMAIL,
    email,
  };
}

const actions = {
  SET_EMAIL,
};

const actionCreators = {
  setEmail,
};

export { actions, actionCreators };
