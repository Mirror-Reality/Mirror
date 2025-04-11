import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Connection, PublicKey, Transaction } from '@solana/web3.js';
import { create } from 'ipfs-http-client';
import axios from 'axios';
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import { useWallet } from '@solana/wallet-adapter-react';

const DashboardContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const MirrorCard = styled.div`
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const Button = styled.button`
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
  
  &:hover {
    background: #45a049;
  }
`;

const MirrorDashboard = () => {
  const [mirrorData, setMirrorData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const { publicKey, sendTransaction } = useWallet();
  const connection = new Connection(process.env.REACT_APP_SOLANA_RPC_URL || 'https://api.devnet.solana.com');

  useEffect(() => {
    if (publicKey) {
      loadMirrorData();
    }
  }, [publicKey]);

  const loadMirrorData = async () => {
    try {
      setIsLoading(true);
      if (!publicKey) {
        throw new Error('Wallet not connected');
      }
      
      // Load mirror data from Solana program
      const response = await axios.get(`/api/mirror/${publicKey.toString()}`);
      setMirrorData(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const createNewMirror = async () => {
    try {
      setIsLoading(true);
      if (!publicKey) {
        throw new Error('Wallet not connected');
      }
      
      // Create IPFS client
      const ipfs = create({ url: process.env.REACT_APP_IPFS_API_URL });
      
      // Upload initial mirror data to IPFS
      const mirrorData = {
        personality: {},
        preferences: {},
        createdAt: new Date().toISOString()
      };
      
      const { path } = await ipfs.add(JSON.stringify(mirrorData));
      
      // Create mirror on Solana
      const programId = new PublicKey(process.env.REACT_APP_PROGRAM_ID);
      const instruction = {
        programId,
        keys: [
          { pubkey: publicKey, isSigner: true, isWritable: true },
          { pubkey: new PublicKey(process.env.REACT_APP_MIRROR_ACCOUNT), isSigner: false, isWritable: true }
        ],
        data: Buffer.from([0, ...Buffer.from(path)])
      };

      const transaction = new Transaction().add(instruction);
      const signature = await sendTransaction(transaction, connection);
      await connection.confirmTransaction(signature);
      
      await loadMirrorData();
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <DashboardContainer>
      <h1>My Digital Mirror</h1>
      
      {!mirrorData ? (
        <Button onClick={createNewMirror}>Create New Mirror</Button>
      ) : (
        <MirrorCard>
          <h2>Mirror Status</h2>
          <p>Created: {new Date(mirrorData.createdAt).toLocaleDateString()}</p>
          <p>Last Updated: {new Date(mirrorData.lastUpdated).toLocaleDateString()}</p>
          <p>Status: {mirrorData.isActive ? 'Active' : 'Inactive'}</p>
          
          <div>
            <Button onClick={() => {/* Update mirror */}}>Update Mirror</Button>
            <Button onClick={() => {/* Deactivate mirror */}}>Deactivate</Button>
          </div>
        </MirrorCard>
      )}
    </DashboardContainer>
  );
};

export default MirrorDashboard; 