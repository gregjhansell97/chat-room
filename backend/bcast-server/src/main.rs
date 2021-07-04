mod websocket::client;

extern crate ws;

mod multicast {
    struct Server {
        // this will be the http server that will take in a request, send that request to
        // the manager which will send to the appropriate sockets
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
    // start up websocket thread

    println!("Starting server");
    //ws::listen("127.0.0.1:9694", |out| User {out }).unwrap()
}
