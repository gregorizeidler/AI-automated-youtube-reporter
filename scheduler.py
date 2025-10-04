"""Intelligent scheduling system for optimal posting times."""

from datetime import datetime, time as dt_time, timedelta
from typing import List, Dict, Optional
import json
from pathlib import Path


class IntelligentScheduler:
    """Smart scheduler that posts at optimal times based on category and analytics."""
    
    # Peak engagement times by category (based on general YouTube analytics)
    OPTIMAL_TIMES = {
        'sports': [
            dt_time(18, 0),  # 6 PM - After work
            dt_time(20, 0),  # 8 PM - Prime time
            dt_time(12, 0),  # 12 PM - Lunch break
        ],
        'politics': [
            dt_time(7, 0),   # 7 AM - Morning news
            dt_time(12, 0),  # 12 PM - Lunch break
            dt_time(18, 0),  # 6 PM - Evening news
        ],
        'finance': [
            dt_time(8, 0),   # 8 AM - Market opens
            dt_time(12, 0),  # 12 PM - Lunch trading
            dt_time(16, 0),  # 4 PM - Market close
        ],
        'technology': [
            dt_time(10, 0),  # 10 AM - Morning browse
            dt_time(14, 0),  # 2 PM - Afternoon break
            dt_time(21, 0),  # 9 PM - Evening
        ],
        'entertainment': [
            dt_time(19, 0),  # 7 PM - After dinner
            dt_time(21, 0),  # 9 PM - Prime time
            dt_time(15, 0),  # 3 PM - Weekend afternoon
        ],
        'default': [
            dt_time(12, 0),  # 12 PM
            dt_time(18, 0),  # 6 PM
            dt_time(20, 0),  # 8 PM
        ]
    }
    
    # Days of week preference (0 = Monday, 6 = Sunday)
    OPTIMAL_DAYS = {
        'sports': [5, 6, 0, 1],  # Weekend and Monday/Tuesday
        'politics': [0, 1, 2, 3, 4],  # Weekdays
        'finance': [0, 1, 2, 3, 4],  # Weekdays
        'technology': [0, 1, 2, 3, 4],  # Weekdays
        'entertainment': [4, 5, 6],  # Weekend
        'default': [0, 1, 2, 3, 4, 5, 6]  # Any day
    }
    
    def __init__(self, schedule_file: str = "schedule.json"):
        """Initialize scheduler."""
        self.schedule_file = Path(schedule_file)
        self.schedule = self.load_schedule()
    
    def load_schedule(self) -> Dict:
        """Load existing schedule from file."""
        if self.schedule_file.exists():
            try:
                with open(self.schedule_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error loading schedule: {e}")
                return {'scheduled': [], 'published': []}
        return {'scheduled': [], 'published': []}
    
    def save_schedule(self):
        """Save schedule to file."""
        try:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.schedule, f, indent=2, default=str)
        except Exception as e:
            print(f"❌ Error saving schedule: {e}")
    
    def get_next_optimal_time(
        self, 
        category: str, 
        min_hours_gap: int = 4,
        timezone_offset: int = 0
    ) -> datetime:
        """
        Get next optimal posting time for category.
        
        Args:
            category: Content category
            min_hours_gap: Minimum hours between posts
            timezone_offset: Timezone offset from UTC (e.g., -3 for Brazil)
        """
        now = datetime.now()
        optimal_times = self.OPTIMAL_TIMES.get(category, self.OPTIMAL_TIMES['default'])
        optimal_days = self.OPTIMAL_DAYS.get(category, self.OPTIMAL_DAYS['default'])
        
        # Get recent scheduled times
        recent_times = self._get_recent_scheduled_times(hours_back=min_hours_gap)
        
        # Try next 7 days
        for day_offset in range(7):
            check_date = now + timedelta(days=day_offset)
            
            # Skip if not an optimal day for this category
            if check_date.weekday() not in optimal_days and day_offset > 0:
                continue
            
            for optimal_time in optimal_times:
                scheduled_datetime = datetime.combine(
                    check_date.date(),
                    optimal_time
                )
                
                # Apply timezone offset
                scheduled_datetime += timedelta(hours=timezone_offset)
                
                # Must be in the future
                if scheduled_datetime <= now:
                    continue
                
                # Check minimum gap
                if self._has_minimum_gap(scheduled_datetime, recent_times, min_hours_gap):
                    return scheduled_datetime
        
        # Fallback: just add min_hours_gap to now
        return now + timedelta(hours=min_hours_gap)
    
    def _get_recent_scheduled_times(self, hours_back: int = 24) -> List[datetime]:
        """Get recently scheduled times."""
        cutoff = datetime.now() - timedelta(hours=hours_back)
        recent = []
        
        for item in self.schedule.get('scheduled', []):
            scheduled_time = datetime.fromisoformat(item['scheduled_time'])
            if scheduled_time >= cutoff:
                recent.append(scheduled_time)
        
        return recent
    
    def _has_minimum_gap(
        self, 
        candidate_time: datetime, 
        existing_times: List[datetime], 
        min_hours: int
    ) -> bool:
        """Check if candidate time has minimum gap from existing times."""
        for existing_time in existing_times:
            time_diff = abs((candidate_time - existing_time).total_seconds() / 3600)
            if time_diff < min_hours:
                return False
        return True
    
    def schedule_video(
        self, 
        video_id: int, 
        category: str, 
        title: str,
        scheduled_time: Optional[datetime] = None
    ) -> datetime:
        """
        Schedule a video for publication.
        
        Args:
            video_id: Video database ID
            category: Video category
            title: Video title
            scheduled_time: Specific time or None for auto-schedule
        """
        if scheduled_time is None:
            scheduled_time = self.get_next_optimal_time(category)
        
        schedule_entry = {
            'video_id': video_id,
            'category': category,
            'title': title,
            'scheduled_time': scheduled_time.isoformat(),
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        self.schedule['scheduled'].append(schedule_entry)
        self.save_schedule()
        
        print(f"📅 Scheduled: '{title}' for {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        
        return scheduled_time
    
    def get_due_videos(self) -> List[Dict]:
        """Get videos that are due for publication."""
        now = datetime.now()
        due_videos = []
        
        for item in self.schedule.get('scheduled', []):
            if item['status'] != 'pending':
                continue
            
            scheduled_time = datetime.fromisoformat(item['scheduled_time'])
            if scheduled_time <= now:
                due_videos.append(item)
        
        return due_videos
    
    def mark_published(self, video_id: int, youtube_url: str):
        """Mark video as published."""
        for item in self.schedule.get('scheduled', []):
            if item.get('video_id') == video_id:
                item['status'] = 'published'
                item['published_at'] = datetime.now().isoformat()
                item['youtube_url'] = youtube_url
                
                # Move to published list
                self.schedule['published'].append(item)
                
                self.save_schedule()
                break
    
    def get_upcoming_schedule(self, days: int = 7) -> List[Dict]:
        """Get upcoming schedule for next N days."""
        cutoff = datetime.now() + timedelta(days=days)
        upcoming = []
        
        for item in self.schedule.get('scheduled', []):
            if item['status'] != 'pending':
                continue
            
            scheduled_time = datetime.fromisoformat(item['scheduled_time'])
            if scheduled_time <= cutoff:
                upcoming.append(item)
        
        # Sort by time
        upcoming.sort(key=lambda x: x['scheduled_time'])
        
        return upcoming
    
    def print_schedule(self, days: int = 7):
        """Print upcoming schedule."""
        upcoming = self.get_upcoming_schedule(days)
        
        if not upcoming:
            print("\n📅 No videos scheduled")
            return
        
        print(f"\n📅 Upcoming Schedule (next {days} days):")
        print("=" * 80)
        
        for item in upcoming:
            scheduled_time = datetime.fromisoformat(item['scheduled_time'])
            print(f"{scheduled_time.strftime('%Y-%m-%d %H:%M')} - [{item['category']}] {item['title']}")
        
        print("=" * 80)

