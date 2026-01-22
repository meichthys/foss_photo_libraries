#!/usr/bin/env python3
"""
Tests for generate_table.py
"""

import unittest
import json
import tempfile
import os
from generate_table import (
    score_to_emoji,
    load_json,
    generate_table_header,
    generate_logo_row,
    generate_badge_row,
    generate_license_row,
    generate_default_row,
    generate_comparison_table,
    generate_readme
)


class TestScoreToEmoji(unittest.TestCase):
    """Test cases for the score_to_emoji function."""
    
    def test_x_returns_cross(self):
        """Test that 'x' returns a cross emoji."""
        self.assertEqual(score_to_emoji('x'), '❌')
        self.assertEqual(score_to_emoji('X'), '❌')  # Case insensitive
    
    def test_wip_with_number(self):
        """Test WIP (work in progress) with various numbers."""
        self.assertEqual(score_to_emoji('wip-0'), '🚧0️⃣')
        self.assertEqual(score_to_emoji('wip-1'), '🚧1️⃣')
        self.assertEqual(score_to_emoji('wip-2'), '🚧2️⃣')
        self.assertEqual(score_to_emoji('wip-3'), '🚧3️⃣')
        self.assertEqual(score_to_emoji('wip-4'), '🚧4️⃣')
        self.assertEqual(score_to_emoji('wip-5'), '🚧5️⃣')
        self.assertEqual(score_to_emoji('wip-6'), '🚧6️⃣')
        self.assertEqual(score_to_emoji('wip-7'), '🚧7️⃣')
        self.assertEqual(score_to_emoji('wip-8'), '🚧8️⃣')
        self.assertEqual(score_to_emoji('wip-9'), '🚧9️⃣')
        self.assertEqual(score_to_emoji('wip-10'), '🚧🔟')
    
    def test_wip_case_insensitive(self):
        """Test that WIP is case insensitive."""
        self.assertEqual(score_to_emoji('WIP-3'), '🚧3️⃣')
        self.assertEqual(score_to_emoji('Wip-3'), '🚧3️⃣')
    
    def test_plain_numbers_string(self):
        """Test plain number strings return green tick with emoji number."""
        self.assertEqual(score_to_emoji('0'), '✅0️⃣')
        self.assertEqual(score_to_emoji('1'), '✅1️⃣')
        self.assertEqual(score_to_emoji('2'), '✅2️⃣')
        self.assertEqual(score_to_emoji('3'), '✅3️⃣')
        self.assertEqual(score_to_emoji('4'), '✅4️⃣')
        self.assertEqual(score_to_emoji('5'), '✅5️⃣')
        self.assertEqual(score_to_emoji('6'), '✅6️⃣')
        self.assertEqual(score_to_emoji('7'), '✅7️⃣')
        self.assertEqual(score_to_emoji('8'), '✅8️⃣')
        self.assertEqual(score_to_emoji('9'), '✅9️⃣')
        self.assertEqual(score_to_emoji('10'), '✅🔟')
    
    def test_plain_numbers_int(self):
        """Test plain integer numbers return green tick with emoji number."""
        self.assertEqual(score_to_emoji(0), '✅0️⃣')
        self.assertEqual(score_to_emoji(1), '✅1️⃣')
        self.assertEqual(score_to_emoji(5), '✅5️⃣')
        self.assertEqual(score_to_emoji(8), '✅8️⃣')
        self.assertEqual(score_to_emoji(10), '✅🔟')
    
    def test_whitespace_handling(self):
        """Test that whitespace is properly stripped."""
        self.assertEqual(score_to_emoji(' x '), '❌')
        self.assertEqual(score_to_emoji(' 5 '), '✅5️⃣')
        self.assertEqual(score_to_emoji(' wip-3 '), '🚧3️⃣')
    
    def test_unmatched_patterns(self):
        """Test that unmatched patterns return the original string."""
        # These don't match any pattern, so return as-is
        self.assertEqual(score_to_emoji('unknown'), 'unknown')
        self.assertEqual(score_to_emoji('abc123'), 'abc123')
        self.assertEqual(score_to_emoji(''), '')
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Numbers outside 0-10 range
        self.assertEqual(score_to_emoji('11'), '✅11')
        self.assertEqual(score_to_emoji('99'), '✅99')
        self.assertEqual(score_to_emoji('-1'), '-1')  # Negative, not a digit
        
        # WIP with invalid numbers
        self.assertEqual(score_to_emoji('wip-11'), '🚧11')
        self.assertEqual(score_to_emoji('wip-99'), '🚧99')
    
    def test_special_ten(self):
        """Test that 10 gets the special keycap 10 emoji."""
        self.assertEqual(score_to_emoji('10'), '✅🔟')
        self.assertEqual(score_to_emoji(10), '✅🔟')
        self.assertEqual(score_to_emoji('wip-10'), '🚧🔟')


