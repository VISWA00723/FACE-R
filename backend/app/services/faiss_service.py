"""
FAISS Service for fast vector similarity search
"""
import numpy as np
import faiss
import pickle
from typing import List, Tuple, Optional
from pathlib import Path
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class FAISSService:
    """
    Service for fast vector similarity search using FAISS
    """
    
    def __init__(self):
        self.index = None
        self.employee_ids = []
        self.dimension = settings.EMBEDDING_SIZE
        self.index_path = settings.FAISS_INDEX_PATH
        self.metadata_path = settings.FAISS_INDEX_PATH.replace('.bin', '_metadata.pkl')
        
        if settings.USE_FAISS:
            self.load_or_create_index()
    
    def load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        try:
            if Path(self.index_path).exists() and Path(self.metadata_path).exists():
                logger.info("Loading existing FAISS index...")
                self.index = faiss.read_index(self.index_path)
                
                with open(self.metadata_path, 'rb') as f:
                    self.employee_ids = pickle.load(f)
                
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                logger.info("Creating new FAISS index...")
                self.create_index()
        except Exception as e:
            logger.error(f"Error loading FAISS index: {str(e)}")
            self.create_index()
    
    def create_index(self):
        """Create a new FAISS index"""
        # Use L2 distance (Euclidean)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.employee_ids = []
        logger.info("Created new FAISS index")
    
    def add_embedding(self, employee_id: str, embedding: np.ndarray):
        """
        Add an embedding to the FAISS index
        
        Args:
            employee_id: Employee ID
            embedding: 512D embedding vector
        """
        if not settings.USE_FAISS:
            return
        
        try:
            # Ensure embedding is 2D array
            if len(embedding.shape) == 1:
                embedding = embedding.reshape(1, -1)
            
            # Convert to float32 (FAISS requirement)
            embedding = embedding.astype('float32')
            
            # Add to index
            self.index.add(embedding)
            self.employee_ids.append(employee_id)
            
            logger.info(f"Added embedding for employee {employee_id} to FAISS index")
            
            # Save index
            self.save_index()
        except Exception as e:
            logger.error(f"Error adding embedding to FAISS: {str(e)}")
            raise
    
    def update_embedding(self, employee_id: str, new_embedding: np.ndarray):
        """
        Update an existing embedding in the FAISS index
        
        Args:
            employee_id: Employee ID
            new_embedding: New 512D embedding vector
        """
        if not settings.USE_FAISS:
            return
        
        try:
            # Find the index of the employee
            if employee_id in self.employee_ids:
                idx = self.employee_ids.index(employee_id)
                
                # FAISS doesn't support direct update, so we need to rebuild
                # For production, consider using IVF indices for better update support
                logger.warning("FAISS IndexFlatL2 doesn't support updates. Rebuilding index...")
                
                # Remove old entry
                self.employee_ids.pop(idx)
                
                # Rebuild index
                self.rebuild_index_from_db()
            else:
                # If not found, just add it
                self.add_embedding(employee_id, new_embedding)
        except Exception as e:
            logger.error(f"Error updating embedding in FAISS: {str(e)}")
            raise
    
    def search(self, query_embedding: np.ndarray, k: int = 1) -> List[Tuple[str, float]]:
        """
        Search for similar embeddings
        
        Args:
            query_embedding: Query embedding vector
            k: Number of nearest neighbors to return
            
        Returns:
            List of tuples (employee_id, distance)
        """
        if not settings.USE_FAISS or self.index.ntotal == 0:
            return []
        
        try:
            # Ensure embedding is 2D array
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Convert to float32
            query_embedding = query_embedding.astype('float32')
            
            # Search
            distances, indices = self.index.search(query_embedding, k)
            
            # Format results
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx != -1 and idx < len(self.employee_ids):
                    results.append((self.employee_ids[idx], float(dist)))
            
            return results
        except Exception as e:
            logger.error(f"Error searching FAISS index: {str(e)}")
            return []
    
    def save_index(self):
        """Save FAISS index to disk"""
        try:
            # Create directory if it doesn't exist
            Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Save index
            faiss.write_index(self.index, self.index_path)
            
            # Save metadata
            with open(self.metadata_path, 'wb') as f:
                pickle.dump(self.employee_ids, f)
            
            logger.info("FAISS index saved successfully")
        except Exception as e:
            logger.error(f"Error saving FAISS index: {str(e)}")
    
    def rebuild_index_from_db(self):
        """Rebuild FAISS index from database (to be implemented with DB access)"""
        logger.warning("Rebuild from DB not implemented yet")
        pass
    
    def delete_embedding(self, employee_id: str):
        """
        Delete an embedding from the FAISS index
        
        Args:
            employee_id: Employee ID
        """
        if not settings.USE_FAISS:
            return
        
        try:
            if employee_id in self.employee_ids:
                # FAISS IndexFlatL2 doesn't support deletion
                # Need to rebuild the index
                logger.warning("FAISS IndexFlatL2 doesn't support deletion. Rebuilding index...")
                self.employee_ids.remove(employee_id)
                self.rebuild_index_from_db()
        except Exception as e:
            logger.error(f"Error deleting embedding from FAISS: {str(e)}")


# Singleton instance
faiss_service = FAISSService() if settings.USE_FAISS else None
