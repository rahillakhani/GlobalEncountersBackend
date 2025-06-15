from pydantic import BaseModel
from typing import Dict

class MealWindow(BaseModel):
    early_threshold: int
    late_threshold: int

class MealTiming(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str
    display_start: str
    display_end: str

class MealTimingsResponse(BaseModel):
    lunch: MealTiming
    dinner: MealTiming
    meal_window: MealWindow 