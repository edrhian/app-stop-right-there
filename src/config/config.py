"""Implementation for configuration file management"""
import yaml

def load_config(path: str):
    """Load a YAML config file
    
    Args:
        path: Relative path of configuration file
    """

    with open(path, "r", encoding="UTF-8") as file:
        return yaml.safe_load(file)

def save_config(path: str, configuration):
    """Saves configuration
    
    Args:
        path: Relative path of configuration file
        configuration: the configuration python object, previously loaded with yaml_safe_load
    """
    with open(path, "w", encoding="UTF-8") as file:
        yaml.safe_dump(configuration, file)

if __name__ == "__main__":
    config = load_config(path="config/config.yaml")
    print(config['timer']['duration_seconds'])
    config['timer']['duration_seconds'] = 5
    save_config(path="config/config.yaml", configuration=config)
