#!/usr/bin/env python3
"""
Fix indentation issues in mobile_earthquake_app.py
"""

def fix_indentation():
    with open('mobile_earthquake_app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the main function and the try block
    fixed_lines = []
    in_main_try = False
    try_indent_level = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Look for the main function try block
        if 'def main():' in line:
            fixed_lines.append(line)
            continue
            
        # Look for the main try block start
        if line.strip() == 'try:' and 'def main():' in ''.join(lines[max(0, i-10):i]):
            in_main_try = True
            try_indent_level = len(line) - len(line.lstrip())
            fixed_lines.append(line)
            continue
            
        # Look for the main except block
        if in_main_try and line.strip().startswith('except Exception as e:') and len(line) - len(line.lstrip()) == try_indent_level:
            in_main_try = False
            fixed_lines.append(line)
            continue
            
        # If we're in the main try block and the line is not properly indented
        if in_main_try:
            # Expected indentation is try_indent_level + 4
            expected_indent = try_indent_level + 4
            current_indent = len(line) - len(line.lstrip())
            
            # If line is not empty and not properly indented
            if line.strip() and current_indent < expected_indent:
                # Re-indent the line
                fixed_line = ' ' * expected_indent + line.lstrip()
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    # Write the fixed file
    with open('mobile_earthquake_app_fixed.py', 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("Fixed indentation saved to mobile_earthquake_app_fixed.py")

if __name__ == "__main__":
    fix_indentation()