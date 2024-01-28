// Server logic
// create listener
// wait for incoming connections
// when request is received, accept, and the client should wait for a response (command)
// for loop for entering commands in server
// if command is exit, terminate connection
// otherwise, send command to client, client should execute command on machine, and send output to server
// convert output in stream to utf-8 and display

  ///////////////////////////////////////////////////////////////
 //                          BUGFIXES                         //
///////////////////////////////////////////////////////////////
// When entering nothing as a command, it breaks the program //
// so that no further commands can be sent and the input st- //
// -ring does not print.                                     //
//                                                           //
// When sending an incorrect command, or a command with arg- //
// -uments, the client panics and crashes.                   //
//                                                           //
// 


#![allow(unused)]
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream, SocketAddr};
use std::thread;

fn banner() {
    println!("banner here");
}

fn listener_handler(host_ip_addr: &str, host_port_num: &str) {
    let address_str = format!("{}:{}", host_ip_addr, host_port_num);

    // Parse the string into a SocketAddr
    let address: SocketAddr = address_str.parse().expect("Failed to parse address");

    // Bind to address and port
    let listener = TcpListener::bind(&address).expect("Failed to bind to address.");
    println!("Server listening on {}...", address);

    // Listen for connections
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                std::thread::spawn(|| comm_handler(stream));
            }
            Err(e) => {
                // stderr - standard error stream
                eprintln!("Failed to establish connection: {}", e);
            }
        }
    }
}

fn comm_in(mut stream: &TcpStream) -> usize {
    // Read the response from the client
    let mut buffer = [0; 1024];
    let bytes_read = stream.read(&mut buffer).expect("Failed to read from client.");
    //if bytes_read == 0 {
    //    println!("Client closed the connection.");
    //    break;
    //}
    // Convert data from buffer to UTF-8
    let response = String::from_utf8_lossy(&buffer[..bytes_read]);
    println!("{}", response);
    bytes_read
}

fn comm_out(mut stream: &TcpStream) {
     // Send a command to the client
     let mut command = String::new();
     print!(">: ");

    // Assign data from server to variable and print it
     std::io::stdout().flush().expect("Failed to flush stdout");
     std::io::stdin().read_line(&mut command).expect("Failed to read line");
     let command = command.trim();
     
     stream.write_all(command.as_bytes()).expect("Failed to send command to client.");
     stream.flush().expect("Failed to flush stream");
}

fn comm_handler(mut stream: TcpStream) {
    loop {
        comm_out(&stream);
        comm_in(&stream);
    }
}

// Entry point
fn main() {
    banner();
    let host_ip = "127.0.0.1";
    let host_port = "8080";
    listener_handler(&host_ip, &host_port);
}
