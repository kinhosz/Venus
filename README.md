# Venus
## An encrypted communication protocol

This project was made for the Communication Protocols discipline at UFPE.  
It consists on the development of a voting protocol that's secure even in unsafe networks.  

## Dependencies
To run this project, you must use Python 3.8.5. You also need to install the rsa package, which can be found on the pip.
```sh
pip install rsa
```
The other dependencies should already be native to python, but are listed here in case of any errors:
- datetime
- json
- random
- shutil
- socket
- sys
- time

## Main Components
### CA
Our projects uses the RSA cryptography, so we need a safe place to store the public keys of our servers.
This is the purpose of the CA.  
To make one available, just run:
``` py
import Venus
ca = Venus.vCA()
ca.listen()
```
Note that the listen method has one optional param, which indicates the CA lifetime (in seconds). Leave blank to use it as Block Mode and not determine a specific lifetime.

### Server
This is the component responsible for running the voting sessions, as well as making their results available. 
To make one available, just run:
``` py
import Venus
server = Venus.vServer()
server.register()
server.listen()
```
The constructor function has one optional parameter, which corresponds to the desired address. By default, it will be hosted on the localhost:12000. Note that this parameter, when passed, must be in a tuple format: (ip,port).  
The listen signature is exactly the same as the CA's listen.  
But before running it, you should register your server on an active CA, by running the register function, which has no parameters.

### Client
This is the responsible for making all the queries to operate the server, which include:
- Creating a voting session
- Voting on a running session
- Checking the results of a session

To make an instance of the client, run:
```py
import Venus
client = Venus.vClient()
```

#### Creating Session
```py
packet = client.createSession(address, description, options, endingMode, limit)
```
- The address must be a tuple containing the IP and port where the server is located.
Ex: ("localhost",12000)
- The description is a string containing the title or question of the voting session
Ex: "2024 Presidential Elections"
- The options is a list containing only strings, which are the given choices for the session
Ex: ["Obama", "Dwayne Johnson", "Kanye West"]
- You can also determine the ending mode, which can be on votes (indicated by 1) or time (indicated by 0). By default, this option is set by votes.
Ex: 1
- The last parameter indicates the limit (in seconds or number of votes) until the voting session ends. By default, this option is set to 5.
Ex: 5

By executing this, you'll get a return from the server in the form of a python dictionary, which will have the following fields:
- code: indicates the state of the operation (complete table can be consulted at the end of this document)
- sessionID: the identification of the voting session
```py
# Sample response packet
{
    'code': '901',
    'sessionID': 117208796664160
}
```

Notice that the sessionID field might not be in the packet, this happens in case of an error, which is indicated by the code, which is always present.

#### Voting
```py
packet = client.vote(address, sessionID, option)
```
- The address must be a tuple containing the IP and port where the server is located
Ex: ("localhost",12000)
- The sessionID must be the ID of the required voting session
Ex: 117208796664160
- The option is in which option the vote goes to
Ex: "Obama"

As the return, you'll get the response from the server, which only has one field, corresponding to the code.
```py
# Sample response packet
{
    'code': '902'
}
```

#### Checking Result
```py
packet = client.checkResult(address, sessionID)
```
- The address must be a tuple containing the IP and port where the server is located
Ex: ("localhost",12000)
- The sessionID must be the ID of the required voting session
Ex: 117208796664160

As the return, you'll get the response, with all the session data, which includes:
- code: indicates the state of the operation
- sessionId: identification of the voting session
- description: title of the session
- result: dictionary containing each option as keys and the number of votes as it's values
- totalVotes: the total amount of votes
- endingMode: either 0 (by time) or 1 (by votes)
- limit: either the number of seconds or votes required to finish the session
- start: timestamp of the moment the session began

```py
# Sample response packet
{
    'code': '903',
    'sessionID': 117208796664160,
    'description': '2024 Presidential Elections',
    'result': {
                'Obama': 2,
                'Dwayne Johnson': 1,
                'Kanye West': 0
    },
    'totalVotes': 3,
    'endingMode': 1,
    'limit': 3,
    'start': '2021-04-14 23:43:23.343332'
}
```

Please note that in case of any errors, the only field returned will be the code, describing the error itself.

### Code Reference
| Code | Meaning |
| ------ | ------ |
| 408 | Server Timeout |
| 701 | Error: Invalid sessionID |
| 702 | Error: Closed Session |
| 703 | Error: Session still open |
| 704 | Error: Invalid vote option |
| 901 | Session created successfully |
| 902 | Vote sucessfully registered |
| 903 | Successfully checked results |
| 999 | Invalid packet format |
