import React, { useEffect, useRef, useState } from 'react';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';
import { connect } from 'react-redux';
// global css
import 'common/css/azul-negro.css';
// mailbox
import getMailbox from "common/js/mailbox.js"
// local imports
//import { appendMessage } from './store.js'
import './Messenger.css';


/*
message type:
{
  app: messenger
  content:
    from: user who sent content // will always have
    // specific to messenger
    name: str // unique
    nick-name: str // not unique
    message: "string name"

}
*/

const mailbox = getMailbox("messenger")
mailbox.on("set", (state, messages) => {
  const groups = {}
  for(let m of messages) {
    if(!(m.group in groups)) {
      groups[m.group] = []
    }
    groups[m.group].push(m)
  }
  return groups
});

mailbox.on("push", (state, message) => {
  const groups = {}
  for(let g of Object.keys(state)) {
    groups[g] = state[g];
  }
  if(!(message.group in groups)) {
    groups[message.group] = [];
  }
  groups[message.group].push(message);
  return groups;
})

function NavOptions(props) {
  const {usernames} = props;
  const [show, setShow] = useState(false);
  return (
    <div className={"NavOptions"}>
      <Button className={"AddChatButton"} onClick={()=>setShow(true)}>
        <i className="AddChatButtonIcon fa fa-plus primary-color"></i>
      </Button>

      <Modal className={"AddChatModal"} closeButton show={show} onHide={()=>setShow(false)}>
        <Modal.Body className={"primary-color"}>
          <Form.Control
            validated={false}
            id="AddChatGroupInput"
            placeholder="Group"/>
          <Form.Control
            id="AddChatUserInput"
            placeholder="Username"/>
        </Modal.Body>
      </Modal>
    </div>
  );
}

function NavTabs(props) {
  const {groups} = props;
  const group_tabs = groups.map((g) => (
    <h1 className={"NavTab"} key={g}> {g} </h1>
  ));
  return (
    <div className={"NavTabs primary-scrollbar"}>
      {group_tabs}
    </div>
  );
}

function ChatOptions(props) {
  let {group} = props;
  if(group === undefined) group = ""
  return (
    <div className={"ChatOptions"} >
      <h1 className={"ChatOptionsTitle"}> {group} </h1>
    </div>
  )
}

function ChatMessages(props) {
  const bottomRef = useRef(null);
  const {messages} = props;
  const message_components = messages.map((m, i) => (
    <blockquote key={i} className="MyChatMessage blockquote mb-0">
      <p className="ChatMessageContent"> {m.message} </p>
      <footer className="ChatMessageFooter primary-color blockquote-footer">
        {m.from}
      </footer>
    </blockquote>
  ));
    //<h1 className={"ChatMessage"} key={m}> {i} </h1>
  useEffect(() => bottomRef.current.scrollIntoView(), [message_components])
  return (
    <div className={"ChatMessages"}>
      <div className={"ChatMessageList primary-scrollbar"}>
        {message_components}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

function ChatMessageInput(props) {
  const msg = React.createRef();
  return (
    <div className="ChatMessageInputBox">
      <Form.Control
        id="ChatMessageInput"
        className="ChatMessageInput"
        placeholder="Send it bro!"
        ref={msg}
        onKeyPress={(v) => {
          if(v.key === "Enter") {
            getMailbox("messenger").push({from: "Greg", message: msg.current.value, group: "HOMIES"});
            // this is where we're gonna set state
            msg.current.value = "";
          }
        }}/>
    </div>
  )
}

class Messenger extends React.Component {

  render() {
    let {messages, groups} = this.props;
    const group = groups[0];
    messages = group in messages ? messages[group] : [];
    //const groups = ["Homies", "Family", "Random", "Chat2", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    return (
      <Container fluid className="Messenger" >
        <Row sm={12}>
          <Col className="Messenger-Col" sm={3}>
            <NavOptions />
            <NavTabs groups={groups}/>
          </Col>
          <Col className="Messenger-Col" sm={9}>
            <ChatOptions group={group} />
            <ChatMessages messages={messages}/>
            <ChatMessageInput />
          </Col>
        </Row>
      </Container>
    );
  }
}

function mapMessengerStateToProps(state, props) {
  /*
  groups:
  [{
    name: HOMIES
    unique-name: HOMIES-(time of creation)-user
    users: []
    messages: []
  }]
  */
  return {
    groups: Object.keys(state.messages),
    messages: state.messages
  }
}
Messenger = connect(mapMessengerStateToProps)(Messenger);

export default Messenger;
