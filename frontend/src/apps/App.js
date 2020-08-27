import { Provider } from 'react-redux';
import React from 'react';

// Local CSS Styling
import 'common/css/azul-negro.css';
import 'apps/App.css';

// App Mailboxes
import getMailbox from 'common/js/mailbox.js'

// Apps
import Messenger from "apps/messenger/Messenger";

//create stores


function App(props) {
  return (
    <div className="App">
      <Provider store={getMailbox("messenger").store}>
        <Messenger />
      </Provider>
    </div>
  );
}

export default App;
