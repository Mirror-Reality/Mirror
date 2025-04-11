// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MirrorIdentity {
    struct DigitalMirror {
        string ipfsHash;
        address owner;
        uint256 createdAt;
        uint256 lastUpdated;
        bool isActive;
    }

    mapping(address => DigitalMirror) public mirrors;
    mapping(address => bool) public authorizedUsers;

    event MirrorCreated(address indexed owner, string ipfsHash);
    event MirrorUpdated(address indexed owner, string ipfsHash);
    event MirrorDeactivated(address indexed owner);

    modifier onlyOwner(address mirrorOwner) {
        require(msg.sender == mirrorOwner, "Only owner can perform this action");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedUsers[msg.sender], "Not authorized");
        _;
    }

    function createMirror(string memory ipfsHash) public {
        require(mirrors[msg.sender].owner == address(0), "Mirror already exists");
        
        mirrors[msg.sender] = DigitalMirror({
            ipfsHash: ipfsHash,
            owner: msg.sender,
            createdAt: block.timestamp,
            lastUpdated: block.timestamp,
            isActive: true
        });

        emit MirrorCreated(msg.sender, ipfsHash);
    }

    function updateMirror(string memory ipfsHash) public onlyOwner(msg.sender) {
        require(mirrors[msg.sender].isActive, "Mirror is not active");
        
        mirrors[msg.sender].ipfsHash = ipfsHash;
        mirrors[msg.sender].lastUpdated = block.timestamp;

        emit MirrorUpdated(msg.sender, ipfsHash);
    }

    function deactivateMirror() public onlyOwner(msg.sender) {
        require(mirrors[msg.sender].isActive, "Mirror is already inactive");
        
        mirrors[msg.sender].isActive = false;
        mirrors[msg.sender].lastUpdated = block.timestamp;

        emit MirrorDeactivated(msg.sender);
    }

    function getMirror(address owner) public view returns (
        string memory ipfsHash,
        uint256 createdAt,
        uint256 lastUpdated,
        bool isActive
    ) {
        DigitalMirror memory mirror = mirrors[owner];
        return (
            mirror.ipfsHash,
            mirror.createdAt,
            mirror.lastUpdated,
            mirror.isActive
        );
    }
} 