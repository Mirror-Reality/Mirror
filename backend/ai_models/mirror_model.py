import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from typing import List, Dict, Any
import numpy as np

class MirrorModel(nn.Module):
    def __init__(self, model_name: str = "gpt2"):
        super(MirrorModel, self).__init__()
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.personality_vectors = {}
        
    def train_personality(self, user_data: List[Dict[str, Any]]) -> None:
        """
        Train the model on user-specific data to capture personality traits
        """
        # Process user data and create personality embeddings
        for data in user_data:
            text = data.get("text", "")
            personality_traits = data.get("personality_traits", {})
            
            # Create personality vector
            personality_vector = self._create_personality_vector(personality_traits)
            self.personality_vectors[data["user_id"]] = personality_vector
            
            # Fine-tune model on user's text
            self._fine_tune_model(text)
    
    def generate_response(self, 
                         user_id: str, 
                         prompt: str, 
                         max_length: int = 100) -> str:
        """
        Generate a response that matches the user's personality
        """
        # Get user's personality vector
        personality_vector = self.personality_vectors.get(user_id)
        if personality_vector is None:
            raise ValueError(f"No personality data found for user {user_id}")
        
        # Encode prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        
        # Generate response
        output = self.model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        
        # Decode and return response
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response
    
    def _create_personality_vector(self, traits: Dict[str, float]) -> torch.Tensor:
        """
        Create a personality vector from traits
        """
        # Convert traits to tensor
        vector = torch.tensor(list(traits.values()), dtype=torch.float32)
        return vector
    
    def _fine_tune_model(self, text: str) -> None:
        """
        Fine-tune the model on user's text
        """
        # Tokenize text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        
        # Fine-tune model
        outputs = self.model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        loss.backward()
        
    def save_model(self, path: str) -> None:
        """
        Save the model and personality vectors
        """
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'personality_vectors': self.personality_vectors
        }, path)
    
    def load_model(self, path: str) -> None:
        """
        Load the model and personality vectors
        """
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.personality_vectors = checkpoint['personality_vectors'] 