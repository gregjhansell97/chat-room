use std::sync::mpsc;
use std::collections::HashMap;

enum ManagerRequest {
    Register(String, ws::Sender),
    Unregister(String),
    Multicast(Vec<String>, String),
}

struct Manager {
    messages: mpsc::Receiver<ManagerRequest>,
    sender: mpsc::Sender<ManagerRequest>,
}

impl Manager {
    pub fn new() -> Manager {
        let (tx, rx) = mpsc::channel();
        Manager {
            messages: rx,
            sender: tx,
        }
    }
    pub fn sender(&self) -> &mpsc::Sender<ManagerRequest> { &self.sender }
    fn handle_requests(requests: impl Iterator<Item=ManagerRequest>) {
        let mut clients = HashMap::new();
        for m in requests {
            match m {
                ManagerRequest::Register(token, sender) => {
                    clients.insert(token, sender);
                }
                ManagerRequest::Unregister(token) => {
                    clients.remove(&token);
                }
                ManagerRequest::Multicast(tokens, msg) => {
                    for t in tokens {
                        match clients.get(&t) {
                            None => { }
                            Some(sender) => {
                                sender.send(msg.as_str()).unwrap();
                            }
                        }
                    }

                }
            }

        }
    }
    pub fn listen(&self) { Manager::handle_requests(self.messages.iter()); }
}

#[cfg(test)]
mod tests {
    use crate::_websocket::{Manager, ManagerRequest};
    use std::sync::mpsc;

    #[test]
    fn test_new_manager_construction() {
        let manager = Manager::new();
    }

    #[test]
    fn test_registration() {
        let (tx, rx) = mpsc::channel();
        requests = [ManagerRequest::Register(String::from("greg"), tx)];
        Manager::handle_requests(requests.iter());
    }
}


struct Client {
    sender: ws::Sender,
    token: Option<String>,
    manager: mpsc::Sender<ManagerRequest>,
}

impl Client {
    pub fn new(manager: mpsc::Sender<ManagerRequest>, sender: ws::Sender) -> Client {
        Client {
            sender,
            token: None,
            manager,
        }
    }
}

impl ws::Handler for Client {
    fn on_open(&mut self, _:ws::Handshake) -> ws::Result<()> { Ok(()) }

    fn on_message(&mut self, msg: ws::Message) -> ws::Result<()> {
        println!("{:?}", msg.as_text());
        // TODO: actually parse message for token
        let next_token = String::from("this-is-fake-until-actually-receives-request");
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

// #[cfg(test)]
// mod tests {
//     use std::thread;
//     use std::time;
//     use std::sync::mpsc;
//     use crate::websocket::Manager;
//     use crate::websocket::Client;
//     use crate::websocket::ManagerRequest;
//
//     fn spawn_servers(addr: String) {
//         let manager = Manager::new();
//         let m_sender = manager.sender().clone();
//         thread::spawn(move || { manager.listen() });
//         println!("{}", &addr);
//         thread::spawn(move || {
//             ws::listen(
//                 addr,
//                 move |out| Client::new(m_sender.clone(), out)).unwrap();
//         });
//     }
//
//     #[test]
//     fn spawning_servers() {
//         spawn_servers(String::from("ws://127.0.0.1:9694"));
//     }
//
//     #[test]
//     fn one_client_token_registry() {
//         let url = String::from("ws://127.0.0.1:3012");
//         spawn_servers(url.clone());
//         ws::connect(url, |out| {
//             println!("HERE!");
//             out.send("hello world").unwrap();
//             println!("NOT HERE");
//             move |msg| {
//                 println!("Got message: {}", msg);
//                 out.close(ws::CloseCode::Normal)
//             }
//         }).unwrap();
//         thread::sleep(time::Duration::from_secs(5));
//     }
// }
