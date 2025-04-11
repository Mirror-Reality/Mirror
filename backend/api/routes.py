from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from solana.rpc.api import Client
from solana.publickey import PublicKey
import json
from ..ai_models.mirror_model import MirrorModel
from ..core.database import get_db
from sqlalchemy.orm import Session
import os

router = APIRouter()
mirror_model = MirrorModel()

# Initialize Solana client
solana_client = Client(os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com"))
program_id = PublicKey(os.getenv("PROGRAM_ID"))

@router.post("/mirror")
async def create_mirror(
    ipfs_hash: str,
    address: str,
    db: Session = Depends(get_db)
):
    try:
        # Verify address is valid
        try:
            public_key = PublicKey(address)
        except:
            raise HTTPException(status_code=400, detail="Invalid Solana address")
        
        # Create mirror in database
        mirror = {
            "ipfs_hash": ipfs_hash,
            "owner_address": address,
            "is_active": True
        }
        
        db_mirror = db.add(mirror)
        db.commit()
        
        return {"message": "Mirror created successfully", "mirror_id": db_mirror.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mirror/{address}")
async def get_mirror(
    address: str,
    db: Session = Depends(get_db)
):
    try:
        # Get mirror from database
        mirror = db.query(Mirror).filter(Mirror.owner_address == address).first()
        if not mirror:
            raise HTTPException(status_code=404, detail="Mirror not found")
        
        return {
            "ipfs_hash": mirror.ipfs_hash,
            "owner_address": mirror.owner_address,
            "created_at": mirror.created_at,
            "last_updated": mirror.last_updated,
            "is_active": mirror.is_active
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mirror/{address}/train")
async def train_mirror(
    address: str,
    training_data: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    try:
        # Verify mirror exists
        mirror = db.query(Mirror).filter(Mirror.owner_address == address).first()
        if not mirror:
            raise HTTPException(status_code=404, detail="Mirror not found")
        
        # Train model with user data
        mirror_model.train_personality(training_data)
        
        return {"message": "Mirror trained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mirror/{address}/generate")
async def generate_response(
    address: str,
    prompt: str,
    db: Session = Depends(get_db)
):
    try:
        # Verify mirror exists
        mirror = db.query(Mirror).filter(Mirror.owner_address == address).first()
        if not mirror:
            raise HTTPException(status_code=404, detail="Mirror not found")
        
        # Generate response using mirror model
        response = mirror_model.generate_response(address, prompt)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mirror/{address}/deactivate")
async def deactivate_mirror(
    address: str,
    db: Session = Depends(get_db)
):
    try:
        # Verify mirror exists
        mirror = db.query(Mirror).filter(Mirror.owner_address == address).first()
        if not mirror:
            raise HTTPException(status_code=404, detail="Mirror not found")
        
        # Deactivate mirror
        mirror.is_active = False
        db.commit()
        
        return {"message": "Mirror deactivated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 