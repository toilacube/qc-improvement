import pystache
import json
import os
from typing import Dict, List, Any, Optional

class PromptFactory:
    """
    A factory class that generates customizable prompts using external template files.
    Supports loading templates and configurations from files.
    """
    
    def __init__(self, 
                 template_path: Optional[str] = None, 
                 default_config_path: Optional[str] = None):
        """
        Initialize PromptFactory with optional template and default config paths.
        
        Args:
            template_path: Path to the mustache template file
            default_config_path: Path to the default configuration JSON file
        """
        # Set default paths if not provided
        self.template_path = template_path or os.path.join(
            os.path.dirname(__file__), 'default_template.mustache'
        )
        self.default_config_path = default_config_path or os.path.join(
            os.path.dirname(__file__), 'default_config.json'
        )
        
        # Load default template
        self.template = self._load_template(self.template_path)
        
        # Load default configuration
        self.default_values = self._load_default_config()
    
    def _load_template(self, path: str) -> str:
        """
        Load mustache template from a file.
        
        Args:
            path: Path to the mustache template file
        
        Returns:
            Template string
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback to a basic default template if file is not found
            return """
**Please act as an Expert.** Your task is to generate output based on the following requirements.

{{#core_objectives}}
- {{.}}
{{/core_objectives}}

{{#additional_sections}}
### **{{section_title}}**

{{section_content}}
{{/additional_sections}}
"""
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Load default configuration from a JSON file.
        
        Returns:
            Default configuration dictionary
        """
        try:
            with open(self.default_config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to hardcoded default configuration
            return {
                "core_objectives": [
                    "Generate test cases in a table format.",
                    "Align test cases with user stories.",
                    "Use standardized templates for clarity.",
                    "Include a Priority column."
                ],
                "additional_sections": []
            }
    
    def create_prompt(self, config: Optional[Dict[str, Any]] = None) -> str:
        """
        Creates a prompt based on the provided configuration.
        
        Args:
            config: Dictionary containing configuration options for the prompt
            
        Returns:
            Rendered prompt string
        """
        if config is None:
            config = {}
        
        # Merge default values with user-provided config
        merged_config = self.default_values.copy()
        
        # Update core objectives if provided
        if "core_objectives" in config:
            merged_config["core_objectives"] = config["core_objectives"]
        
        # Add or replace additional sections
        if "additional_sections" in config:
            merged_config["additional_sections"] = config["additional_sections"]
            
        # Render the template with the merged configuration
        return pystache.render(self.template, merged_config)
    
    def save_config(self, config: Dict[str, Any], filename: str) -> None:
        """
        Saves a configuration to a JSON file.
        
        Args:
            config: Configuration dictionary to save
            filename: Name of the file to save the configuration to
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def load_config(self, filename: str) -> Dict[str, Any]:
        """
        Loads a configuration from a JSON file.
        
        Args:
            filename: Name of the file to load the configuration from
            
        Returns:
            Configuration dictionary
        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

# Example files to demonstrate usage
def create_example_files():
    """
    Create example template and configuration files for demonstration.
    """
    # Example Mustache Template
    template_content = """
**Please act as an Expert QC (Quality Control) Engineer.** Your task is to generate structured test cases in a table format based on user stories and testing requirements.

---

### **1. Core Objectives**

{{#core_objectives}}
- {{.}}
{{/core_objectives}}

{{#additional_sections}}
### **{{section_title}}**

{{section_content}}
{{/additional_sections}}
"""

    # Example Default Configuration
    default_config = {
        "core_objectives": [
            "Generate test cases in a table format.",
            "Align test cases with user stories and ensure coverage across all testing types.",
            "Use standardized templates for clarity and consistency.",
            "Include a Priority column to categorize test cases."
        ],
        "additional_sections": []
    }

    # Ensure directory exists
    os.makedirs('config', exist_ok=True)

    # Write template file
    with open('config/default_template.mustache', 'w', encoding='utf-8') as f:
        f.write(template_content)

    # Write default config file
    with open('config/default_config.json', 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2)

# Example usage
if __name__ == "__main__":
    # Create example files first
    create_example_files()

    # Initialize PromptFactory with custom paths
    factory = PromptFactory(
        template_path='config/default_template.mustache',
        default_config_path='config/default_config.json'
    )
    
    # Generate default prompt
    default_prompt = factory.create_prompt()
    print("Default Prompt:\n", default_prompt)
    
    # Create a custom configuration
    custom_config = {
        "core_objectives": [
            "Generate comprehensive test cases with clear pass/fail criteria.",
            "Ensure complete traceability between requirements and test cases.",
            "Include edge cases and boundary testing scenarios."
        ],
        "additional_sections": [
            {
                "section_title": "2. Test Case Structure",
                "section_content": "- Test ID: Unique identifier for each test case\n- Description: Clear description of what is being tested\n- Preconditions: Required setup before test execution"
            }
        ]
    }
    
    # Generate custom prompt
    custom_prompt = factory.create_prompt(custom_config)
    print("\nCustom Prompt:\n", custom_prompt)