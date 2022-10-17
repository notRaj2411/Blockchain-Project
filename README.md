# Land Management system with PoW

## Group 39

Ashish AVS - 2019B2A7PS1435H<br/>
Abhsihek Jalan - 2019B1A71547H<br/>
Raj Srivastava - 2019B1A71426H<br/>
Utkarsh Tiwari - 2019B1A71147H<br/>


## To Run:
* Make sure the appropriate libraries are download and can be accessed by the code.
     
1.  Run 1 or upto all 3 of node_5001.py, node_5002.py & node_5003.py on separate terminals to access them as 3 separate nodes for the Blockchain system.  
2.  To connect the current node with other nodes of the system, send a post request with route as 'localhost/connect_node' and the respective node addresses in JSON format. 
3.  To register a new user send a post request with route as 'localhost/register' and user_id and property_id in JSON format.
4.  To inititate a transaction, send a post request with route as 'localhost/add_transaction' and buyer_id, seller_id and property_id in JSON format.
5.  To mine a block send  a get request with route as 'localhost/mine_block'.
6.  To get transaction history related to a property send  a post request with route as 'localhost/transaction_history' and property_id in JSON format.
7.  To get the current status of the blockchain send a get request with route as 'localhost/get_chain'.
8.  To get the registered users along with the properties send a get request with route as 'localhost/get_usersproperty'.
9.  To replace the current chain at that node with the longest chain in the blockchain, send a get request with route as 'localhost/replace_chain'.


## Libraries used:
* datetime
* hashlib
* json
* flask
* time
* requests
* uuid4 from uuid
* url parse from urllib.parse

## Function description:

### constructor
Creates and initializes the necessary variables and data structures for the blockchain:<br/>
blockchain[], transactions[], users[], nodes[], user_property{}, nodes[].<br/>
Calls the function create_block()

### create_block()
Takes the required proof, previous hash and the merkle root to create a new block with the following structure:<br/>
{index, timestamp, proof, previous_hash, transactions, merkle-root}

### get_previous_block()
Returns the last block added to the blockchain.

### proof_of_work()
Implementation of the proof of work consensus algorithm. Uses the previous proof to generate new hash values using sha256 until the computational requiremnet of having '0000' as the prefix of the hash is met.


### get_chain()
Returns the current status of the blockchain. <br/>
If the blockchain has not been created, it creates the genesis block and displays it to the user.

### connect_node()
Connects a particular node with other set of nodes

### hash()
Generates the hash value for a particular transaction or block.


### is_chain_valid()
Checks if the current state of the blockchain is valid. For each block, it check if the previous hash value is the same as the hash of the previous block. It also checks for each block by using the current and previous proof for the proof of work, i.e., '0000'.

### add_transaction()
Adds a new transaction with buyer_id, seller_id, property_id and timestamp. 

### check_user()
Checks if a user is already registered

### register_user()
Registers a new user to the system, along with all their owned properites, if the user_id doesnot already exist by calling the check_user() function.

### get_users()
Returns all the users that are currently added to the system.

### add_node()
Adds a new node to the system.

### replace_chain()
Replace chain checks if the blockchain at a particular node is the longest chain or not. If not, it is updated by the longest chain.

### find_merkle_root()
Hash values are generated for the list of transactions and stored in a sorted order. If the number of transactions are odd, the last hash is duplicated. The process is repeated to finally obtain the merkle root or the root hash value.

### Flask is used with Postman for sending and receving releavnt JSON data via function calls.
