# Configuration API

**System configuration management and user preferences.**

*Part of [ClaudeDirector API Reference](../API_REFERENCE.md)*

---

## 🛠️ **Configuration API**

### **Configuration Manager**
```python
# .claudedirector/lib/claudedirector/config/config_manager.py
class ConfigurationManager:
    """Manage ClaudeDirector configuration"""

    def __init__(self, config_path: str = ".claudedirector/config"):
        self.config_path = Path(config_path)
        self.config = self._load_configuration()

    def _load_configuration(self) -> dict:
        """Load configuration from files"""
        config = {}

        # Load base configuration
        base_config_file = self.config_path / "default_config.yaml"
        if base_config_file.exists():
            with open(base_config_file) as f:
                config.update(yaml.safe_load(f))

        # Load user configuration (overrides)
        user_config_file = self.config_path / "user_config.yaml"
        if user_config_file.exists():
            with open(user_config_file) as f:
                user_config = yaml.safe_load(f)
                config = self._merge_configs(config, user_config)

        return config

    def get(self, key: str, default=None):
        """Get configuration value with dot notation support"""
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value):
        """Set configuration value with dot notation support"""
        keys = key.split('.')
        config_section = self.config

        for k in keys[:-1]:
            if k not in config_section:
                config_section[k] = {}
            config_section = config_section[k]

        config_section[keys[-1]] = value

    def save_user_config(self):
        """Save user configuration to file"""
        user_config_file = self.config_path / "user_config.yaml"
        with open(user_config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
```

---

**🎯 Complete API reference for extending ClaudeDirector's strategic AI architecture.**
