"""
Configuration Management for Mobile Earthquake App
Handles persistent storage of application settings
"""

import json
import os
import threading
from datetime import datetime
import logging

class AppConfig:
    """Thread-safe configuration management"""
    
    def __init__(self, config_file="mobile_config.json"):
        self.config_file = config_file
        self.lock = threading.Lock()
        self.config = self._load_config()
    
    def _get_default_config(self):
        """Get default configuration values"""
        return {
            "retention_policy": {
                "metrics_retention_days": 90,
                "cleanup_frequency_percent": 1,
                "log_max_size_mb": 5,
                "log_backup_count": 10
            },
            "app_settings": {
                "default_feed_type": "all_hour",
                "default_view_type": "overview",
                "cache_ttl_seconds": 300,
                "admin_mode_enabled": True
            },
            "analytics": {
                "visitor_tracking_enabled": True,
                "performance_logging_enabled": True,
                "error_reporting_enabled": True
            },
            "metadata": {
                "config_version": "1.0",
                "created_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "app_version": "1.0.0"
            }
        }
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Merge with defaults for any missing keys
                default_config = self._get_default_config()
                merged_config = self._merge_configs(default_config, config)
                
                # Update last_updated if we merged new defaults
                if merged_config != config:
                    merged_config["metadata"]["last_updated"] = datetime.now().isoformat()
                    self._save_config(merged_config)
                
                return merged_config
            else:
                # Create new config file with defaults
                default_config = self._get_default_config()
                self._save_config(default_config)
                return default_config
                
        except Exception as e:
            logging.error(f"CONFIG_ERROR | Failed to load config: {e}")
            return self._get_default_config()
    
    def _merge_configs(self, default, current):
        """Recursively merge current config with defaults"""
        for key, value in default.items():
            if key not in current:
                current[key] = value
            elif isinstance(value, dict) and isinstance(current[key], dict):
                current[key] = self._merge_configs(value, current[key])
        return current
    
    def _save_config(self, config=None):
        """Save configuration to file"""
        try:
            config_to_save = config or self.config
            config_to_save["metadata"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"CONFIG_ERROR | Failed to save config: {e}")
    
    def get(self, path, default=None):
        """Get configuration value using dot notation (e.g., 'retention_policy.metrics_retention_days')"""
        with self.lock:
            try:
                keys = path.split('.')
                value = self.config
                
                for key in keys:
                    value = value[key]
                
                return value
            except (KeyError, TypeError):
                return default
    
    def set(self, path, value):
        """Set configuration value using dot notation"""
        with self.lock:
            try:
                keys = path.split('.')
                config_ref = self.config
                
                # Navigate to the parent of the target key
                for key in keys[:-1]:
                    if key not in config_ref:
                        config_ref[key] = {}
                    config_ref = config_ref[key]
                
                # Set the value
                config_ref[keys[-1]] = value
                
                # Save to file
                self._save_config()
                
                logging.info(f"CONFIG_UPDATE | {path} = {value}")
                return True
                
            except Exception as e:
                logging.error(f"CONFIG_ERROR | Failed to set {path} = {value}: {e}")
                return False
    
    def get_retention_config(self):
        """Get retention policy configuration"""
        with self.lock:
            return {
                "metrics_retention_days": self.get("retention_policy.metrics_retention_days", 90),
                "cleanup_frequency_percent": self.get("retention_policy.cleanup_frequency_percent", 1),
                "log_max_size_mb": self.get("retention_policy.log_max_size_mb", 5),
                "log_backup_count": self.get("retention_policy.log_backup_count", 10)
            }
    
    def update_retention_config(self, metrics_days=None, cleanup_frequency=None, log_size_mb=None, log_backup_count=None):
        """Update retention policy configuration"""
        with self.lock:
            try:
                if metrics_days is not None:
                    self.set("retention_policy.metrics_retention_days", metrics_days)
                
                if cleanup_frequency is not None:
                    self.set("retention_policy.cleanup_frequency_percent", cleanup_frequency)
                
                if log_size_mb is not None:
                    self.set("retention_policy.log_max_size_mb", log_size_mb)
                
                if log_backup_count is not None:
                    self.set("retention_policy.log_backup_count", log_backup_count)
                
                return True
                
            except Exception as e:
                logging.error(f"CONFIG_ERROR | Failed to update retention config: {e}")
                return False
    
    def get_app_settings(self):
        """Get application settings"""
        with self.lock:
            return {
                "default_feed_type": self.get("app_settings.default_feed_type", "all_hour"),
                "default_view_type": self.get("app_settings.default_view_type", "overview"),
                "cache_ttl_seconds": self.get("app_settings.cache_ttl_seconds", 300),
                "admin_mode_enabled": self.get("app_settings.admin_mode_enabled", True)
            }
    
    def export_config(self):
        """Export complete configuration as JSON string"""
        with self.lock:
            try:
                export_data = dict(self.config)
                export_data["export_metadata"] = {
                    "export_timestamp": datetime.now().isoformat(),
                    "export_type": "full_config"
                }
                return json.dumps(export_data, indent=2, ensure_ascii=False)
            except Exception as e:
                logging.error(f"CONFIG_ERROR | Failed to export config: {e}")
                return None
    
    def import_config(self, config_json):
        """Import configuration from JSON string"""
        with self.lock:
            try:
                imported_config = json.loads(config_json)
                
                # Remove export metadata if present
                if "export_metadata" in imported_config:
                    del imported_config["export_metadata"]
                
                # Merge with defaults to ensure all required keys exist
                default_config = self._get_default_config()
                merged_config = self._merge_configs(default_config, imported_config)
                
                # Update metadata
                merged_config["metadata"]["last_updated"] = datetime.now().isoformat()
                merged_config["metadata"]["import_date"] = datetime.now().isoformat()
                
                # Save and update current config
                self.config = merged_config
                self._save_config()
                
                logging.info("CONFIG_IMPORT | Configuration imported successfully")
                return True
                
            except Exception as e:
                logging.error(f"CONFIG_ERROR | Failed to import config: {e}")
                return False
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        with self.lock:
            try:
                default_config = self._get_default_config()
                default_config["metadata"]["reset_date"] = datetime.now().isoformat()
                
                self.config = default_config
                self._save_config()
                
                logging.info("CONFIG_RESET | Configuration reset to defaults")
                return True
                
            except Exception as e:
                logging.error(f"CONFIG_ERROR | Failed to reset config: {e}")
                return False
    
    def get_config_summary(self):
        """Get a summary of current configuration"""
        with self.lock:
            return {
                "config_file": self.config_file,
                "config_version": self.get("metadata.config_version", "unknown"),
                "app_version": self.get("metadata.app_version", "unknown"),
                "created_date": self.get("metadata.created_date", "unknown"),
                "last_updated": self.get("metadata.last_updated", "unknown"),
                "retention_days": self.get("retention_policy.metrics_retention_days", 90),
                "cleanup_frequency": self.get("retention_policy.cleanup_frequency_percent", 1),
                "file_exists": os.path.exists(self.config_file),
                "file_size": os.path.getsize(self.config_file) if os.path.exists(self.config_file) else 0
            }

# Global configuration instance
_config_instance = None

def get_app_config():
    """Get the global configuration instance (singleton pattern)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = AppConfig()
    return _config_instance

if __name__ == "__main__":
    # Test the configuration system
    config = get_app_config()
    
    print("📋 Configuration System Test")
    print("=" * 40)
    
    # Show current config
    summary = config.get_config_summary()
    print(f"Config file: {summary['config_file']}")
    print(f"File exists: {summary['file_exists']}")
    print(f"File size: {summary['file_size']} bytes")
    print(f"Version: {summary['config_version']}")
    print(f"Last updated: {summary['last_updated']}")
    
    # Show retention settings
    retention = config.get_retention_config()
    print(f"\nRetention Settings:")
    print(f"- Metrics retention: {retention['metrics_retention_days']} days")
    print(f"- Cleanup frequency: {retention['cleanup_frequency_percent']}%")
    print(f"- Log size limit: {retention['log_max_size_mb']} MB")
    print(f"- Log backup count: {retention['log_backup_count']} files")