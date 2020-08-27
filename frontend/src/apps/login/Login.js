import React, { useEffect, useRef } from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
// global css
import 'common/css/azul-negro.css';
// local imports
import './Login.css';


function Login(props) {
  const username = React.createRef();
  const password = React.createRef()
  return (
    <div className="Login">
      <div className="UsernameInputBox">
        <Form.Control
          id="UsernameInput"
          placeholder="Username"
          ref={username}
            if(v.key === "Enter") {
              //TODO: submit message when enter is pressed
              // this is where we're gonna set state
              msg.current.value = "";
            }
          }}/>
      </div>
      <div className="PasswordInputBox">
        <Form.Control
          type="password"
          id="PasswordInput"
          placeholder="Password"
          ref={msg}
          onKeyPress={(v) => {
            if(v.key === "Enter") {
              //TODO: submit message when enter is pressed
              const un = username.current.value;
              const
              // this is where we're gonna set state
              msg.current.value = "";
            }
          }}/>
      </div>
      <Button className="LoginButton" onClick={()=> console.log("clicked")}>
      Login
      </Button>
    </div>
  );

}

export default Login;
