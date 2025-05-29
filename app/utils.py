#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Estate Management System - Utilities Module
Common utility functions and helpers
"""

import os
import shutil
import uuid
from datetime import datetime
from typing import List, Optional
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class FileManager:
    """File and directory management utilities"""

    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {e}")
            return False

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination"""
        try:
            # Ensure destination directory exists
            dest_dir = os.path.dirname(destination)
            FileManager.ensure_directory(dest_dir)

            shutil.copy2(source, destination)
            logger.info(f"File copied: {source} -> {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return False

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension"""
        return os.path.splitext(file_path)[1].lower()


class ImageManager:
    """Image processing and management utilities"""

    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    MAX_IMAGE_SIZE = (1920, 1080)  # Maximum size for stored images
    THUMBNAIL_SIZE = (300, 200)    # Thumbnail size

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """Check if file is a supported image format"""
        ext = FileManager.get_file_extension(file_path)
        return ext in ImageManager.SUPPORTED_FORMATS

    @staticmethod
    def resize_image(input_path: str, output_path: str,
                    max_size: tuple = MAX_IMAGE_SIZE) -> bool:
        """Resize image to maximum size while maintaining aspect ratio"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Calculate new size maintaining aspect ratio
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save optimized image
                img.save(output_path, 'JPEG', quality=85, optimize=True)
                logger.info(f"Image resized: {input_path} -> {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error resizing image: {e}")
            return False

    @staticmethod
    def create_thumbnail(input_path: str, output_path: str,
                        size: tuple = THUMBNAIL_SIZE) -> bool:
        """Create thumbnail image"""
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Save thumbnail
                img.save(output_path, 'JPEG', quality=75, optimize=True)
                logger.info(f"Thumbnail created: {output_path}")
                return True
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            return False

    @staticmethod
    def get_image_info(file_path: str) -> dict:
        """Get image information"""
        try:
            with Image.open(file_path) as img:
                return {
                    'size': img.size,
                    'mode': img.mode,
                    'format': img.format,
                    'file_size': FileManager.get_file_size(file_path)
                }
        except Exception as e:
            logger.error(f"Error getting image info: {e}")
            return {}


class PhotoManager:
    """Property photo management"""

    def __init__(self, photos_dir: str):
        """Initialize photo manager"""
        self.photos_dir = photos_dir
        self.thumbnails_dir = os.path.join(photos_dir, 'thumbnails')

        # Ensure directories exist
        FileManager.ensure_directory(self.photos_dir)
        FileManager.ensure_directory(self.thumbnails_dir)

    def save_property_photo(self, source_path: str, company_code: str) -> Optional[str]:
        """Save property photo and create thumbnail"""
        try:
            # Validate image file
            if not ImageManager.is_image_file(source_path):
                logger.error(f"Unsupported image format: {source_path}")
                return None

            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{company_code}_{timestamp}_{unique_id}.jpg"

            # Full size image path
            full_path = os.path.join(self.photos_dir, filename)

            # Thumbnail path
            thumb_filename = f"thumb_{filename}"
            thumb_path = os.path.join(self.thumbnails_dir, thumb_filename)

            # Resize and save full image
            if not ImageManager.resize_image(source_path, full_path):
                return None

            # Create thumbnail
            ImageManager.create_thumbnail(full_path, thumb_path)

            logger.info(f"Property photo saved: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error saving property photo: {e}")
            return None

    def get_photo_path(self, filename: str) -> str:
        """Get full path to photo"""
        return os.path.join(self.photos_dir, filename)

    def get_thumbnail_path(self, filename: str) -> str:
        """Get full path to thumbnail"""
        thumb_filename = f"thumb_{filename}"
        return os.path.join(self.thumbnails_dir, thumb_filename)

    def delete_property_photo(self, filename: str) -> bool:
        """Delete property photo and thumbnail"""
        try:
            # Delete full image
            full_path = self.get_photo_path(filename)
            FileManager.delete_file(full_path)

            # Delete thumbnail
            thumb_path = self.get_thumbnail_path(filename)
            FileManager.delete_file(thumb_path)

            logger.info(f"Property photo deleted: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error deleting property photo: {e}")
            return False


class DataValidator:
    """Data validation utilities"""

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number (basic validation)"""
        if not phone:
            return True  # Empty phone is allowed

        # Remove spaces and common separators
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # Check if it contains only digits and starts with appropriate prefix
        return clean_phone.isdigit() and len(clean_phone) >= 10

    @staticmethod
    def validate_year(year: str) -> bool:
        """Validate construction year"""
        if not year:
            return True  # Empty year is allowed

        try:
            year_int = int(year)
            current_year = datetime.now().year
            return 1900 <= year_int <= current_year + 5  # Allow up to 5 years in future
        except ValueError:
            return False

    @staticmethod
    def validate_area(area: str) -> bool:
        """Validate property area"""
        if not area:
            return True  # Empty area is allowed

        try:
            area_float = float(area)
            return area_float > 0
        except ValueError:
            return False

    @staticmethod
    def validate_number(number: str, min_val: int = 0, max_val: int = 100) -> bool:
        """Validate numeric input"""
        if not number:
            return True  # Empty number is allowed

        try:
            num = int(number)
            return min_val <= num <= max_val
        except ValueError:
            return False


class TextUtils:
    """Text processing utilities"""

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""

        # Strip whitespace and normalize
        return text.strip()

    @staticmethod
    def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
        """Truncate text to maximum length"""
        if not text or len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def format_currency(amount: float, currency: str = "IQD") -> str:
        """Format currency amount"""
        try:
            return f"{amount:,.0f} {currency}"
        except:
            return f"{amount} {currency}"

    @staticmethod
    def format_area(area: float, unit: str = "م²") -> str:
        """Format area measurement"""
        try:
            return f"{area:,.1f} {unit}"
        except:
            return f"{area} {unit}"


class ExportUtils:
    """Data export utilities"""

    @staticmethod
    def export_to_text(data: List[dict], filename: str,
                      title: str = "Real Estate Report") -> bool:
        """Export data to text file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n")
                f.write(f"تاريخ التصدير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                for i, item in enumerate(data, 1):
                    f.write(f"السجل رقم {i}:\n")
                    f.write("-" * 20 + "\n")

                    for key, value in item.items():
                        f.write(f"{key}: {value}\n")

                    f.write("\n")

                f.write(f"\nإجمالي السجلات: {len(data)}\n")

            logger.info(f"Data exported to: {filename}")
            return True
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            return False
