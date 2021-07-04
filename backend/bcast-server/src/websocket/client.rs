struct Client {
    sender: ws::Sender,
    token: Option<String>,
    manager: mpsc::Sender<ManagerRequest>,
}


// idea de couple ws::Sender from Client more since that's giving you trouble
// create a websocket that creates a client... that when called it sends message to the manager

impl Client {
    pub fn new(manager: mpsc::Sender<ManagerRequest>, sender: ws::Sender) -> Client {
        Client {
            sender,
            token: None,
            manager,
        }
    }

    // change to a message format that's not ws::Message - an expected structure...
    // validate that the sender gets new messages
    // do something with on_close - same deal
    // define a set of messages a client could receive
    // also need a receiver that sits in another thread, though it's function
    // can be called without another thread... (for testing)
}

impl ws::Handler for Client {
    fn on_open(&mut self, _:ws::Handshake) -> ws::Result<()> {
        // need to iterate over
        Ok(())
    }

    fn on_message(&mut self, msg: ws::Message) -> ws::Result<()> {
        // TODO: actually parse message for token
        let next_token = String::from("this-is-fake-until-actually-receives-request");
        // convert message to something expected
        // then call handle message
        // set token to new value - unregister old value and register new value
        self.token = match &self.token {
            None => {
                self.manager.send(ManagerRequest::Register(next_token.clone(), self.sender.clone())).unwrap();
                Some(next_token)
            }
            Some(token) => {
                //(self.unregister)(token);
                self.manager.send(ManagerRequest::Register(next_token.clone(), self.sender.clone())).unwrap();
                self.manager.send(ManagerRequest::Unregister(token.clone())).unwrap();
                Some(next_token)
            }
        };
        return Ok(());
    }

    fn on_close(&mut self, _: ws::CloseCode, _: &str) {
        // removes token from registry
        self.token = match &self.token {
            None => { None }
            Some(token) => {
                self.manager.send(ManagerRequest::Unregister(token.clone())).unwrap();
                None
            }
        }
    }

    fn on_error(&mut self, _: ws::Error) {
        // TODO: not sure exactly what to do here - unrecoverable?
        // removes token from registry
        println!("Error occurred");
        self.token = match &self.token {
            None => { None }
            Some(token) => {
                self.manager.send(ManagerRequest::Unregister(token.clone())).unwrap();
                None
            }
        }
    }
}
