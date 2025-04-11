module.exports = {
  networks: {
    localhost: {
      url: "http://localhost:8899",
      accounts: ["your_local_keypair_path"]
    },
    devnet: {
      url: "https://api.devnet.solana.com",
      accounts: ["your_devnet_keypair_path"]
    },
    mainnet: {
      url: "https://api.mainnet-beta.solana.com",
      accounts: ["your_mainnet_keypair_path"]
    }
  },
  solc: {
    version: "0.8.0",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
}; 