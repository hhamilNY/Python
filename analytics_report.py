#!/usr/bin/env python3
"""
Analytics Report Generator for USGS Earthquake Monitor
Generates visitor and usage statistics from log files
"""

import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json

def parse_log_file(log_path):
    """Parse the earthquake app log file and extract analytics"""
    if not os.path.exists(log_path):
        print(f"❌ Log file not found: {log_path}")
        return None
    
    analytics = {
        "unique_visitors": set(),
        "daily_visitors": defaultdict(int),
        "page_views": 0,
        "sessions": set(),
        "data_sources": Counter(),
        "view_types": Counter(),
        "user_actions": Counter(),
        "errors": [],
        "performance_metrics": [],
        "hourly_activity": defaultdict(int)
    }
    
    print(f"📖 Reading log file: {log_path}")
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            try:
                parts = line.strip().split(" | ")
                if len(parts) < 4:
                    continue
                
                timestamp_str = parts[0]
                level = parts[1].strip()
                function = parts[2].strip()
                message = parts[3]
                
                # Parse timestamp
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    date_str = timestamp.strftime("%Y-%m-%d")
                    hour_str = timestamp.strftime("%H")
                    analytics["hourly_activity"][hour_str] += 1
                except:
                    continue
                
                # Track visitors
                if "NEW_VISITOR" in message:
                    try:
                        visitor_id = message.split("ID: ")[1].split(" |")[0]
                        analytics["unique_visitors"].add(visitor_id)
                        analytics["daily_visitors"][date_str] += 1
                    except:
                        pass
                
                # Track page views
                elif "PAGE_VIEW" in message:
                    analytics["page_views"] += 1
                
                # Track sessions
                elif "SESSION_START" in message:
                    try:
                        session_id = message.split("session: ")[1].split(" |")[0]
                        analytics["sessions"].add(session_id)
                    except:
                        pass
                
                # Track user actions
                elif "USER_ACTION" in message:
                    try:
                        action = message.split("Action: ")[1].split(" |")[0]
                        analytics["user_actions"][action] += 1
                        
                        # Track specific data source changes
                        if "data_source_change" in action and "Details: " in message:
                            source = message.split("Details: ")[1].strip()
                            analytics["data_sources"][source] += 1
                        
                        # Track view changes
                        elif "view_change" in action and "Details: " in message:
                            view = message.split("Details: ")[1].strip()
                            analytics["view_types"][view] += 1
                    except:
                        pass
                
                # Track errors
                elif level == "ERROR":
                    analytics["errors"].append({
                        "timestamp": timestamp_str,
                        "message": message,
                        "line": line_num
                    })
                
                # Track performance
                elif "Completed" in message and " in " in message:
                    try:
                        func_name = message.split("Completed ")[1].split(" in ")[0]
                        time_str = message.split(" in ")[1].split("s")[0]
                        exec_time = float(time_str)
                        analytics["performance_metrics"].append({
                            "function": func_name,
                            "time": exec_time,
                            "timestamp": timestamp_str
                        })
                    except:
                        pass
                        
            except Exception as e:
                print(f"⚠️  Error parsing line {line_num}: {e}")
                continue
    
    except Exception as e:
        print(f"❌ Error reading log file: {e}")
        return None
    
    # Convert sets to counts for JSON serialization
    analytics["unique_visitor_count"] = len(analytics["unique_visitors"])
    analytics["session_count"] = len(analytics["sessions"])
    analytics["unique_visitors"] = list(analytics["unique_visitors"])
    analytics["sessions"] = list(analytics["sessions"])
    
    return analytics

