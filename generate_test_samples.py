import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import random
from debug_logger import DebugLogger

class TestSampleGenerator:
    def __init__(self):
        """Initialize the test sample generator with logging"""
        self.debug_logger = DebugLogger("TestSampleGenerator")
        self.logger = self.debug_logger.get_logger()
        
        # Create samples directory
        self.samples_dir = "samples"
        os.makedirs(self.samples_dir, exist_ok=True)
        
        self.logger.info("TestSampleGenerator initialized")

    def create_synthetic_stamp(self, size=(128, 128)):
        """Create a synthetic stamp image"""
        try:
            # Create a new image with white background
            image = Image.new('RGB', size, 'white')
            draw = ImageDraw.Draw(image)
            
            # Draw outer circle (stamp border)
            margin = 10
            draw.ellipse([margin, margin, size[0]-margin, size[1]-margin],
                        outline='black', width=3)
            
            # Add some random text or patterns
            for _ in range(random.randint(3, 6)):
                x = random.randint(margin*2, size[0]-margin*2)
                y = random.randint(margin*2, size[1]-margin*2)
                draw.text((x, y), random.choice(['*', '+', '#', '@']),
                         fill='black')
            
            # Convert to numpy array
            return np.array(image)
            
        except Exception as e:
            self.debug_logger.log_error(e, "Error creating synthetic stamp")
            raise

    def create_background_image(self, size=(128, 128)):
        """Create a background image without stamps"""
        try:
            # Create random patterns
            image = np.random.randint(200, 255, (*size, 3), dtype=np.uint8)
            
            # Add some random lines
            for _ in range(random.randint(2, 5)):
                pt1 = (random.randint(0, size[0]), random.randint(0, size[1]))
                pt2 = (random.randint(0, size[0]), random.randint(0, size[1]))
                color = (random.randint(100, 200),
                        random.randint(100, 200),
                        random.randint(100, 200))
                cv2.line(image, pt1, pt2, color, 2)
            
            return image
            
        except Exception as e:
            self.debug_logger.log_error(e, "Error creating background image")
            raise

    def generate_samples(self, num_samples=20):
        """Generate test samples with and without stamps"""
        try:
            self.logger.info(f"Generating {num_samples} test samples...")
            
            for i in range(num_samples):
                # Decide if this sample should have a stamp
                has_stamp = random.choice([True, False])
                
                if has_stamp:
                    # Create image with stamp
                    base_image = self.create_background_image()
                    stamp = self.create_synthetic_stamp()
                    
                    # Place stamp at random position
                    x = random.randint(0, base_image.shape[1]-stamp.shape[1])
                    y = random.randint(0, base_image.shape[0]-stamp.shape[0])
                    
                    # Blend stamp with background
                    alpha = 0.7
                    roi = base_image[y:y+stamp.shape[0], x:x+stamp.shape[1]]
                    blended = cv2.addWeighted(roi, 1-alpha, stamp, alpha, 0)
                    base_image[y:y+stamp.shape[0], x:x+stamp.shape[1]] = blended
                    
                    filename = f"stamp_{i+1}.jpg"
                else:
                    # Create image without stamp
                    base_image = self.create_background_image()
                    filename = f"no_stamp_{i+1}.jpg"
                
                # Save image
                output_path = os.path.join(self.samples_dir, filename)
                cv2.imwrite(output_path, cv2.cvtColor(base_image, cv2.COLOR_RGB2BGR))
                
                self.logger.debug(f"Generated: {filename}")
            
            self.logger.info(f"Successfully generated {num_samples} test samples")
            
        except Exception as e:
            self.debug_logger.log_error(e, "Error generating samples")
            raise

    def verify_samples(self):
        """Verify that samples were created correctly"""
        try:
            files = os.listdir(self.samples_dir)
            stamp_files = [f for f in files if f.startswith('stamp_')]
            no_stamp_files = [f for f in files if f.startswith('no_stamp_')]
            
            self.logger.info("Sample Generation Summary:")
            self.logger.info(f"Total samples: {len(files)}")
            self.logger.info(f"Samples with stamps: {len(stamp_files)}")
            self.logger.info(f"Samples without stamps: {len(no_stamp_files)}")
            
            return len(files) > 0
            
        except Exception as e:
            self.debug_logger.log_error(e, "Error verifying samples")
            raise

if __name__ == "__main__":
    try:
        # Generate test samples
        generator = TestSampleGenerator()
        generator.generate_samples(num_samples=20)  # Generate 20 test samples
        
        # Verify samples were created
        if generator.verify_samples():
            print("✅ Test samples generated successfully!")
            print(f"📁 Check the 'samples' directory for the generated images.")
        else:
            print("❌ Error: No samples were generated.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")