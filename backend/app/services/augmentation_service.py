"""
Image Augmentation Service for CCTV Face Recognition

Applies various augmentations to simulate real-world CCTV conditions:
- Brightness/Contrast variations (day/night)
- Gaussian blur (motion blur, low-res cameras)
- Small rotations (head tilts)
- Horizontal flip (pose changes)
- Random cropping/scaling (different distances)
- Noise addition (sensor noise)

This helps embeddings generalize better without retraining the model.
"""
import cv2
import numpy as np
from typing import List, Tuple
import random
import logging

logger = logging.getLogger(__name__)


class AugmentationService:
    """Service for augmenting face images to improve CCTV robustness"""
    
    def __init__(self):
        """Initialize augmentation service"""
        self.enabled = True
        logger.info("Augmentation service initialized")
    
    def adjust_brightness_contrast(
        self, 
        image: np.ndarray, 
        brightness_range: Tuple[float, float] = (0.7, 1.3),
        contrast_range: Tuple[float, float] = (0.8, 1.2)
    ) -> np.ndarray:
        """
        Adjust brightness and contrast to simulate lighting variations
        
        Args:
            image: Input image
            brightness_range: (min, max) brightness multiplier
            contrast_range: (min, max) contrast multiplier
            
        Returns:
            Augmented image
        """
        brightness = random.uniform(*brightness_range)
        contrast = random.uniform(*contrast_range)
        
        # Apply brightness and contrast
        # Formula: new_image = contrast * image + brightness
        img_float = image.astype(np.float32)
        img_float = img_float * contrast + (brightness - 1.0) * 128
        img_float = np.clip(img_float, 0, 255)
        
        return img_float.astype(np.uint8)
    
    def add_gaussian_blur(
        self, 
        image: np.ndarray, 
        kernel_size_range: Tuple[int, int] = (3, 7)
    ) -> np.ndarray:
        """
        Add Gaussian blur to simulate motion blur or low-res cameras
        
        Args:
            image: Input image
            kernel_size_range: (min, max) kernel size (must be odd)
            
        Returns:
            Blurred image
        """
        kernel_size = random.choice([3, 5, 7])  # Must be odd
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def rotate_image(
        self, 
        image: np.ndarray, 
        angle_range: Tuple[float, float] = (-15, 15)
    ) -> np.ndarray:
        """
        Rotate image to simulate head tilts
        
        Args:
            image: Input image
            angle_range: (min, max) rotation angle in degrees
            
        Returns:
            Rotated image
        """
        angle = random.uniform(*angle_range)
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        # Get rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Perform rotation
        rotated = cv2.warpAffine(image, M, (width, height), 
                                 borderMode=cv2.BORDER_REFLECT)
        
        return rotated
    
    def horizontal_flip(self, image: np.ndarray) -> np.ndarray:
        """
        Flip image horizontally
        
        Args:
            image: Input image
            
        Returns:
            Flipped image
        """
        return cv2.flip(image, 1)
    
    def random_crop_scale(
        self, 
        image: np.ndarray, 
        scale_range: Tuple[float, float] = (0.85, 1.0)
    ) -> np.ndarray:
        """
        Randomly crop and scale image to simulate different distances
        
        Args:
            image: Input image
            scale_range: (min, max) scale factor
            
        Returns:
            Cropped and scaled image
        """
        height, width = image.shape[:2]
        scale = random.uniform(*scale_range)
        
        # Calculate crop dimensions
        new_height = int(height * scale)
        new_width = int(width * scale)
        
        # Random crop position
        y = random.randint(0, height - new_height) if height > new_height else 0
        x = random.randint(0, width - new_width) if width > new_width else 0
        
        # Crop
        cropped = image[y:y+new_height, x:x+new_width]
        
        # Resize back to original size
        resized = cv2.resize(cropped, (width, height))
        
        return resized
    
    def add_gaussian_noise(
        self, 
        image: np.ndarray, 
        sigma_range: Tuple[float, float] = (5, 15)
    ) -> np.ndarray:
        """
        Add Gaussian noise to simulate sensor noise
        
        Args:
            image: Input image
            sigma_range: (min, max) standard deviation of noise
            
        Returns:
            Noisy image
        """
        sigma = random.uniform(*sigma_range)
        noise = np.random.normal(0, sigma, image.shape)
        
        noisy_image = image.astype(np.float32) + noise
        noisy_image = np.clip(noisy_image, 0, 255)
        
        return noisy_image.astype(np.uint8)
    
    def simulate_occlusion(
        self, 
        image: np.ndarray, 
        occlusion_type: str = 'random'
    ) -> np.ndarray:
        """
        Simulate occlusions (glasses, masks, etc.)
        
        Args:
            image: Input image
            occlusion_type: 'glasses', 'mask', 'scarf', or 'random'
            
        Returns:
            Image with simulated occlusion
        """
        height, width = image.shape[:2]
        occluded = image.copy()
        
        if occlusion_type == 'random':
            occlusion_type = random.choice(['glasses', 'mask', 'none'])
        
        if occlusion_type == 'glasses':
            # Simulate glasses in upper half
            y1 = int(height * 0.3)
            y2 = int(height * 0.5)
            x1 = int(width * 0.15)
            x2 = int(width * 0.85)
            # Add a semi-transparent dark rectangle
            overlay = occluded[y1:y2, x1:x2].copy()
            overlay = (overlay * 0.7).astype(np.uint8)
            occluded[y1:y2, x1:x2] = overlay
        
        elif occlusion_type == 'mask':
            # Simulate mask in lower half
            y1 = int(height * 0.5)
            y2 = int(height * 0.85)
            x1 = int(width * 0.2)
            x2 = int(width * 0.8)
            # Add a semi-opaque rectangle
            overlay = occluded[y1:y2, x1:x2].copy()
            overlay = (overlay * 0.5 + 128 * 0.5).astype(np.uint8)
            occluded[y1:y2, x1:x2] = overlay
        
        return occluded
    
    def augment_single_image(
        self, 
        image: np.ndarray, 
        augmentation_probability: float = 0.5
    ) -> np.ndarray:
        """
        Apply random augmentations to a single image
        
        Args:
            image: Input image
            augmentation_probability: Probability of applying each augmentation
            
        Returns:
            Augmented image
        """
        augmented = image.copy()
        
        # Apply augmentations with probability
        if random.random() < augmentation_probability:
            augmented = self.adjust_brightness_contrast(augmented)
        
        if random.random() < augmentation_probability * 0.5:
            augmented = self.add_gaussian_blur(augmented)
        
        if random.random() < augmentation_probability * 0.7:
            augmented = self.rotate_image(augmented)
        
        if random.random() < 0.3:  # Less frequent
            augmented = self.horizontal_flip(augmented)
        
        if random.random() < augmentation_probability * 0.6:
            augmented = self.random_crop_scale(augmented)
        
        if random.random() < augmentation_probability * 0.3:
            augmented = self.add_gaussian_noise(augmented)
        
        # Occlusion is optional and rare
        if random.random() < 0.1:
            augmented = self.simulate_occlusion(augmented)
        
        return augmented
    
    def augment_images_for_registration(
        self, 
        images: List[np.ndarray], 
        augmentations_per_image: int = 2,
        include_originals: bool = True
    ) -> List[np.ndarray]:
        """
        Augment a list of images for employee registration
        
        Args:
            images: List of original images
            augmentations_per_image: Number of augmented versions per original
            include_originals: Whether to include original images
            
        Returns:
            List of original + augmented images
        """
        if not self.enabled:
            logger.info("Augmentation disabled, returning original images")
            return images
        
        augmented_images = []
        
        # Include original images if requested
        if include_originals:
            augmented_images.extend(images)
            logger.info(f"Added {len(images)} original images")
        
        # Generate augmented versions
        for idx, image in enumerate(images):
            for aug_idx in range(augmentations_per_image):
                augmented = self.augment_single_image(image)
                augmented_images.append(augmented)
            
            if (idx + 1) % 10 == 0:
                logger.info(f"Augmented {idx + 1}/{len(images)} images")
        
        logger.info(f"Total images after augmentation: {len(augmented_images)} "
                   f"(original: {len(images)}, augmented: {len(augmented_images) - len(images)})")
        
        return augmented_images
    
    def create_cctv_variations(
        self, 
        image: np.ndarray
    ) -> List[Tuple[np.ndarray, str]]:
        """
        Create specific CCTV condition variations
        
        Args:
            image: Original image
            
        Returns:
            List of (augmented_image, description) tuples
        """
        variations = []
        
        # Original
        variations.append((image.copy(), "Original"))
        
        # Low light
        dark = self.adjust_brightness_contrast(
            image, 
            brightness_range=(0.5, 0.7), 
            contrast_range=(0.7, 0.9)
        )
        variations.append((dark, "Low light"))
        
        # Bright light
        bright = self.adjust_brightness_contrast(
            image, 
            brightness_range=(1.2, 1.5), 
            contrast_range=(1.1, 1.3)
        )
        variations.append((bright, "Bright light"))
        
        # Motion blur
        blurred = self.add_gaussian_blur(image, kernel_size_range=(5, 7))
        variations.append((blurred, "Motion blur"))
        
        # Angled
        rotated_left = self.rotate_image(image, angle_range=(-10, -5))
        variations.append((rotated_left, "Tilted left"))
        
        rotated_right = self.rotate_image(image, angle_range=(5, 10))
        variations.append((rotated_right, "Tilted right"))
        
        # Flipped
        flipped = self.horizontal_flip(image)
        variations.append((flipped, "Mirrored"))
        
        # Far away (zoomed out)
        zoomed_out = self.random_crop_scale(image, scale_range=(0.7, 0.8))
        variations.append((zoomed_out, "Far distance"))
        
        # Noisy (bad sensor)
        noisy = self.add_gaussian_noise(image, sigma_range=(10, 20))
        variations.append((noisy, "Noisy sensor"))
        
        logger.info(f"Created {len(variations)} CCTV variations")
        
        return variations


# Singleton instance
augmentation_service = AugmentationService()
