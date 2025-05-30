import sys
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.metrics import dp

# Add the app directory to Python path
sys.path.insert(0, './app')

from app.database import DatabaseManager
from app.utils import PhotoManager
from app.config import config

# Just a minimal test app to verify photo loading
class TestPhotoApp(App):
    def build(self):
        self.db = DatabaseManager()
        self.photo_manager = PhotoManager(config.photos_dir)

        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # Get properties
        properties = self.db.get_properties()
        if not properties:
            layout.add_widget(Button(text="No properties found!"))
            return layout

        # Use the first property for testing
        test_property = properties[0]
        company_code = test_property.get('Companyco')

        # Display property info
        property_info = f"Testing with: {company_code}"
        info_btn = Button(text=property_info, size_hint_y=None, height=dp(50))
        layout.add_widget(info_btn)

        # Button to get photos
        get_photos_btn = Button(
            text="Get Photos",
            size_hint_y=None,
            height=dp(50),
            on_press=lambda x: self.get_photos(company_code)
        )
        layout.add_widget(get_photos_btn)

        # Results display
        self.results_button = Button(text="Press 'Get Photos' to test", size_hint_y=None, height=dp(50))
        layout.add_widget(self.results_button)

        return layout

    def get_photos(self, company_code):
        """Test getting photos for a property"""
        try:
            photos = self.db.get_property_photos(company_code)

            if not photos:
                self.results_button.text = "No photos found for this property"
                return

            # Verify the photos have the expected fields
            for photo in photos:
                if 'photo_path' not in photo or 'photo_name' not in photo:
                    self.results_button.text = f"Error: Missing required fields in photo data"
                    return

                # Check if file exists
                if not os.path.exists(photo['photo_path']):
                    self.results_button.text = f"Error: Photo file not found: {photo['photo_path']}"
                    return

            self.results_button.text = f"Success! Found {len(photos)} photos with all required fields"

        except Exception as e:
            self.results_button.text = f"Error: {str(e)}"

if __name__ == "__main__":
    TestPhotoApp().run()
