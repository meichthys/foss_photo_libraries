#!/usr/bin/env python3
"""
Tests for generate_table.py
"""

import unittest
from generate_table import score_to_emoji


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


if __name__ == '__main__':
    unittest.main()
