# Blockchain-Project

# SmartContracts

## Group 39

Ashish AVS - 2019B2A7PS1435H<br/>
Abhsihek Jalan - 2019B1A71547H<br/>
Raj Srivastava - 2019B1A71426H<br/>
Utkarsh Tiwari - 2019B1A71147H<br/>


## Tools used:
* RemixIDE

## Transaction States:
* AWAITING_PAYMENT(0) : This is the initial state when the contract is created.
* AWAITING_DELIVERY(1) : This state is reached when the customer deposits the money
* TRANSACTION_COMPLETE(2) : This state is reached when the customer confirms the delivery and contract has been fulfilled.

## Function description:

### modifier onlyCustomer()
Displays a relevant message when only the customer can call a function but it has been called by the buyer (xyz.com).

### modifier onlyxyz()
Displays a relevant message when only the buyer(xyz.com) can call a function but it has been called by the customer.

### constructor
Initializes the customer and seller address

### deposit()
This function is called by the customer and it deposits the money to the smart contract after which the contract goes to the state 1.

### confirmDelivery()
This function is also called by the customer to confirm the delivery of the product after which the money is tranferred to the sellers account and the contract goes to state 2.
