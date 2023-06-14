# Digital Election Protocol
This is a client-server application for organizing secret binary voting. A simple secret digital voting protocol is used.  
#### Designations:
- A - agency-server conducting electronic voting
- E - voter-client, legitimate voting participant
- B - digital ballot. B contains the name of the candidate and other data verifying it and necessary to enhance the security of the protocol.  

#### The voting algorithm looks like this:
* **_Step 1._** A puts out lists of possible voters.
* **_Step 2._** Users, including E, report their desire to participate in the voting.
* **_Step 3._** A puts out lists of legitimate voters.
* **_Step 4._** A creates public and private keys and shares the public key. Anyone can encrypt a message using a public key, but only A. can decrypt it.
* **_Step 5._** 
  - E creates its own public and private EDS keys, then publishes the public key. Anyone can check document E, but only the voter himself can sign it.  
  - generates a message B, where in one way or another expresses his will
  - signs the message with a private private key
  - encrypts the message with a public key
  - sends an encrypted message A
* **_Step 6._** 
  - A collects messages
  - decrypts them using a publicly available key
  - counts them and publishes the results

#### Requirements:
```
interpreter: python version 3.10
libs to be installed: PyQt5, json, socket, threading, sqlite3, Crypto, os
```

#### Workflow:
- Launch server by `python gui_server.py`
- Launch clients by `python gui_client.py subnet`, where "subnet" is subnet, where server is launched
- Add user from client. If it exists, warning appers.
- Server creates list of voters and submit question to client's machines
- Server counts votes and show results