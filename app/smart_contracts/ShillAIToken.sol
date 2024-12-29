// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/// @title ShillAI Smart Contract for Trading and Governance
contract ShillAIToken {
    string public constant name = "ShillAI Token";
    string public constant symbol = "SHILL";
    uint8 public constant decimals = 18;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event RevenueShared(address indexed staker, uint256 reward);

    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    constructor(uint256 initialSupply) {
        owner = msg.sender;
        totalSupply = initialSupply * (10 ** uint256(decimals));
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address to, uint256 value) public returns (bool) {
        require(balanceOf[msg.sender] >= value, "Insufficient balance");
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function approve(address spender, uint256 value) public returns (bool) {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(balanceOf[from] >= value, "Insufficient balance");
        require(allowance[from][msg.sender] >= value, "Allowance exceeded");

        balanceOf[from] -= value;
        balanceOf[to] += value;
        allowance[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }

    // Staking logic
    mapping(address => uint256) public stakedBalance;
    uint256 public totalStaked;

    function stake(uint256 amount) public {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance to stake");
        balanceOf[msg.sender] -= amount;
        stakedBalance[msg.sender] += amount;
        totalStaked += amount;
    }

    function unstake(uint256 amount) public {
        require(stakedBalance[msg.sender] >= amount, "Insufficient staked balance");
        stakedBalance[msg.sender] -= amount;
        balanceOf[msg.sender] += amount;
        totalStaked -= amount;
    }

    // Revenue sharing logic
    function distributeRewards(uint256 rewardAmount) public onlyOwner {
        require(totalStaked > 0, "No staked tokens to distribute rewards");

        for (uint i = 0; i < totalStaked; i++) {
            address staker = msg.sender; // Replace with actual staker addresses
            uint256 reward = (stakedBalance[staker] * rewardAmount) / totalStaked;
            balanceOf[staker] += reward;
            emit RevenueShared(staker, reward);
        }
    }
}
