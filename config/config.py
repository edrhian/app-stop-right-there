import yaml

def load_config(path: str):
    """Load a YAML config file"""

    with open(path, "r", encoding="UTF-8") as file:
        return yaml.safe_load(file)
    
def save_config(path: str, config):
    """Saves configuration""" 
    with open(path, "w") as file:
        yaml.safe_dump(config, file)

if __name__ == "__main__":
    config = load_config(path="config/config.yaml")
    print(config['timer']['duration_seconds'])
    config['timer']['duration_seconds'] = 5
    save_config(path="config/config.yaml", config=config)
