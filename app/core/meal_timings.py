from datetime import datetime, time
from typing import Dict, Optional, Tuple
import yaml
import os
from pathlib import Path

class MealTimings:
    def __init__(self):
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load meal timing configurations from YAML file"""
        config_path = Path(__file__).parent / "meal_timings.yml"
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise Exception(f"Error loading meal timings configuration: {str(e)}")

    def _parse_time(self, time_str: str) -> time:
        """Convert time string to datetime.time object"""
        return datetime.strptime(time_str, "%H:%M").time()

    def get_meal_timings(self, meal_type: str) -> Tuple[time, time]:
        """Get start and end time for a specific meal type"""
        if meal_type not in ['lunch', 'dinner']:
            raise ValueError(f"Invalid meal type: {meal_type}")
        
        meal_config = self.config[meal_type]
        start_time = self._parse_time(meal_config['start_time'])
        end_time = self._parse_time(meal_config['end_time'])
        return start_time, end_time

    def is_meal_time_valid(self, meal_type: str, current_time: Optional[datetime] = None) -> bool:
        """
        Check if the current time is within valid meal service hours
        
        Args:
            meal_type: 'lunch' or 'dinner'
            current_time: datetime object (defaults to current time if None)
            
        Returns:
            bool: True if current time is within meal service hours
        """
        if current_time is None:
            current_time = datetime.now()
        
        start_time, end_time = self.get_meal_timings(meal_type)
        current_time_only = current_time.time()
        
        # Check if current time is within meal service hours
        return start_time <= current_time_only <= end_time

    def is_meal_late(self, meal_type: str, scan_time: datetime) -> bool:
        """
        Check if a meal scan is late based on the late threshold
        
        Args:
            meal_type: 'lunch' or 'dinner'
            scan_time: datetime when the meal was scanned
            
        Returns:
            bool: True if the meal scan is considered late
        """
        _, end_time = self.get_meal_timings(meal_type)
        scan_time_only = scan_time.time()
        
        # Convert times to minutes for easier comparison
        end_minutes = end_time.hour * 60 + end_time.minute
        scan_minutes = scan_time_only.hour * 60 + scan_time_only.minute
        
        late_threshold = self.config['meal_window']['late_threshold']
        return scan_minutes > (end_minutes + late_threshold)

    def is_meal_early(self, meal_type: str, scan_time: datetime) -> bool:
        """
        Check if a meal scan is too early based on the early threshold
        
        Args:
            meal_type: 'lunch' or 'dinner'
            scan_time: datetime when the meal was scanned
            
        Returns:
            bool: True if the meal scan is too early
        """
        start_time, _ = self.get_meal_timings(meal_type)
        scan_time_only = scan_time.time()
        
        # Convert times to minutes for easier comparison
        start_minutes = start_time.hour * 60 + start_time.minute
        scan_minutes = scan_time_only.hour * 60 + scan_time_only.minute
        
        early_threshold = self.config['meal_window']['early_threshold']
        return scan_minutes < (start_minutes - early_threshold)

    def get_meal_name(self, meal_type: str) -> str:
        """Get the display name for a meal type"""
        return self.config[meal_type]['name']

    def get_meal_description(self, meal_type: str) -> str:
        """Get the description for a meal type"""
        return self.config[meal_type]['description']

# Create a singleton instance
meal_timings = MealTimings() 