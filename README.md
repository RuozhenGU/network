#### Simple Client Server Network

---

A basic example client server socket programming for information exchange on a message board. The connections are established through TCP handshakes and the information are transmitted through UDP. 

<i>Limitations: only one thread which means multi-clients are not supported</i>

##### Prerequisite & Running

* Download latest `python3.X` version

* pip install required library `socket` 

* First make sure server is on and prints n_port via `./server.sh <pwd>` 

  > `pwd` is user-defined password that is an integer type for client and server to authenticate
  >
  > After executing, the server will print its available `n port` for client to connect using TCP

* Second run client via `./client.sh <server address> <n_port of server> <pwd> <msg>`

  > If you run client/server on same machine, use `localhost` for `<server address>`, otherwise find the ip of your server by `$ ifconfig`  (or google [what is my ip](https://www.google.com/search?q=what is my ip))
  >
  > Copy the `n port` printed by `server.sh` and pass it to `<n_port of  server>`
  >
  > `<pwd>` of client and server are user specified and need to match for a TCP connections.
  >
  > `<msg>` can be any string you would like to server to register with. If  `TERMINATE`, then that will cause server to terminate cascading. 

##### Connection Scenarios

> TCP Part:

1. Server will find run via an available port and listen for any connections. It will also print out its own `n_port` on console and log file.
2. The client creates the TCP connection with server using the server host address and port
3. The client next will try to send a request and trying to get a random port number from server. This is only possible if the server successfully authenticate the password.
   * If authentication is succeed, a random available port will be returned
   * If failed, 0 as port number is returned, and client will terminate with error message `Invalid req_code`

> UDP Part:

1. The client once has the connection with server, will try to send "GET" and in return, the server will response with all the messages in its pool (by sending subsequent packet through UDP socket)
2. Upon receival, client will print all the message it gets from server
3. Client in the end will send another user input message to server. 
4. Server will terminate or register that message from client in its pool accordingly.
5. A user input is needed for the client to exit

##### Output and Logging

* Server: will log the n port into `server.txt`
* Client: will log the r port as well as all messages received from server; will also print those messages



