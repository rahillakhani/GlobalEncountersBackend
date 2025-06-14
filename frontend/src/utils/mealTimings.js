import mealTimingsConfig from "../../public/meal_timings.json";

class MealTimings {
  constructor() {
    this.config = mealTimingsConfig;
  }

  // Convert time string (HH:MM) to minutes for easier comparison
  timeToMinutes(timeStr) {
    const [hours, minutes] = timeStr.split(":").map(Number);
    return hours * 60 + minutes;
  }

  // Get current time in minutes
  getCurrentTimeInMinutes() {
    const now = new Date();
    return now.getHours() * 60 + now.getMinutes();
  }

  // Check if current time is within meal service hours
  isMealTimeValid(mealType) {
    const currentMinutes = this.getCurrentTimeInMinutes();
    const startMinutes = this.timeToMinutes(this.config[mealType].start_time);
    const endMinutes = this.timeToMinutes(this.config[mealType].end_time);

    return currentMinutes >= startMinutes && currentMinutes <= endMinutes;
  }

  // Check if a meal scan is late
  isMealLate(mealType, scanTime) {
    const scanMinutes = this.timeToMinutes(scanTime);
    const endMinutes = this.timeToMinutes(this.config[mealType].end_time);
    const lateThreshold = this.config.meal_window.late_threshold;

    return scanMinutes > endMinutes + lateThreshold;
  }

  // Check if a meal scan is early
  isMealEarly(mealType, scanTime) {
    const scanMinutes = this.timeToMinutes(scanTime);
    const startMinutes = this.timeToMinutes(this.config[mealType].start_time);
    const earlyThreshold = this.config.meal_window.early_threshold;

    return scanMinutes < startMinutes - earlyThreshold;
  }

  // Get meal display name
  getMealName(mealType) {
    return this.config[mealType].name;
  }

  // Get meal description
  getMealDescription(mealType) {
    return this.config[mealType].description;
  }

  // Get formatted meal times for display
  getMealDisplayTimes(mealType) {
    return {
      start: this.config[mealType].display_start,
      end: this.config[mealType].display_end,
    };
  }

  // Get all active meal types
  getActiveMeals() {
    const meals = ["lunch", "dinner"];
    return meals.filter((meal) => this.isMealTimeValid(meal));
  }

  // Get next meal
  getNextMeal() {
    const currentMinutes = this.getCurrentTimeInMinutes();
    const meals = ["lunch", "dinner"];

    for (const meal of meals) {
      const startMinutes = this.timeToMinutes(this.config[meal].start_time);
      if (currentMinutes < startMinutes) {
        return {
          type: meal,
          name: this.getMealName(meal),
          startTime: this.config[meal].display_start,
          timeUntil: startMinutes - currentMinutes,
        };
      }
    }

    // If no next meal today, return first meal of next day
    return {
      type: "lunch",
      name: this.getMealName("lunch"),
      startTime: this.config.lunch.display_start,
      timeUntil:
        24 * 60 -
        currentMinutes +
        this.timeToMinutes(this.config.lunch.start_time),
    };
  }

  // Format minutes into hours and minutes
  formatTimeUntil(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h ${mins}m`;
    }
    return `${mins}m`;
  }
}

// Create and export a singleton instance
export const mealTimings = new MealTimings();
