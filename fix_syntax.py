#!/usr/bin/env python3
"""
Quick syntax fix script to resolve concatenated line issues
"""

import re
import os

def fix_concatenated_lines(file_path):
    """Fix common concatenated line patterns"""
    print(f"Fixing {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Common patterns to fix
    patterns = [
        (r'(\))(\s+)(def\s+)', r'\1\n\n    \3'),  # ) def -> )\n\n    def
        (r'(\))(\s+)(class\s+)', r'\1\n\n\3'),   # ) class -> )\n\nclass
        (r'(\w+)(\s+)(def\s+)', r'\1\n\n    \3'),  # word def -> word\n\n    def
        (r'(""".*?""")(\s+)(def\s+)', r'\1\n\n    \3'),  # docstring def
        (r'(""".*?""")(\s+)(class\s+)', r'\1\n\n\3'),   # docstring class
        (r'(True|False|None)(\s+)(def\s+)', r'\1\n\n    \3'),  # bool/None def
        (r'(\w+\(\))(\s+)(def\s+)', r'\1\n\n    \3'),  # function_call() def
    ]

    original_content = content

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file_path}")
        return True
    else:
        print(f"No fixes needed for {file_path}")
        return False

# Files to fix
files_to_fix = [
    'main.py',
    'app/views/enhanced_owners.py',
    'app/views/enhanced_properties.py',
    'app/views/enhanced_search.py'
]

if __name__ == "__main__":
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            fix_concatenated_lines(file_path)
        else:
            print(f"File not found: {file_path}")
