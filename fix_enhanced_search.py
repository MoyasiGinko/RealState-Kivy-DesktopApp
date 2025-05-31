#!/usr/bin/env python3
"""
Fix enhanced_search.py file
"""

def fix_enhanced_search():
    import re

    target_file = 'app/views/enhanced_search.py'

    print(f"Fixing {target_file}")

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix indentation issues
        content = re.sub(r'for prop_type in property_types:            chip', 'for prop_type in property_types:\n            chip', content)
        content = re.sub(r'for status in statuses:\n            chip = MDChip\(\n\n                type="filter",\n\n                on_release=lambda x, s=status: self\.toggle_filter_chip\(x, \\\'status\\\', s\)\n\n            \)\n\n            chip\.add_widget\(MDLabel\(',
                       'for status in statuses:\n            chip = MDChip(\n                type="filter",\n                on_release=lambda x, s=status: self.toggle_filter_chip(x, \'status\', s)\n            )\n            chip.add_widget(MDLabel(\n                text=status,\n                halign="center",\n                adaptive_size=True\n            ))\n            self.status_chips_layout.add_widget(chip)', content)

        # Fix other formatting issues
        content = content.replace(')        ', ')\n\n        ')
        content = content.replace('        ))        ', '        ))\n\n        ')
        content = content.replace('        )# ', '        )\n\n        # ')

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Fixed {target_file}")
        return True
    except Exception as e:
        print(f"Error fixing {target_file}: {e}")
        return False

if __name__ == "__main__":
    fix_enhanced_search()
