"""
Enhanced User Session Management System
Provides comprehensive user tracking with location, device, and security features
"""

import json
import os
import threading
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import hashlib
import requests

class UserSessionManager:
    """Enhanced user session management with location and security tracking"""
    
    def __init__(self, sessions_file="sessions/user_sessions.json"):
        self.sessions_file = sessions_file
        self.lock = threading.Lock()
        self._ensure_sessions_dir()
        self.sessions = self._load_sessions()
        self.active_sessions = {}  # In-memory active session cache
    
    def _ensure_sessions_dir(self):
        """Create sessions directory if it doesn't exist"""
        sessions_dir = os.path.dirname(self.sessions_file)
        if sessions_dir and not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)
    
    def _load_sessions(self):
        """Load session data from persistent storage"""
        default_data = {
            "user_sessions": {},
            "login_history": [],
            "security_events": [],
            "device_fingerprints": {},
            "location_history": {},
            "session_analytics": {
                "total_logins": 0,
                "unique_locations": set(),
                "unique_devices": set(),
                "suspicious_activities": 0
            },
            "metadata": {
                "created_date": datetime.now().isoformat(),
                "last_updated": None,
                "version": "1.0"
            }
        }
        
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert sets back from lists
                if 'session_analytics' in data:
                    analytics = data['session_analytics']
                    if 'unique_locations' in analytics:
                        analytics['unique_locations'] = set(analytics['unique_locations'])
                    if 'unique_devices' in analytics:
                        analytics['unique_devices'] = set(analytics['unique_devices'])
                
                # Merge with defaults for missing keys
                for key, value in default_data.items():
                    if key not in data:
                        data[key] = value
                
                return data
            else:
                return default_data
                
        except Exception as e:
            logging.error(f"SESSION_ERROR | Failed to load sessions: {e}")
            return default_data
    
    def _save_sessions(self):
        """Save session data to persistent storage"""
        try:
            # Convert sets for JSON serialization
            data = dict(self.sessions)
            if 'session_analytics' in data:
                analytics = data['session_analytics']
                if 'unique_locations' in analytics:
                    analytics['unique_locations'] = list(analytics['unique_locations'])
                if 'unique_devices' in analytics:
                    analytics['unique_devices'] = list(analytics['unique_devices'])
            
            data['metadata']['last_updated'] = datetime.now().isoformat()
            
            with open(self.sessions_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"SESSION_ERROR | Failed to save sessions: {e}")
    
    def _get_client_ip(self, request_headers):
        """Extract client IP from request headers"""
        # Try various headers that might contain the real IP
        ip_headers = [
            'X-Forwarded-For',
            'X-Real-IP',
            'X-Client-IP',
            'CF-Connecting-IP',  # Cloudflare
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_REAL_IP'
        ]
        
        for header in ip_headers:
            if header in request_headers:
                ip = request_headers[header].split(',')[0].strip()
                if ip and ip != 'unknown':
                    return ip
        
        return request_headers.get('Remote-Addr', 'unknown')
    
    def _get_location_from_ip(self, ip_address):
        """Get location information from IP address using free IP geolocation API"""
        try:
            if ip_address in ['127.0.0.1', 'localhost', 'unknown']:
                return {
                    'country': 'Local',
                    'region': 'Local',
                    'city': 'Local',
                    'timezone': 'Local',
                    'isp': 'Local'
                }
            
            # Use free IP geolocation service
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    return {
                        'country': data.get('country', 'Unknown'),
                        'region': data.get('regionName', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'timezone': data.get('timezone', 'Unknown'),
                        'isp': data.get('isp', 'Unknown'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon')
                    }
        except Exception as e:
            logging.warning(f"LOCATION_ERROR | Failed to get location for IP {ip_address}: {e}")
        
        return {
            'country': 'Unknown',
            'region': 'Unknown', 
            'city': 'Unknown',
            'timezone': 'Unknown',
            'isp': 'Unknown'
        }
    
    def _create_device_fingerprint(self, user_agent, screen_resolution=None, timezone=None):
        """Create a device fingerprint from available information"""
        fingerprint_data = {
            'user_agent': user_agent or 'unknown',
            'screen_resolution': screen_resolution or 'unknown',
            'timezone': timezone or 'unknown'
        }
        
        # Create hash of combined data
        fingerprint_string = f"{fingerprint_data['user_agent']}|{fingerprint_data['screen_resolution']}|{fingerprint_data['timezone']}"
        device_id = hashlib.md5(fingerprint_string.encode()).hexdigest()[:12]
        
        return device_id, fingerprint_data
    
    def create_session(self, visitor_id, request_headers=None, user_agent=None, 
                      screen_resolution=None, timezone=None):
        """Create a new user session with comprehensive tracking"""
        with self.lock:
            session_id = str(uuid.uuid4())
            current_time = datetime.now().isoformat()
            
            # Get client information
            client_ip = self._get_client_ip(request_headers or {})
            location_info = self._get_location_from_ip(client_ip)
            device_id, device_info = self._create_device_fingerprint(
                user_agent, screen_resolution, timezone
            )
            
            # Create session record
            session_data = {
                'session_id': session_id,
                'visitor_id': visitor_id,
                'start_time': current_time,
                'last_activity': current_time,
                'ip_address': client_ip,
                'location': location_info,
                'device_id': device_id,
                'device_info': device_info,
                'page_views': 1,
                'actions': [],
                'duration_minutes': 0,
                'is_active': True,
                'security_flags': {
                    'suspicious_activity': False,
                    'multiple_locations': False,
                    'rapid_requests': False
                }
            }
            
            # Store in sessions
            self.sessions['user_sessions'][session_id] = session_data
            self.active_sessions[session_id] = session_data
            
            # Add to login history
            login_record = {
                'timestamp': current_time,
                'visitor_id': visitor_id,
                'session_id': session_id,
                'ip_address': client_ip,
                'location': location_info,
                'device_id': device_id,
                'login_method': 'browser_session'
            }
            self.sessions['login_history'].append(login_record)
            
            # Update analytics
            analytics = self.sessions['session_analytics']
            analytics['total_logins'] += 1
            analytics['unique_locations'].add(f"{location_info['city']}, {location_info['country']}")
            analytics['unique_devices'].add(device_id)
            
            # Store device fingerprint if new
            if device_id not in self.sessions['device_fingerprints']:
                self.sessions['device_fingerprints'][device_id] = {
                    'first_seen': current_time,
                    'last_seen': current_time,
                    'device_info': device_info,
                    'session_count': 1,
                    'locations_used': [location_info]
                }
            else:
                device_record = self.sessions['device_fingerprints'][device_id]
                device_record['last_seen'] = current_time
                device_record['session_count'] += 1
                
                # Check for multiple locations (potential security concern)
                current_location = f"{location_info['city']}, {location_info['country']}"
                existing_locations = [f"{loc['city']}, {loc['country']}" for loc in device_record['locations_used']]
                
                if current_location not in existing_locations:
                    device_record['locations_used'].append(location_info)
                    if len(device_record['locations_used']) > 2:
                        session_data['security_flags']['multiple_locations'] = True
                        self._log_security_event('multiple_locations', session_id, visitor_id, {
                            'device_id': device_id,
                            'new_location': location_info,
                            'previous_locations': len(device_record['locations_used']) - 1
                        })
            
            # Store location history for this visitor
            if visitor_id not in self.sessions['location_history']:
                self.sessions['location_history'][visitor_id] = []
            
            self.sessions['location_history'][visitor_id].append({
                'timestamp': current_time,
                'location': location_info,
                'ip_address': client_ip,
                'session_id': session_id
            })
            
            self._save_sessions()
            
            logging.info(f"SESSION_CREATED | Session: {session_id} | Visitor: {visitor_id} | Location: {location_info['city']}, {location_info['country']} | IP: {client_ip}")
            
            return session_id, session_data
    
    def _log_security_event(self, event_type, session_id, visitor_id, details):
        """Log security-related events"""
        security_event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'session_id': session_id,
            'visitor_id': visitor_id,
            'details': details,
            'severity': self._get_event_severity(event_type)
        }
        
        self.sessions['security_events'].append(security_event)
        self.sessions['session_analytics']['suspicious_activities'] += 1
        
        logging.warning(f"SECURITY_EVENT | Type: {event_type} | Session: {session_id} | Details: {details}")
    
    def _get_event_severity(self, event_type):
        """Get severity level for security events"""
        severity_map = {
            'multiple_locations': 'medium',
            'rapid_requests': 'low',
            'suspicious_activity': 'high',
            'session_hijacking': 'critical'
        }
        return severity_map.get(event_type, 'low')
    
    def update_session_activity(self, session_id, action=None):
        """Update session with new activity"""
        with self.lock:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                current_time = datetime.now()
                session['last_activity'] = current_time.isoformat()
                
                # Calculate duration
                start_time = datetime.fromisoformat(session['start_time'])
                duration = (current_time - start_time).total_seconds() / 60
                session['duration_minutes'] = round(duration, 2)
                
                if action:
                    session['actions'].append({
                        'timestamp': current_time.isoformat(),
                        'action': action
                    })
                
                # Update in persistent storage
                self.sessions['user_sessions'][session_id] = session
                self._save_sessions()
    
    def end_session(self, session_id):
        """End a user session"""
        with self.lock:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session['is_active'] = False
                session['end_time'] = datetime.now().isoformat()
                
                # Update persistent storage
                self.sessions['user_sessions'][session_id] = session
                
                # Remove from active sessions
                del self.active_sessions[session_id]
                
                self._save_sessions()
                
                logging.info(f"SESSION_ENDED | Session: {session_id} | Duration: {session['duration_minutes']} minutes")
    
    def get_session_info(self, session_id):
        """Get detailed information about a session"""
        with self.lock:
            return self.sessions['user_sessions'].get(session_id)
    
    def get_visitor_sessions(self, visitor_id):
        """Get all sessions for a specific visitor"""
        with self.lock:
            visitor_sessions = []
            for session_data in self.sessions['user_sessions'].values():
                if session_data['visitor_id'] == visitor_id:
                    visitor_sessions.append(session_data)
            return sorted(visitor_sessions, key=lambda x: x['start_time'], reverse=True)
    
    def get_location_history(self, visitor_id):
        """Get location history for a visitor"""
        with self.lock:
            return self.sessions['location_history'].get(visitor_id, [])
    
    def get_security_summary(self):
        """Get security analysis summary"""
        with self.lock:
            recent_events = [
                event for event in self.sessions['security_events']
                if datetime.fromisoformat(event['timestamp']) > datetime.now() - timedelta(days=30)
            ]
            
            return {
                'total_security_events': len(self.sessions['security_events']),
                'recent_events_30_days': len(recent_events),
                'suspicious_activities': self.sessions['session_analytics']['suspicious_activities'],
                'unique_locations': len(self.sessions['session_analytics']['unique_locations']),
                'unique_devices': len(self.sessions['session_analytics']['unique_devices']),
                'recent_events': recent_events[-10:]  # Last 10 events
            }
    
    def get_analytics_summary(self):
        """Get comprehensive analytics summary"""
        with self.lock:
            active_sessions_count = len(self.active_sessions)
            total_sessions = len(self.sessions['user_sessions'])
            
            # Calculate average session duration
            durations = [s['duration_minutes'] for s in self.sessions['user_sessions'].values() 
                        if 'duration_minutes' in s and s['duration_minutes'] > 0]
            avg_duration = sum(durations) / len(durations) if durations else 0
            
            return {
                'total_sessions': total_sessions,
                'active_sessions': active_sessions_count,
                'total_logins': self.sessions['session_analytics']['total_logins'],
                'unique_locations': len(self.sessions['session_analytics']['unique_locations']),
                'unique_devices': len(self.sessions['session_analytics']['unique_devices']),
                'average_session_duration_minutes': round(avg_duration, 2),
                'security_events': len(self.sessions['security_events'])
            }
    
    def cleanup_old_sessions(self, days_to_keep=90):
        """Clean up old session data"""
        with self.lock:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Clean old sessions
            sessions_to_remove = []
            for session_id, session_data in self.sessions['user_sessions'].items():
                session_time = datetime.fromisoformat(session_data['start_time'])
                if session_time < cutoff_date:
                    sessions_to_remove.append(session_id)
            
            for session_id in sessions_to_remove:
                del self.sessions['user_sessions'][session_id]
            
            # Clean old login history
            self.sessions['login_history'] = [
                record for record in self.sessions['login_history']
                if datetime.fromisoformat(record['timestamp']) >= cutoff_date
            ]
            
            # Clean old security events
            self.sessions['security_events'] = [
                event for event in self.sessions['security_events']
                if datetime.fromisoformat(event['timestamp']) >= cutoff_date
            ]
            
            if sessions_to_remove:
                self._save_sessions()
                logging.info(f"SESSION_CLEANUP | Removed {len(sessions_to_remove)} old sessions")
    
    def export_session_data(self, export_file=None):
        """Export all session data"""
        if not export_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"sessions/session_export_{timestamp}.json"
        
        try:
            with self.lock:
                export_data = dict(self.sessions)
                
                # Convert sets for JSON serialization
                if 'session_analytics' in export_data:
                    analytics = export_data['session_analytics']
                    if 'unique_locations' in analytics:
                        analytics['unique_locations'] = list(analytics['unique_locations'])
                    if 'unique_devices' in analytics:
                        analytics['unique_devices'] = list(analytics['unique_devices'])
                
                export_data['export_timestamp'] = datetime.now().isoformat()
                
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                return export_file
        except Exception as e:
            logging.error(f"SESSION_ERROR | Failed to export session data: {e}")
            return None

# Global session manager instance
_session_manager = None

def get_session_manager():
    """Get the global session manager instance (singleton pattern)"""
    global _session_manager
    if _session_manager is None:
        _session_manager = UserSessionManager()
    return _session_manager

if __name__ == "__main__":
    # Test session manager
    manager = get_session_manager()
    
    # Create a test session
    test_headers = {'X-Forwarded-For': '8.8.8.8', 'User-Agent': 'Test Browser'}
    session_id, session_data = manager.create_session('test_visitor_123', test_headers)
    
    print(f"Created session: {session_id}")
    print(f"Location: {session_data['location']['city']}, {session_data['location']['country']}")
    print(f"Device ID: {session_data['device_id']}")
    
    # Show analytics
    analytics = manager.get_analytics_summary()
    print(f"\nAnalytics: {analytics}")