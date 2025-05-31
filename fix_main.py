#!/usr/bin/env python3
"""
Fix indentation issues in main.py
"""

def fix_main_py():
    source_file = 'main_fixed.py'
    target_file = 'main.py'

    print(f"Copying content from {source_file} to {target_file}")

    try:
        with open(source_file, 'r', encoding='utf-8') as source:
            content = source.read()

        with open(target_file, 'w', encoding='utf-8') as target:
            target.write(content)

        print(f"Successfully updated {target_file}")
        return True
    except Exception as e:
        print(f"Error updating {target_file}: {e}")
        return False

if __name__ == "__main__":
    fix_main_py()
