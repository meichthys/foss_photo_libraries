# Table Generation System

This system allows you to regenerate the README.md comparison table from structured JSON data.

## Files

- **`projects.json`**: Contains all project data and feature definitions
- **`readme.tpl`**: Template file for the README (contains static content and `{{COMPARISON_TABLE}}` placeholder)
- **`generate_table.py`**: Python script that generates the table from JSON and inserts it into the template
- **`readme.md`**: Generated output file (the main README)

## Usage

To regenerate the README.md file:

```bash
python3 generate_table.py
```

## Project Data Structure

The `projects.json` file contains two main sections:

### 1. Projects Array

Each project has the following fields:

```json
{
  "name": "ProjectName",
  "github_url": "https://github.com/owner/repo",
  "logo_url": "https://...",
  "logo_alt": "Project Logo",
  "github_stars_repo": "owner/repo",
  "contributors_repo": "owner/repo",
  "last_commit_repo": "owner/repo",
  "last_commit_branch": "main",
  "license_repo": "owner/repo",
  "license_custom": "GPL-3.0",  // Optional: use instead of badge
  "demo_url": "https://demo.example.com/",
  "demo_title": "User:demo Pass:demo1234",  // Optional tooltip
  "demo_rating": "8️⃣"
}
```

### 2. Features Array

Features to include in the comparison (currently only first 10 rows are implemented):

```json
{
  "name": "Feature Name",
  "link": "features.md#feature-anchor"
}
```

## Current Implementation

The script currently generates the following rows (lines 18-50 of the original table):

1. **Logo** - Project logos as images
2. **Github Stars** - Star count badges
3. **Contributors** - Contributor count badges
4. **Last Commit** - Last commit date badges
5. **Source Language** - Primary programming language
6. **License** - License type badges
7. **Demo** - Demo links with ratings
8. **Freeness** - (Not yet implemented in generator)
9. **Automatic Mobile Upload** - (Not yet implemented in generator)
10. **Web App** - (Not yet implemented in generator)

## Adding More Features

To add support for additional feature rows:

1. Add feature data to each project in `projects.json`
2. Create a new function in `generate_table.py`:

```python
def generate_feature_row(projects):
    """Generate your feature row."""
    row = "| [Feature Name](features.md#anchor) "
    
    for project in projects:
        # Get data from project dict
        value = project.get('feature_key', '❌')
        row += f"| {value} "
    
    row += "|\n"
    return row
```

3. Add the function call to `generate_comparison_table()`:

```python
table += generate_feature_row(projects)
```

## Template Customization

Edit `readme.tpl` to change the static content around the table. The placeholder `{{COMPARISON_TABLE}}` will be replaced with the generated table.

