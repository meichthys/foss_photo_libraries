#!/usr/bin/env python3
"""
Generate README.md from template and JSON data.
This script reads projects.json and readme.tpl to create the comparison table.
"""

import json

def score_to_emoji(score):
    """
    Map score strings to their visual representation with emojis.
    
    Args:
        score: Can be a string like "x", "wip-3", "8", or an integer
    
    Returns:
        String with appropriate emoji representation
    
    Examples:
        "x" → "❌"
        "wip-3" → "🚧3️⃣"
        "8" or 8 → "✅8️⃣"
        "10" or 10 → "✅🔟"
    """
    # Convert to string for consistent handling
    score_str = str(score).strip().lower()
    
    # Map for emoji numbers 0-10
    emoji_numbers = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
        '10': '🔟'
    }
    
    # Handle "x" - Cross
    if score_str == 'x':
        return "❌"
    
    # Handle "wip-N" - Work in progress with number
    if score_str.startswith('wip-'):
        number = score_str.split('-')[1]
        emoji_num = emoji_numbers.get(number, number)
        return f"🚧{emoji_num}"
    
    # Handle plain numbers - Green tick with number
    if score_str.isdigit():
        emoji_num = emoji_numbers.get(score_str, score_str)
        return f"✅{emoji_num}"
    
    # Return as-is if no pattern matches
    return score_str


def load_json(filepath="projects.json"):
    """Load project data from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_table_header(projects):
    """Generate the table header with project names."""
    header = "| Feature "
    separator = "| :------- "
    
    for project in projects:
        name = project['name']
        repo = project['repo']
        url = f"https://github.com/{repo}"
        header += f"| [{name}]({url}) "
        separator += "| " + "-" * (len(url) + len(name) + 4) + " "
    
    header += "|\n"
    separator += "|\n"
    
    return header + separator


def generate_logo_row(projects):
    """Generate the logo row."""
    row = "| Logo "
    
    for project in projects:
        logo_url = project['logo_url']
        logo_alt = project['logo_alt']
        cell = f'<img src="{logo_url}" style="width: 50px"  alt="{logo_alt}"/>'
        row += f"| {cell} "
    
    row += "|\n"
    return row


def generate_badge_row(feature_name, feature_link, projects, badge_template, use_lowercase=False, use_branch=False):
    """
    Generic function to generate a row with badges.
    
    Args:
        feature_name: Name of the feature (e.g., "Github Stars")
        feature_link: Link for the feature header (e.g., "features.md#github-stars")
        projects: List of projects
        badge_template: Format string for the badge URL. Use {repo} and {branch} as placeholders
        use_lowercase: Whether to lowercase the repo name
        use_branch: Whether to include branch in the badge URL
    """
    row = f"| [{feature_name}]({feature_link}) "
    
    for project in projects:
        repo = project['repo'].lower() if use_lowercase else project['repo']
        
        if use_branch:
            branch = project.get('branch', 'master')
            badge = badge_template.format(repo=repo, branch=branch)
        else:
            badge = badge_template.format(repo=repo)
        
        row += f"| {badge} "
    
    row += "|\n"
    return row





def generate_license_row(projects):
    """Generate license row."""
    row = "| [License](features.md#license) "
    
    for project in projects:
        if 'license_custom' in project:
            # Custom license display
            custom = project['license_custom']
            badge = f"![?](https://img.shields.io/static/v1?label=%20&message={custom}&color=orange)"
        else:
            repo = project['repo']
            badge = f"![?](https://img.shields.io/github/license/{repo}?label=%20)"
        row += f"| {badge} "
    
    row += "|\n"
    return row


def generate_default_row(feature, projects):
    """
    Generate a default row for features without a custom processor.
    Uses score_to_emoji to convert values.
    Also checks for feature_key + '_url' to create links.
    """
    feature_name = feature['name']
    feature_link = feature.get('link')
    feature_key = feature_name.lower().replace(' ', '_').replace('/', '_')
    feature_url_key = feature_key + '_url'
    
    # Build row header
    if feature_link:
        row = f"| [{feature_name}]({feature_link}) "
    else:
        row = f"| {feature_name} "
    
    # Add cells for each project
    for project in projects:
        # Try to find the feature value in the project
        value = project.get(feature_key, '❌')
        
        # Convert value using score_to_emoji if it's a simple value
        if isinstance(value, (str, int)):
            cell = score_to_emoji(value)
        else:
            cell = value
        
        # Check if there's a URL field for this feature (even for X/❌ to link to reason/issue)
        if feature_url_key in project:
            url = project[feature_url_key]
            cell = f"[{cell}]({url})"
        
        row += f"| {cell} "
    
    row += "|\n"
    return row


def generate_comparison_table(data):
    """Generate the complete comparison table dynamically based on features."""
    projects = data['projects']
    features = data.get('features', [])
    
    # Generate header
    table = generate_table_header(projects)
    
    # Loop over features and generate each row
    for feature in features:
        processor_name = feature.get('processor')
        
        # Match processor name and call appropriate function
        match processor_name:
            case 'generate_logo_row':
                table += generate_logo_row(projects)
            
            case 'generate_badge_row':
                # Read badge configuration from feature
                feature_name = feature['name']
                feature_link = feature.get('link')
                badge_template = feature.get('badge_template', '')
                use_lowercase = feature.get('use_lowercase', False)
                use_branch = feature.get('use_branch', False)
                
                table += generate_badge_row(
                    feature_name,
                    feature_link,
                    projects,
                    badge_template,
                    use_lowercase=use_lowercase,
                    use_branch=use_branch
                )
            
            case 'generate_license_row':
                table += generate_license_row(projects)
            
            case _:
                # Use default conversion for unknown or null processors
                table += generate_default_row(feature, projects)
    
    return table


def generate_readme(template_file="readme.tpl", output_file="readme.md", json_file="projects.json"):
    """Generate README.md from template and JSON data."""
    # Load data
    data = load_json(json_file)
    
    # Read template
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate table
    table = generate_comparison_table(data)
    
    # Replace placeholder in template
    output = template.replace("{{COMPARISON_TABLE}}", table)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

if __name__ == "__main__":
    generate_readme()
