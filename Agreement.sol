pragma solidity ^0.8.11;

contract Escrow {
    enum State { AWAITING_PAYMENT, AWAITING_DELIVERY, TRANSACTION_COMPLETE }
    
    State public currState;
    
    address public customer;
    address payable public xyz;
    
    modifier onlyCustomer() {
        require(msg.sender == customer, "Only customer can call this method");
        _;
    }
    
    modifier onlyxyz() {
        require(msg.sender == xyz, "Only xyz can call this method");
        _;
    }
    
    constructor(address _customer, address payable _xyz) public {
        customer = _customer;
        xyz = _xyz;
    }
    
    function deposit() onlyCustomer external payable {
        require(currState == State.AWAITING_PAYMENT, "Already paid");
        currState = State.AWAITING_DELIVERY;
    }
    
    function confirmDelivery() onlyCustomer external {
        require(currState == State.AWAITING_DELIVERY, "Cannot confirm delivery");
        xyz.transfer(address(this).balance);
        currState = State.TRANSACTION_COMPLETE;
    }
}