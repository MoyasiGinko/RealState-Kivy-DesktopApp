#!/usr/bin/env python3
"""
Fix MDChip components in the enhanced_search.py file
"""

import re

def fix_mdchip_components(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix syntax errors with missing line breaks
    content = content.replace('        )        ', '        )\n\n        ')
    content = content.replace('        ))        ', '        ))\n\n        ')
    content = content.replace('        )# ', '        )\n\n        # ')
    content = content.replace('        ))# ', '        ))\n\n        # ')

    # Fix MDChip components - type="choice" to type="filter"
    content = re.sub(r'type="choice"', r'type="filter"', content)

    # Fix MDChip components - replace text property with MDLabel
    pattern = r'(\s+)chip = MDChip\(\s+text=(\w+),\s+type="filter",\s+on_release=lambda x, (\w+)=\2: self\.toggle_filter_chip\(x, \'(\w+)\', \3\)\s+\)'
    replacement = r'\1chip = MDChip(\n\1    type="filter",\n\1    on_release=lambda x, \3=\2: self.toggle_filter_chip(x, \'\4\', \3)\n\1)\n\1chip.add_widget(MDLabel(\n\1    text=\2,\n\1    halign="center",\n\1    adaptive_size=True\n\1))'

    content = re.sub(pattern, replacement, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_mdchip_components('app/views/enhanced_search.py')