def generate_report(analytics):
    """Generate a formatted analytics report"""
    if not analytics:
        return "❌ No analytics data available"
    
    report = []
    report.append("🌍 USGS Earthquake Monitor - Analytics Report")
    report.append("=" * 50)
    report.append(f"📊 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Visitor Statistics
    report.append("👥 VISITOR STATISTICS")
    report.append("-" * 25)
    report.append(f"🌟 Unique Visitors: {analytics['unique_visitor_count']}")
    report.append(f"👀 Total Page Views: {analytics['page_views']}")
    report.append(f"🔗 Unique Sessions: {analytics['session_count']}")
    
    if analytics['page_views'] > 0 and analytics['unique_visitor_count'] > 0:
        avg_pages = analytics['page_views'] / analytics['unique_visitor_count']
        report.append(f"📈 Avg Pages per Visitor: {avg_pages:.1f}")
    
    report.append("")
    
    # Daily Activity
    if analytics['daily_visitors']:
        report.append("📅 DAILY VISITOR ACTIVITY")
        report.append("-" * 25)
        sorted_days = sorted(analytics['daily_visitors'].items())
        for date, count in sorted_days[-7:]:  # Last 7 days
            report.append(f"📆 {date}: {count} new visitors")
        report.append("")
    
    # Hourly Activity
    if analytics['hourly_activity']:
        report.append("⏰ HOURLY ACTIVITY PATTERN")
        report.append("-" * 25)
        sorted_hours = sorted(analytics['hourly_activity'].items())
        for hour, count in sorted_hours:
            bar = "█" * min(count // 5, 20)  # Simple bar chart
            report.append(f"{hour}:00 | {count:3d} | {bar}")
        report.append("")
    
    # Popular Features
    if analytics['data_sources']:
        report.append("📡 POPULAR DATA SOURCES")
        report.append("-" * 25)
        for source, count in analytics['data_sources'].most_common(5):
            report.append(f"🔸 {source}: {count} selections")
        report.append("")
    
    if analytics['view_types']:
        report.append("📱 POPULAR VIEW TYPES")
        report.append("-" * 25)
        for view, count in analytics['view_types'].most_common(5):
            report.append(f"🔸 {view}: {count} selections")
        report.append("")
    
    # User Actions
    if analytics['user_actions']:
        report.append("🎯 USER ACTIONS")
        report.append("-" * 25)
        for action, count in analytics['user_actions'].most_common(5):
            report.append(f"🔸 {action}: {count} times")
        report.append("")
    
    # Performance Metrics
    if analytics['performance_metrics']:
        report.append("⚡ PERFORMANCE METRICS")
        report.append("-" * 25)
        
        # Group by function
        func_times = defaultdict(list)
        for metric in analytics['performance_metrics']:
            func_times[metric['function']].append(metric['time'])
        
        for func, times in func_times.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)
            report.append(f"🔸 {func}: avg {avg_time:.3f}s, max {max_time:.3f}s ({len(times)} calls)")
        report.append("")
    
    # Error Summary
    if analytics['errors']:
        report.append("⚠️  ERROR SUMMARY")
        report.append("-" * 25)
        report.append(f"🔴 Total Errors: {len(analytics['errors'])}")
        
        # Show recent errors
        recent_errors = analytics['errors'][-5:]
        for error in recent_errors:
            timestamp = error['timestamp']
            message = error['message'][:80] + "..." if len(error['message']) > 80 else error['message']
            report.append(f"🔸 {timestamp}: {message}")
        report.append("")
    
    # Summary
    report.append("📋 SUMMARY")
    report.append("-" * 25)
    if analytics['unique_visitor_count'] > 0:
        report.append("✅ Application is actively being used")
        report.append(f"📊 {analytics['unique_visitor_count']} people have visited the earthquake monitor")
        report.append(f"📈 {analytics['page_views']} total page interactions")
    else:
        report.append("ℹ️  No visitor activity detected yet")
    
    if analytics['errors']:
        error_rate = len(analytics['errors']) / max(analytics['page_views'], 1) * 100
        report.append(f"⚠️  Error rate: {error_rate:.1f}%")
    
    return "\n".join(report)

def save_json_report(analytics, filename):
    """Save analytics data as JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analytics, f, indent=2, default=str)
        print(f"💾 JSON report saved: {filename}")
    except Exception as e:
        print(f"❌ Error saving JSON report: {e}")

def main():
    """Main analytics report generator"""
    print("🌍 USGS Earthquake Monitor - Analytics Report Generator")
    print("=" * 60)
    
    # Default log file path
    log_path = os.path.join("logs", "earthquake_app.log")
    
    # Allow custom log path as command line argument
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    
    # Parse the log file
    analytics = parse_log_file(log_path)
    
    if not analytics:
        print("❌ Failed to generate analytics report")
        return
    
    # Generate and display report
    report = generate_report(analytics)
    print("\n" + report)
    
    # Save reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save text report
    report_filename = f"analytics_report_{timestamp}.txt"
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n💾 Report saved: {report_filename}")
    except Exception as e:
        print(f"\n❌ Error saving report: {e}")
    
    # Save JSON data
    json_filename = f"analytics_data_{timestamp}.json"
    save_json_report(analytics, json_filename)
    
    print(f"\n✅ Analytics report generation complete!")
    print(f"📊 {analytics['unique_visitor_count']} unique visitors tracked")
    print(f"👀 {analytics['page_views']} page views recorded")

if __name__ == "__main__":
    main()