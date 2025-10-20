"""Face Recognition Service using SCRFD and ArcFace (InsightFace)
"""
import cv2
import numpy as np
import base64
from typing import List, Tuple, Optional
from insightface.app import FaceAnalysis
from app.core.config import settings
from app.services.augmentation_service import augmentation_service
import logging

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    """
    Service for face detection and recognition using SCRFD and ArcFace (InsightFace)
    SCRFD: Faster and more robust face detection for real-world/CCTV scenarios
    ArcFace: High-accuracy 512D face embeddings
    """
    
    def __init__(self):
        """Initialize face detection and recognition models"""
        try:
            # Initialize InsightFace with SCRFD detector and ArcFace model
            logger.info("Initializing InsightFace (SCRFD + ArcFace)...")
            self.face_analyzer = FaceAnalysis(
                name='buffalo_l',  # buffalo_l includes SCRFD detector + ArcFace recognition
                providers=['CPUExecutionProvider']
            )
            # det_size: detection size for SCRFD (larger = more accurate but slower)
            # ctx_id: 0 for CPU, GPU id for CUDA
            self.face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
            
            logger.info("Face recognition models initialized successfully")
            logger.info("Using SCRFD for detection (faster, more robust than MTCNN)")
            logger.info("Using ArcFace for embedding extraction (512D vectors)")
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
    
    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """
        Detect faces using SCRFD (via InsightFace)
        
        Args:
            image: OpenCV image (BGR format)
            
        Returns:
            List of face detections with bounding boxes, landmarks, and scores
        """
        try:
            # InsightFace expects BGR format (same as OpenCV)
            faces = self.face_analyzer.get(image)
            
            # Convert InsightFace face objects to dict format
            face_detections = []
            for face in faces:
                detection = {
                    'box': face.bbox.astype(int).tolist(),  # [x1, y1, x2, y2]
                    'confidence': float(face.det_score),
                    'keypoints': face.kps.astype(int).tolist() if hasattr(face, 'kps') else None,
                    'embedding': face.embedding
                }
                face_detections.append(detection)
            
            logger.info(f"Detected {len(face_detections)} face(s) using SCRFD")
            return face_detections
        except Exception as e:
            logger.error(f"Error detecting faces with SCRFD: {str(e)}")
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
    
    def process_registration_images(self, base64_images: List[str], use_augmentation: bool = None) -> Tuple[Optional[List[np.ndarray]], int]:
        """
        Process multiple images for employee registration
        Stores ALL embeddings (not averaged) for better variation handling
        Optionally applies data augmentation for CCTV robustness
        
        Args:
            base64_images: List of base64 encoded images
            use_augmentation: Override default augmentation setting (None = use config)
            
        Returns:
            Tuple of (list of embedding vectors, number of successful images)
        """
        # Determine if augmentation should be used
        if use_augmentation is None:
            use_augmentation = settings.USE_AUGMENTATION
        
        # Convert base64 images to numpy arrays
        images = []
        for idx, base64_img in enumerate(base64_images):
            try:
                image = self.base64_to_image(base64_img)
                images.append(image)
            except Exception as e:
                logger.error(f"Error converting image {idx + 1}: {str(e)}")
                continue
        
        if len(images) == 0:
            logger.error("No valid images to process")
            return None, 0
        
        logger.info(f"Converted {len(images)} images from base64")
        
        # Apply augmentation if enabled
        if use_augmentation:
            logger.info(f"Applying augmentation (x{settings.AUGMENTATIONS_PER_IMAGE} per image)...")
            images = augmentation_service.augment_images_for_registration(
                images,
                augmentations_per_image=settings.AUGMENTATIONS_PER_IMAGE,
                include_originals=settings.INCLUDE_ORIGINAL_IMAGES
            )
            logger.info(f"After augmentation: {len(images)} images total")
        
        # Extract embeddings from all images (original + augmented)
        embeddings = []
        successful_count = 0
        
        for idx, image in enumerate(images):
            try:
                # Extract embedding
                embedding = self.extract_face_embedding(image)
                
                if embedding is not None:
                    embeddings.append(embedding)
                    successful_count += 1
                    if (idx + 1) % 10 == 0 or (idx + 1) == len(images):
                        logger.info(f"Extracted embeddings: {idx + 1}/{len(images)}")
                else:
                    logger.warning(f"No face detected in image {idx + 1}/{len(images)}")
            except Exception as e:
                logger.error(f"Error processing image {idx + 1}: {str(e)}")
                continue
        
        if len(embeddings) == 0:
            logger.error("No valid face embeddings extracted from images")
            return None, 0
        
        logger.info(f"Successfully extracted {successful_count}/{len(images)} embeddings")
        logger.info(f"Storing {len(embeddings)} individual embeddings for better accuracy")
        
        if use_augmentation:
            logger.info(f"✅ Augmentation enabled: embeddings cover lighting, blur, angles, and other CCTV variations")
        
        return embeddings, successful_count
    
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
        Calculate distance between two embeddings (DEPRECATED - use compare_embeddings)
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Distance (lower is more similar)
        """
        # Euclidean distance (deprecated - cosine similarity is better for normalized embeddings)
        distance = np.linalg.norm(embedding1 - embedding2)
        return float(distance)
    
    def recognize_face(self, base64_image: str, stored_embeddings: List[Tuple[str, List[np.ndarray]]]) -> Tuple[Optional[str], Optional[float]]:
        """
        Recognize face from image using cosine similarity
        Compares against ALL stored embeddings for each employee (not averaged)
        
        Args:
            base64_image: Base64 encoded image
            stored_embeddings: List of tuples (employee_id, list_of_embeddings)
            
        Returns:
            Tuple of (employee_id, confidence) or (None, None) if not recognized
            
        Note:
            Uses cosine similarity (range -1 to 1, where 1 = identical)
            More stable than Euclidean distance for normalized embeddings
            Compares against all embeddings and takes the BEST match
        """
        try:
            # Convert base64 to image
            image = self.base64_to_image(base64_image)
            
            # Extract embedding
            query_embedding = self.extract_face_embedding(image)
            
            if query_embedding is None:
                logger.warning("No face detected in query image")
                return None, None
            
            # Find best match using cosine similarity
            best_match_id = None
            best_similarity = -1.0  # Start with lowest possible similarity
            
            for employee_id, employee_embeddings in stored_embeddings:
                # Compare against ALL embeddings for this employee
                # Take the BEST (highest) similarity score
                max_similarity_for_employee = -1.0
                
                for stored_embedding in employee_embeddings:
                    similarity = self.compare_embeddings(query_embedding, stored_embedding)
                    if similarity > max_similarity_for_employee:
                        max_similarity_for_employee = similarity
                
                # Check if this employee has the best overall match
                if max_similarity_for_employee > best_similarity:
                    best_similarity = max_similarity_for_employee
                    best_match_id = employee_id
            
            # Check if best match is above threshold
            if best_similarity > settings.FACE_RECOGNITION_THRESHOLD:
                confidence = best_similarity  # Similarity is already in 0-1 range
                logger.info(f"Face recognized: {best_match_id} (similarity: {best_similarity:.4f}, confidence: {confidence:.2%})")
                return best_match_id, confidence
            else:
                logger.info(f"Face not recognized (best similarity: {best_similarity:.4f}, threshold: {settings.FACE_RECOGNITION_THRESHOLD})")
                return None, None
        except Exception as e:
            logger.error(f"Error recognizing face: {str(e)}")
            return None, None


# Singleton instance
face_recognition_service = FaceRecognitionService()
