"""
Face Recognition Service using MTCNN and ArcFace (InsightFace)
"""
import cv2
import numpy as np
import base64
from typing import List, Tuple, Optional
from mtcnn import MTCNN
from insightface.app import FaceAnalysis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    """
    Service for face detection and recognition using MTCNN and ArcFace
    """
    
    def __init__(self):
        """Initialize face detection and recognition models"""
        try:
            # Initialize MTCNN for face detection
            logger.info("Initializing MTCNN face detector...")
            self.detector = MTCNN(min_face_size=settings.MIN_FACE_SIZE)
            
            # Initialize InsightFace with ArcFace model
            logger.info("Initializing InsightFace ArcFace model...")
            self.face_analyzer = FaceAnalysis(
                name='buffalo_l',
                providers=['CPUExecutionProvider']
            )
            self.face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
            
            logger.info("Face recognition models initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing face recognition models: {str(e)}")
            raise
    
    def base64_to_image(self, base64_string: str) -> np.ndarray:
        """
        Convert base64 string to OpenCV image
        
        Args:
            base64_string: Base64 encoded image string
            
        Returns:
            OpenCV image (numpy array)
        """
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64 to bytes
            img_bytes = base64.b64decode(base64_string)
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)
            
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                raise ValueError("Failed to decode image")
            
            return img
        except Exception as e:
            logger.error(f"Error converting base64 to image: {str(e)}")
            raise ValueError(f"Invalid image format: {str(e)}")
    
    def detect_faces_mtcnn(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces using MTCNN
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            List of face detections with bounding boxes and keypoints
        """
        try:
            # Convert BGR to RGB for MTCNN
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            faces = self.detector.detect_faces(rgb_image)
            
            return faces
        except Exception as e:
            logger.error(f"Error detecting faces with MTCNN: {str(e)}")
            return []
    
    def extract_face_embedding(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract face embedding using ArcFace (InsightFace)
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            512D embedding vector or None if no face detected
        """
        try:
            # InsightFace expects BGR format
            faces = self.face_analyzer.get(image)
            
            if len(faces) == 0:
                logger.warning("No face detected in image")
                return None
            
            # Get the first (largest) face
            face = faces[0]
            
            # Extract embedding (512D vector)
            embedding = face.embedding
            
            # Normalize embedding
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding
        except Exception as e:
            logger.error(f"Error extracting face embedding: {str(e)}")
            return None
    
    def process_registration_images(self, base64_images: List[str]) -> Tuple[Optional[np.ndarray], int]:
        """
        Process multiple images for employee registration
        
        Args:
            base64_images: List of base64 encoded images
            
        Returns:
            Tuple of (averaged embedding vector, number of successful images)
        """
        embeddings = []
        successful_count = 0
        
        for idx, base64_img in enumerate(base64_images):
            try:
                # Convert base64 to image
                image = self.base64_to_image(base64_img)
                
                # Extract embedding
                embedding = self.extract_face_embedding(image)
                
                if embedding is not None:
                    embeddings.append(embedding)
                    successful_count += 1
                    logger.info(f"Successfully processed image {idx + 1}/{len(base64_images)}")
                else:
                    logger.warning(f"No face detected in image {idx + 1}/{len(base64_images)}")
            except Exception as e:
                logger.error(f"Error processing image {idx + 1}: {str(e)}")
                continue
        
        if len(embeddings) == 0:
            logger.error("No valid face embeddings extracted from images")
            return None, 0
        
        # Average embeddings
        avg_embedding = np.mean(embeddings, axis=0)
        
        # Normalize averaged embedding
        avg_embedding = avg_embedding / np.linalg.norm(avg_embedding)
        
        logger.info(f"Successfully processed {successful_count}/{len(base64_images)} images")
        
        return avg_embedding, successful_count
    
    def compare_embeddings(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compare two embeddings using cosine similarity
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (higher is more similar)
        """
        # Cosine similarity
        similarity = np.dot(embedding1, embedding2)
        return float(similarity)
    
    def calculate_distance(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate distance between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Distance (lower is more similar)
        """
        # Euclidean distance
        distance = np.linalg.norm(embedding1 - embedding2)
        return float(distance)
    
    def recognize_face(self, base64_image: str, stored_embeddings: List[Tuple[str, np.ndarray]]) -> Tuple[Optional[str], Optional[float]]:
        """
        Recognize face from image
        
        Args:
            base64_image: Base64 encoded image
            stored_embeddings: List of tuples (employee_id, embedding)
            
        Returns:
            Tuple of (employee_id, confidence) or (None, None) if not recognized
        """
        try:
            # Convert base64 to image
            image = self.base64_to_image(base64_image)
            
            # Extract embedding
            query_embedding = self.extract_face_embedding(image)
            
            if query_embedding is None:
                logger.warning("No face detected in query image")
                return None, None
            
            # Find best match
            best_match_id = None
            best_distance = float('inf')
            
            for employee_id, stored_embedding in stored_embeddings:
                # Calculate distance
                distance = self.calculate_distance(query_embedding, stored_embedding)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match_id = employee_id
            
            # Check if best match is below threshold
            if best_distance < settings.FACE_RECOGNITION_THRESHOLD:
                confidence = 1.0 - best_distance  # Convert distance to confidence
                logger.info(f"Face recognized: {best_match_id} (distance: {best_distance:.4f})")
                return best_match_id, confidence
            else:
                logger.info(f"Face not recognized (best distance: {best_distance:.4f})")
                return None, None
        except Exception as e:
            logger.error(f"Error recognizing face: {str(e)}")
            return None, None


# Singleton instance
face_recognition_service = FaceRecognitionService()
