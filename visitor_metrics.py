"""
Persistent Visitor Metrics Storage System
Maintains key metrics even when log files rotate
"""

import json
import os
import threading
from datetime import datetime, timedelta
from collections import defaultdict
import logging

class PersistentMetrics:
    """Thread-safe persistent metrics storage"""
    
    def __init__(self, metrics_file="metrics/visitor_metrics.json"):
        self.metrics_file = metrics_file
        self.lock = threading.Lock()
        self._ensure_metrics_dir()
        self.metrics = self._load_metrics()
    
    def _ensure_metrics_dir(self):
        """Create metrics directory if it doesn't exist"""
        metrics_dir = os.path.dirname(self.metrics_file)
        if metrics_dir and not os.path.exists(metrics_dir):
            os.makedirs(metrics_dir)
    
    def _load_metrics(self):
        """Load metrics from persistent storage"""
        default_metrics = {
            "total_unique_visitors": set(),
            "total_page_views": 0,
            "daily_visitors": defaultdict(int),
            "daily_page_views": defaultdict(int),
            "popular_data_sources": defaultdict(int),
            "popular_views": defaultdict(int),
            "user_actions": defaultdict(int),
            "total_sessions": set(),
            "first_visit_date": None,
            "last_updated": None,
            "version": "1.0"
        }
        
        try:
            if os.path.exists(self.metrics_file):
                with open(self.metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert sets back from lists
                if 'total_unique_visitors' in data:
                    data['total_unique_visitors'] = set(data['total_unique_visitors'])
                else:
                    data['total_unique_visitors'] = set()
                
                if 'total_sessions' in data:
                    data['total_sessions'] = set(data['total_sessions'])
                else:
                    data['total_sessions'] = set()
                
                # Convert defaultdicts
                for key in ['daily_visitors', 'daily_page_views', 'popular_data_sources', 
                           'popular_views', 'user_actions']:
                    if key in data:
                        data[key] = defaultdict(int, data[key])
                    else:
                        data[key] = defaultdict(int)
                
                # Merge with defaults for any missing keys
                for key, value in default_metrics.items():
                    if key not in data:
                        data[key] = value
                
                return data
            else:
                return default_metrics
                
        except Exception as e:
            logging.error(f"METRICS_ERROR | Failed to load metrics: {e}")
            return default_metrics
    
    def _save_metrics(self):
        """Save metrics to persistent storage"""
        try:
            # Convert sets and defaultdicts for JSON serialization
            data = dict(self.metrics)
            data['total_unique_visitors'] = list(self.metrics['total_unique_visitors'])
            data['total_sessions'] = list(self.metrics['total_sessions'])
            
            for key in ['daily_visitors', 'daily_page_views', 'popular_data_sources', 
                       'popular_views', 'user_actions']:
                data[key] = dict(self.metrics[key])
            
            data['last_updated'] = datetime.now().isoformat()
            
            with open(self.metrics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"METRICS_ERROR | Failed to save metrics: {e}")
    
    def record_new_visitor(self, visitor_id):
        """Record a new unique visitor"""
        with self.lock:
            if visitor_id not in self.metrics['total_unique_visitors']:
                self.metrics['total_unique_visitors'].add(visitor_id)
                today = datetime.now().strftime("%Y-%m-%d")
                self.metrics['daily_visitors'][today] += 1
                
                if not self.metrics['first_visit_date']:
                    self.metrics['first_visit_date'] = today
                
                self._save_metrics()
    
    def record_page_view(self, visitor_id=None):
        """Record a page view"""
        with self.lock:
            self.metrics['total_page_views'] += 1
            today = datetime.now().strftime("%Y-%m-%d")
            self.metrics['daily_page_views'][today] += 1
            self._save_metrics()
    
    def record_session(self, session_id):
        """Record a new session"""
        with self.lock:
            if session_id not in self.metrics['total_sessions']:
                self.metrics['total_sessions'].add(session_id)
                self._save_metrics()
    
    def record_user_action(self, action, details=None):
        """Record user action"""
        with self.lock:
            if details:
                action_key = f"{action}:{details}"
                
                # Track popular data sources and views separately
                if action == "data_source_change":
                    self.metrics['popular_data_sources'][details] += 1
                elif action == "view_change":
                    self.metrics['popular_views'][details] += 1
            else:
                action_key = action
            
            self.metrics['user_actions'][action_key] += 1
            self._save_metrics()
    
    def get_summary_stats(self):
        """Get summary statistics"""
        with self.lock:
            today = datetime.now().strftime("%Y-%m-%d")
            
            return {
                "total_unique_visitors": len(self.metrics['total_unique_visitors']),
                "total_page_views": self.metrics['total_page_views'],
                "total_sessions": len(self.metrics['total_sessions']),
                "new_visitors_today": self.metrics['daily_visitors'][today],
                "page_views_today": self.metrics['daily_page_views'][today],
                "first_visit_date": self.metrics['first_visit_date'],
                "days_active": len(self.metrics['daily_visitors']),
                "avg_page_views_per_visitor": (
                    self.metrics['total_page_views'] / max(1, len(self.metrics['total_unique_visitors']))
                )
            }
    
    def get_daily_stats(self, days=30):
        """Get daily statistics for the past N days"""
        with self.lock:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            daily_data = []
            current_date = start_date
            
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                daily_data.append({
                    "date": date_str,
                    "visitors": self.metrics['daily_visitors'][date_str],
                    "page_views": self.metrics['daily_page_views'][date_str]
                })
                current_date += timedelta(days=1)
            
            return daily_data
    
    def get_popular_items(self):
        """Get popular data sources and views"""
        with self.lock:
            return {
                "data_sources": dict(sorted(self.metrics['popular_data_sources'].items(), 
                                          key=lambda x: x[1], reverse=True)[:10]),
                "views": dict(sorted(self.metrics['popular_views'].items(), 
                                   key=lambda x: x[1], reverse=True)[:10]),
                "actions": dict(sorted(self.metrics['user_actions'].items(), 
                                     key=lambda x: x[1], reverse=True)[:10])
            }
    
    def cleanup_old_data(self, days_to_keep=90):
        """Clean up old daily data to prevent file from growing too large"""
        with self.lock:
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime("%Y-%m-%d")
            
            # Clean daily visitors
            old_dates = [date for date in self.metrics['daily_visitors'].keys() if date < cutoff_date]
            for date in old_dates:
                del self.metrics['daily_visitors'][date]
            
            # Clean daily page views
            old_dates = [date for date in self.metrics['daily_page_views'].keys() if date < cutoff_date]
            for date in old_dates:
                del self.metrics['daily_page_views'][date]
            
            if old_dates:
                self._save_metrics()
                logging.info(f"METRICS_CLEANUP | Removed data older than {cutoff_date}")
    
    def export_metrics(self, export_file=None):
        """Export all metrics to a file"""
        if not export_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"metrics/metrics_export_{timestamp}.json"
        
        try:
            with self.lock:
                # Get a copy of current metrics for export
                export_data = dict(self.metrics)
                export_data['total_unique_visitors'] = list(self.metrics['total_unique_visitors'])
                export_data['total_sessions'] = list(self.metrics['total_sessions'])
                
                for key in ['daily_visitors', 'daily_page_views', 'popular_data_sources', 
                           'popular_views', 'user_actions']:
                    export_data[key] = dict(self.metrics[key])
                
                export_data['export_timestamp'] = datetime.now().isoformat()
                
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                return export_file
        except Exception as e:
            logging.error(f"METRICS_ERROR | Failed to export metrics: {e}")
            return None

# Global metrics instance
_metrics_instance = None

def get_metrics():
    """Get the global metrics instance (singleton pattern)"""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = PersistentMetrics()
    return _metrics_instance

def migrate_from_logs():
    """Migrate existing metrics from log files to persistent storage"""
    try:
        import os
        log_file = os.path.join("logs", "earthquake_app.log")
        
        if not os.path.exists(log_file):
            return
        
        metrics = get_metrics()
        visitors_processed = set()
        sessions_processed = set()
        
        print("🔄 Migrating metrics from log files...")
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    if "NEW_VISITOR" in line:
                        visitor_id = line.split("ID: ")[1].split(" |")[0]
                        if visitor_id not in visitors_processed:
                            metrics.record_new_visitor(visitor_id)
                            visitors_processed.add(visitor_id)
                    
                    elif "PAGE_VIEW" in line:
                        metrics.record_page_view()
                    
                    elif "SESSION_START" in line:
                        session_id = line.split("session: ")[1].split(" |")[0]
                        if session_id not in sessions_processed:
                            metrics.record_session(session_id)
                            sessions_processed.add(session_id)
                    
                    elif "data_source_change" in line:
                        source = line.split("Details: ")[1].strip()
                        metrics.record_user_action("data_source_change", source)
                    
                    elif "view_change" in line:
                        view = line.split("Details: ")[1].strip()
                        metrics.record_user_action("view_change", view)
                        
                except:
                    continue
        
        stats = metrics.get_summary_stats()
        print(f"✅ Migration complete! Found {stats['total_unique_visitors']} visitors, {stats['total_page_views']} page views")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    # Run migration if this script is executed directly
    migrate_from_logs()
    
    # Show current stats
    metrics = get_metrics()
    stats = metrics.get_summary_stats()
    
    print("\n📊 Current Metrics Summary:")
    print(f"• Total Unique Visitors: {stats['total_unique_visitors']}")
    print(f"• Total Page Views: {stats['total_page_views']}")
    print(f"• Total Sessions: {stats['total_sessions']}")
    print(f"• Days Active: {stats['days_active']}")
    print(f"• Avg Page Views per Visitor: {stats['avg_page_views_per_visitor']:.1f}")
    
    if stats['first_visit_date']:
        print(f"• First Visit: {stats['first_visit_date']}")