class TestLoadJson(unittest.TestCase):
    """Test cases for the load_json function."""
    
    def test_load_valid_json(self):
        """Test loading a valid JSON file."""
        # Create a temporary JSON file
        test_data = {
            "projects": [
                {"name": "Test", "repo": "test/repo"}
            ],
            "features": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            result = load_json(temp_file)
            self.assertEqual(result, test_data)
        finally:
            os.unlink(temp_file)
    
    def test_load_json_with_utf8(self):
        """Test loading JSON with UTF-8 characters."""
        test_data = {
            "projects": [{"name": "Test 中文", "emoji": "✅"}]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)
            temp_file = f.name
        
        try:
            result = load_json(temp_file)
            self.assertEqual(result["projects"][0]["name"], "Test 中文")
            self.assertEqual(result["projects"][0]["emoji"], "✅")
        finally:
            os.unlink(temp_file)


class TestGenerateTableHeader(unittest.TestCase):
    """Test cases for the generate_table_header function."""
    
    def test_header_with_single_project(self):
        """Test header generation with a single project."""
        projects = [
            {"name": "TestApp", "repo": "user/testapp"}
        ]
        
        result = generate_table_header(projects)
        
        self.assertIn("| Feature ", result)
        self.assertIn("| [TestApp](https://github.com/user/testapp)", result)
        self.assertIn("| :-------", result)
        self.assertTrue(result.endswith("|\n"))
    
    def test_header_with_multiple_projects(self):
        """Test header generation with multiple projects."""
        projects = [
            {"name": "App1", "repo": "user/app1"},
            {"name": "App2", "repo": "user/app2"},
            {"name": "App3", "repo": "user/app3"}
        ]
        
        result = generate_table_header(projects)
        
        self.assertIn("[App1](https://github.com/user/app1)", result)
        self.assertIn("[App2](https://github.com/user/app2)", result)
        self.assertIn("[App3](https://github.com/user/app3)", result)
        # Should have 2 lines (header + separator)
        self.assertEqual(result.count('\n'), 2)


class TestGenerateLogoRow(unittest.TestCase):
    """Test cases for the generate_logo_row function."""
    
    def test_logo_row_basic(self):
        """Test basic logo row generation."""
        projects = [
            {
                "name": "Test",
                "logo_url": "https://example.com/logo.png",
                "logo_alt": "Test Logo"
            }
        ]
        
        result = generate_logo_row(projects)
        
        self.assertIn("| Logo ", result)
        self.assertIn('<img src="https://example.com/logo.png"', result)
        self.assertIn('alt="Test Logo"', result)
        self.assertIn('style="width: 50px"', result)
    
    def test_logo_row_multiple_projects(self):
        """Test logo row with multiple projects."""
        projects = [
            {"name": "App1", "logo_url": "https://example.com/logo1.png", "logo_alt": "Logo 1"},
            {"name": "App2", "logo_url": "https://example.com/logo2.png", "logo_alt": "Logo 2"}
        ]
        
        result = generate_logo_row(projects)
        
        self.assertIn("logo1.png", result)
        self.assertIn("logo2.png", result)
        self.assertIn("Logo 1", result)
        self.assertIn("Logo 2", result)


class TestGenerateBadgeRow(unittest.TestCase):
    """Test cases for the generate_badge_row function."""
    
    def test_basic_badge_row(self):
        """Test basic badge row generation."""
        projects = [
            {"name": "Test", "repo": "user/test", "branch": "main"}
        ]
        
        result = generate_badge_row(
            "Stars",
            "features.md#stars",
            projects,
            "![?](https://img.shields.io/github/stars/{repo}?label=%20)"
        )
        
        self.assertIn("| [Stars](features.md#stars)", result)
        self.assertIn("github/stars/user/test", result)
    
    def test_badge_row_with_lowercase(self):
        """Test badge row with lowercase repo names."""
        projects = [
            {"name": "Test", "repo": "User/Test", "branch": "main"}
        ]
        
        result = generate_badge_row(
            "Contributors",
            "features.md#contrib",
            projects,
            "![?](https://img.shields.io/github/contributors/{repo}?label=%20)",
            use_lowercase=True
        )
        
        self.assertIn("user/test", result)
        self.assertNotIn("User/Test", result)
    
    def test_badge_row_with_branch(self):
        """Test badge row with branch in URL."""
        projects = [
            {"name": "Test", "repo": "user/test", "branch": "develop"}
        ]
        
        result = generate_badge_row(
            "Last Commit",
            "features.md#last-commit",
            projects,
            "![?](https://img.shields.io/github/last-commit/{repo}/{branch}?label=%20)",
            use_branch=True
        )
        
        self.assertIn("last-commit/user/test/develop", result)
    
    def test_badge_row_defaults_to_master_branch(self):
        """Test that missing branch defaults to master."""
        projects = [
            {"name": "Test", "repo": "user/test"}  # No branch specified
        ]
        
        result = generate_badge_row(
            "Last Commit",
            "features.md#last-commit",
            projects,
            "![?](https://img.shields.io/github/last-commit/{repo}/{branch}?label=%20)",
            use_branch=True
        )
        
        self.assertIn("last-commit/user/test/master", result)


class TestGenerateLicenseRow(unittest.TestCase):
    """Test cases for the generate_license_row function."""
    
    def test_standard_license(self):
        """Test license row with standard GitHub license badge."""
        projects = [
            {"name": "Test", "repo": "user/test"}
        ]
        
        result = generate_license_row(projects)
        
        self.assertIn("| [License](features.md#license)", result)
        self.assertIn("github/license/user/test", result)
    
    def test_custom_license(self):
        """Test license row with custom license."""
        projects = [
            {"name": "Test", "repo": "user/test", "license_custom": "GPL-3.0"}
        ]
        
        result = generate_license_row(projects)
        
        self.assertIn("static/v1", result)
        self.assertIn("message=GPL-3.0", result)
        self.assertIn("color=orange", result)
    
    def test_mixed_licenses(self):
        """Test license row with mix of standard and custom licenses."""
        projects = [
            {"name": "App1", "repo": "user/app1"},
            {"name": "App2", "repo": "user/app2", "license_custom": "MIT"}
        ]
        
        result = generate_license_row(projects)
        
        self.assertIn("github/license/user/app1", result)
        self.assertIn("message=MIT", result)


class TestGenerateDefaultRow(unittest.TestCase):
    """Test cases for the generate_default_row function."""
    
    def test_default_row_with_values(self):
        """Test default row with numeric values."""
        feature = {
            "name": "Web App",
            "link": "features.md#web-app"
        }
        projects = [
            {"name": "App1", "web_app": "8"},
            {"name": "App2", "web_app": "x"},
            {"name": "App3", "web_app": "wip-3"}
        ]
        
        result = generate_default_row(feature, projects)
        
        self.assertIn("| [Web App](features.md#web-app)", result)
        self.assertIn("✅8️⃣", result)
        self.assertIn("❌", result)
        self.assertIn("🚧3️⃣", result)
    
    def test_default_row_with_missing_values(self):
        """Test default row when projects don't have the feature."""
        feature = {
            "name": "New Feature",
            "link": "features.md#new"
        }
        projects = [
            {"name": "App1"},  # Feature not present
            {"name": "App2", "new_feature": "5"}
        ]
        
        result = generate_default_row(feature, projects)
        
        # Should show ❌ for missing feature
        self.assertIn("❌", result)
        self.assertIn("✅5️⃣", result)
    
    def test_default_row_with_urls(self):
        """Test default row with URL links."""
        feature = {
            "name": "Android App",
            "link": "features.md#android"
        }
        projects = [
            {
                "name": "App1",
                "android_app": "8",
                "android_app_url": "https://github.com/user/app/releases"
            },
            {
                "name": "App2",
                "android_app": "x",
                "android_app_url": "https://github.com/user/app/issues/123"
            }
        ]
        
        result = generate_default_row(feature, projects)
        
        self.assertIn("[✅8️⃣](https://github.com/user/app/releases)", result)
        self.assertIn("[❌](https://github.com/user/app/issues/123)", result)
    
    def test_default_row_no_link(self):
        """Test default row without feature link."""
        feature = {
            "name": "Test Feature",
            "link": None
        }
        projects = [
            {"name": "App1", "test_feature": "5"}
        ]
        
        result = generate_default_row(feature, projects)
        
        self.assertIn("| Test Feature ", result)
        self.assertNotIn("[Test Feature]", result)
    
    def test_default_row_feature_name_conversion(self):
        """Test that feature names are properly converted to keys."""
        feature = {
            "name": "Object/Face Recognition",
            "link": "features.md#object-face"
        }
        projects = [
            {"name": "App1", "object_face_recognition": "9"}
        ]
        
        result = generate_default_row(feature, projects)
        
        self.assertIn("✅9️⃣", result)


class TestGenerateComparisonTable(unittest.TestCase):
    """Test cases for the generate_comparison_table function."""
    
    def test_comparison_table_structure(self):
        """Test that comparison table has proper structure."""
        data = {
            "projects": [
                {"name": "Test", "repo": "user/test", "branch": "main"}
            ],
            "features": [
                {
                    "name": "Test Feature",
                    "link": "features.md#test"
                }
            ]
        }
        
        result = generate_comparison_table(data)
        
        # Should have header
        self.assertIn("| Feature ", result)
        self.assertIn("| :-------", result)
        # Should have feature row
        self.assertIn("| [Test Feature](features.md#test)", result)
    
    def test_comparison_table_with_logo_processor(self):
        """Test table generation with logo processor."""
        data = {
            "projects": [
                {
                    "name": "Test",
                    "repo": "user/test",
                    "logo_url": "https://example.com/logo.png",
                    "logo_alt": "Logo"
                }
            ],
            "features": [
                {
                    "name": "Logo",
                    "link": None,
                    "processor": "generate_logo_row"
                }
            ]
        }
        
        result = generate_comparison_table(data)
        
        self.assertIn("| Logo ", result)
        self.assertIn('<img src="https://example.com/logo.png"', result)
    
    def test_comparison_table_with_badge_processor(self):
        """Test table generation with badge processor."""
        data = {
            "projects": [
                {"name": "Test", "repo": "user/test", "branch": "main"}
            ],
            "features": [
                {
                    "name": "Stars",
                    "link": "features.md#stars",
                    "processor": "generate_badge_row",
                    "badge_template": "![?](https://img.shields.io/github/stars/{repo}?label=%20)"
                }
            ]
        }
        
        result = generate_comparison_table(data)
        
        self.assertIn("github/stars/user/test", result)
    
    def test_comparison_table_with_license_processor(self):
        """Test table generation with license processor."""
        data = {
            "projects": [
                {"name": "Test", "repo": "user/test"}
            ],
            "features": [
                {
                    "name": "License",
                    "link": "features.md#license",
                    "processor": "generate_license_row"
                }
            ]
        }
        
        result = generate_comparison_table(data)
        
        self.assertIn("github/license/user/test", result)
    
    def test_comparison_table_with_default_processor(self):
        """Test table generation with default processor (no processor specified)."""
        data = {
            "projects": [
                {"name": "Test", "repo": "user/test", "web_app": "8"}
            ],
            "features": [
                {
                    "name": "Web App",
                    "link": "features.md#web-app"
                }
            ]
        }
        
        result = generate_comparison_table(data)
        
        self.assertIn("✅8️⃣", result)


class TestReadmeConsistency(unittest.TestCase):
    """Test that the current readme.md matches the generated output."""
    
    def test_readme_matches_generated_output(self):
        """Test that readme.md is up-to-date with projects.json and readme.tpl."""
        # Read the current readme.md
        with open('readme.md', 'r', encoding='utf-8') as f:
            current_readme = f.read()
        
        # Generate a new readme to a temporary file
        temp_output = tempfile.mktemp(suffix='.md')
        
        try:
            generate_readme('readme.tpl', temp_output, 'projects.json')
            
            # Read the generated readme
            with open(temp_output, 'r', encoding='utf-8') as f:
                generated_readme = f.read()
            
            # Compare them
            self.assertEqual(
                current_readme,
                generated_readme,
                "readme.md does not match generated output! "
                "Run 'python3 generate_table.py' to regenerate it."
            )
        finally:
            if os.path.exists(temp_output):
                os.unlink(temp_output)


class TestGenerateReadme(unittest.TestCase):
    """Test cases for the generate_readme function."""
    
    def test_generate_readme_creates_file(self):
        """Test that generate_readme creates output file."""
        # Create temporary files
        template_data = "# Test\n\n{{COMPARISON_TABLE}}\n\nEnd"
        json_data = {
            "projects": [
                {"name": "Test", "repo": "user/test", "branch": "main"}
            ],
            "features": []
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tpl', delete=False) as tf:
            tf.write(template_data)
            template_file = tf.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as jf:
            json.dump(json_data, jf)
            json_file = jf.name
        
        output_file = tempfile.mktemp(suffix='.md')
        
        try:
            generate_readme(template_file, output_file, json_file)
            
            # Check output file exists
            self.assertTrue(os.path.exists(output_file))
            
            # Check content
            with open(output_file, 'r') as f:
                content = f.read()
            
            self.assertIn("# Test", content)
            self.assertIn("End", content)
            self.assertNotIn("{{COMPARISON_TABLE}}", content)
            self.assertIn("| Feature ", content)
        finally:
            os.unlink(template_file)
            os.unlink(json_file)
            if os.path.exists(output_file):
                os.unlink(output_file)
    
    def test_generate_readme_replaces_placeholder(self):
        """Test that generate_readme replaces the placeholder correctly."""
        template_data = "Before\n{{COMPARISON_TABLE}}\nAfter"
        json_data = {
            "projects": [
                {"name": "Test", "repo": "user/test"}
            ],
            "features": [
                {"name": "Feature", "link": "features.md#f"}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tpl', delete=False) as tf:
            tf.write(template_data)
            template_file = tf.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as jf:
            json.dump(json_data, jf)
            json_file = jf.name
        
        output_file = tempfile.mktemp(suffix='.md')
        
        try:
            generate_readme(template_file, output_file, json_file)
            
            with open(output_file, 'r') as f:
                content = f.read()
            
            self.assertIn("Before", content)
            self.assertIn("After", content)
            # Placeholder should be replaced with table
            self.assertNotIn("{{COMPARISON_TABLE}}", content)
            # Should contain table elements
            self.assertIn("| Feature ", content)
            self.assertIn("| [Test](https://github.com/user/test)", content)
        finally:
            os.unlink(template_file)
            os.unlink(json_file)
            if os.path.exists(output_file):
                os.unlink(output_file)


if __name__ == '__main__':
    unittest.main()
