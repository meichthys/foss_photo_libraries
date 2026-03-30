# Contribution Guidelines

To contribute a project or feature, you should only need to make changes to `projects.json`.


## Steps

1. Make changes to `projects.json` (take note of the [project structure](##Project-Data-Structure))

2. Re-generate the README.md file:

  ```bash
  python3 generate_table.py
  ```

3. Run the test suite:

  ```bash
  python3 -m pytest test_generate_table.py -v
  ```

4. Submit your pull request


## Files

For more involved contributions a description of the main project files are:

- **`projects.json`**: Contains all projects and their features
- **`readme.tpl`**: Template file for the README (contains static content and `{{COMPARISON_TABLE}}` placeholder)
- **`generate_table.py`**: Python script that generates the table from JSON and validates its integrity
- **`readme.md`**: Generated output file (the main README)
- **`test_generate_table.py`**: Comprehensive test suite covering all functions and validation


## Project Data Structure

The `projects.json` file contains two main sections:

### 1. Projects Array

Each project requires these **mandatory fields**:
- `name`: Project name
- `repo`: GitHub repository (owner/repo format)
- `logo_url`: URL to project logo
- `logo_alt`: Alt text for logo

**Optional standard fields**:
- `branch`: Branch name (defaults to "master" for badges)
- `license_custom`: Custom license text (overrides GitHub badge)

**Feature fields**: Any feature defined in the features array can be added as:
- `feature_name`: Value indicating the quality of the feature on a scale of 1-10 ("x" means the feature doesn't exist, and prepending 'wip-' means feature is a work in process)
- `feature_name_url`: Optional URL to link to the project's documentation of the feature

Example:
```json
{
  "name": "ProjectName",
  "repo": "owner/repo",
  "branch": "main",
  "logo_url": "https://...",
  "logo_alt": "Project Logo",
  "license_custom": "GPL-3.0",
  "web_app": "8",
  "web_app_url": "https://demo.example.com",
  "ios_app": "x",
  "ios_app_url": "https://github.com/owner/repo/issues/123"
  ...
}
```

### 2. Features Array

Each feature defines a row in the comparison table:

```json
{
  "name": "Feature Name",
  "link": "features.md#feature-anchor",
  "processor": "generate_default_row",
  "description": "Feature description"
}
```

**Processor Types**:
- `generate_logo_row`: Special processor for logo display
- `generate_badge_row`: GitHub badge generation (requires badge_template, use_lowercase, use_branch)
- `generate_license_row`: License badge handling
- `generate_default_row` (or null): Score-based row with emoji conversion

### Score Value Conversion

The system automatically converts score values to an emoji representation:
- `"x"` → ❌ (not available)
- `"0"-"9"` → ✅0️⃣-✅9️⃣ (available with rating)
- `"10"` → ✅🔟 (perfect score - used sparingly)
- `"wip-1"` → 🚧1️⃣ (work in progress with rating of 1)

### Data Validation

The `validate_projects_json()` function ensures data integrity:

✅ **Required Fields Check**: Validates all projects have name, repo, logo_url, logo_alt
✅ **Unmapped Keys Detection**: Identifies project keys not mapped to any feature
✅ **Error Aggregation**: Collects all errors before reporting
✅ **Detailed Error Messages**: Shows which projects have which unmapped keys

Example validation output:
```
projects.json validation FAILED:
Project 'App1' is missing fields: {'repo'}
Found 2 project key(s) not mapped to any feature:
  • 'invalid_key_1' in: App1, App3
  • 'another_bad_key' in: App3
```

## Adding New Features

To add a new feature to the comparison table:

1. **Add feature definition to `projects.json`**:
```json
{
  "features": [
    {
      "name": "New Feature",
      "link": "features.md#new-feature",
      "description": "Description of the feature"
    }
  ]
}
```

2. **Add feature values to projects**:
```json
{
  "projects": [
    {
      "name": "ProjectName",
      "new_feature": "8",
      "new_feature_url": "https://example.com/feature"
    }
  ]
}
```

3. **Regenerate README**:
```bash
python3 generate_table.py
```

The system automatically converts feature names (e.g., "New Feature" → "new_feature") and handles score-to-emoji conversion.

### Custom Processors

For specialized row formatting, implement a custom processor in `generate_table.py`:

```python
def generate_custom_row(projects):
    """Generate a custom-formatted row."""
    row = "| [Feature Name](features.md#anchor) "

    for project in projects:
        value = project.get('feature_key', '❌')
        # Custom formatting logic here
        row += f"| {value} "

    row += "|\n"
    return row
```

Then reference it in the feature definition:
```json
{
  "name": "Custom Feature",
  "processor": "generate_custom_row"
}
```

## CI/CD Integration

The project includes GitHub Actions workflow (`.github/workflows/mega-linter.yml`) that:
- Runs MegaLinter for code quality
- Validates projects.json structure
- Runs all tests to ensure consistency
- Verifies readme.md matches generated output

## Template Customization

Edit `readme.tpl` to change the static content around the table. The placeholder `{{COMPARISON_TABLE}}` will be replaced with the generated table.

