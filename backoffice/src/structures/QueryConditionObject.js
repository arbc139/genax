export const ConditionMode = {
  add: 'CONDITION_MODE_ADD',
  remove: 'CONDITION_MODE_REMOVE',
};

/* static variable */
let idCounter = 0;

export class Condition {
  constructor(type, keyword) {
    this.id = idCounter;
    this.type = type;
    this.keyword = keyword;
    idCounter += 1;
  }
}
