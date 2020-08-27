var Socket = require('simple-websocket');

const stub = true;
let websocket = undefined;
// TODO: check websocket support
if(stub) {
  websocket = {
    on: (cmd, action) => {
      if(cmd === "connect") {
        action();
      } else if(cmd === "data") {
      } else if(cmd === "close") {
      } else if(cmd === "error") {
      } else { console.log("ERROR: " + cmd + "not recognized"); }
    },
    send: (data) => {
      console.log("Sending data: " + data);
    }
  }
} else {
  websocket = new Socket('ws://')
}

export default websocket;
