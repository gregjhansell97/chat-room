import { combineReducers, createStore } from 'redux'


class Mailbox {
  constructor(app) {
    this.app = app;
    this.commands = {}
    // create store for mailbox
    const messages = (state={}, action) => {
      if(action.type === this.app) {
        return action.execute(state)
      } else {
        return state
      }
    };
    const reducers = combineReducers({messages});
    this.store = createStore(reducers);
  }
  on(cmd, f) {
    this.commands[cmd] = f
  }
  set(messages) {
    this.store.dispatch({
      type: this.app,
      execute: (state) => {
        return this.commands["set"](state, messages);
      }
    })
  }
  push(message) {
    this.store.dispatch({
      type: this.app,
      execute: (state) => {
        return this.commands["push"](state, message);
      }
    });
  }
}

const mailboxes = {};
const getMailbox = (app) => {
    if(!(app in mailboxes)) {
      mailboxes[app] = new Mailbox(app);
    }
    return mailboxes[app];
}
export default getMailbox;
