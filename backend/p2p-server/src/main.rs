extern crate ws;

pub mod chat_room_msg {
    use serde::{Deserialize, Serialize};

    #[derive(Deserialize, Serialize)]
    pub enum Kind {
        CreateRoom,
        SendMessage,
    }

    #[derive(Deserialize, Serialize)]
    pub struct Message {
        pub kind: Kind,
        pub room: String,
        data: String
    }
}


struct User {
    out: ws::Sender,
}

// each user has a list of chats they are in, if ref count on that chat goes
// to zero then remove that chat object
//

impl ws::Handler for User {

    fn on_open(&mut self, _:ws::Handshake) -> ws::Result<()> {
        println!("Socket connection created!");
        return Ok(());
    }

    fn on_message(&mut self, msg: ws::Message) -> ws::Result<()> {
        // user is going to send a message and it will come here 
        // here are the options
        // Message will be about creating a room, or sending a message
        // to a room
        let msg: chat_room_msg::Message  = serde_json::from_str(&msg.into_text().unwrap()).unwrap();
        match msg.kind {
            chat_room_msg::Kind::CreateRoom => {
                println!("Creating room: {}", msg.room)
            }
            chat_room_msg::Kind::SendMessage => {
            }
        }
        return Ok(());
    }

    fn on_close(&mut self, _: ws::CloseCode, _: &str) {
        println!("Socket is closing");
    }

    fn on_error(&mut self, _: ws::Error) {
        println!("Error occured");
    }
}


fn main() {
    /*
     * Will have one loop creating websockets and based on the 
     * information received in the websockets handles them accordingly
     *
     * Another loop deals with authentication, at first requests
     * token from here
     */
    println!("Starting server");
    ws::listen("127.0.0.1:9694", |out| User {out: out}).unwrap()
}
