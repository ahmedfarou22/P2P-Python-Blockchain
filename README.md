# P2P-Python-Blockchain
Application chooses
A blockchain is a decentralized database that is shared among a computer network. A blockchain acts as a database, storing information in a digital format. The blockchain's significance is that it ensures the integrity and security of a data record while also generating trust without the requirement for a trusted third party.
Blockchain vs Database
Features	Blockchain	Database 
The data structure	Blocks that form a chain	Tables and columns
Network type	Distributed peer to peer	Centralized server to client
Accessibility	Anyone can access it	Requires permission
Speed 	Blockchains are slow	Databases are fast
History	It has a record history and digital record ownership.	It has no history of records or ownership
Confidentiality 	Is fully confidential	Is not fully confidential
Operations	Only insert operations	Has create, read, update, and delete
Recursive	Is not recursive. We cannot go back to repeat a task on any record.	Is recursive. We can go back to repeat a task on a particular record.

Different application options 
In this course, I had the privilege of choosing how to apply my work. A blockchain is applicable in various scenarios, but the priority for me was to build something innovative that would fix a real-world problem that many people face. I once met a friend that was a victim of corruption in the Egyptian scholastic system, Thanaweya Amma. His papers were tampered with, and his grades were lower than they should be. This happens a lot to benefit other students and give them grades they don’t deserve. A lot of students suffer as a result of this type of corruption each year. So, I decided to build a blockchain application to put an end to it.

My application
For the reasons mentioned above I created a distributed blockchain application that can be used as a database to save Thanaweya students exams on, so that the exams can never be tampered with or changed. The application should work in the backend of the software that is used for testing students. Every block on the block chain contains the students name, the students sitting number, the subject, and the answers of the student. The figures below show how a block and the block chain are constructed.


How to use the application
Prerequisites 
Before starting the program, you need to install the cryptography and Tkinter libraries. Use the below commands to install both libraries.
•	Pip Install cryptography
•	pip install tk 
besides the libraries you must have at least 2 virtual machines working at the same time to create and validate blocks. 
Step 1: Start 2 virtual machines and run the python file.

Step 2: 
Now both the nodes are not connected. to connect them type join in any of the nodes and type the IP address of the other node.
•	Join
•	<IP address of the other node> 192.168.247.134
Step 3: 
Now that you connected the 2 machines together you can start testing some of the functionalities.
•	Type create to create a new block
•	Type see to see the current version of the block chain
•	Type peers to view all the peers on the network

Note: if you want to connect a third node, just type join on that node and pass the IP address of one of the connected nodes. This will make the third node automatically connect to the first 2 (type peers to verify. If done correctly you will find the 3 IP address representing all the peers on the network)

