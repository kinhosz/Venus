# Venus
## An encrypted communication protocol

This project was made for the Communication Protocols discipline at UFPE.  
It consists on the development of a protocol that's secure even in unsafe networks.  

## Main Components
### CA
Our projects uses the RSA cryptography, so we need a safe place to store the public keys of our servers.
This is the purpose of the CA.  
To make one available, just run (after imports):
``` sh
ca = vCA()
ca.listen()
```

### Server
This is the component responsible for running the voting sessions, as well as making their results available.  
To run this, just run (after imports):
``` sh
server = vServer()
server.listen()
```

### Client
This is the responsible for making all the queries to operate the server, they include:
- Creating a voting session
- Voting on a running session
- Check the results of a session

To make an instance and it's operations, run (after imports):
```sh
client = vClient()
client.createSession(address, description, options)
client.vote(address, sessionID, option)
client.checkResult(address, sessionID)
```

### Creating Session Params
- The address must be a tuple containing the IP and port where the server is located
- The description is the question or title of the voting session
- The options is a list containing only strings
-  You can also determine a ending param ("votes" or "time") and send an extra param with the amount of votes or seconds required for the session to end
By default, the session is ended after 5 votes

### Voting Params
- The address must be a tuple containing the IP and port where the server is located
- The sessionID must be the ID of the voting session required
- The option is in which option the vote goes to

### Check Result
- The address must be a tuple containing the IP and port where the server is located
- The sessionID must be the ID of the voting session required

## Dependencies
To run this project, you also need to install these python packages:
- rsa
- 