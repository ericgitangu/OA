import os
import re

FILES = ["README.md", "dsa.md", "INDEX.md"]

def process_file(filepath):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r') as f:
        lines = f.read().splitlines()

    out_lines = []
    
    # Pass 1: Trailing spaces, horizontal rules, trailing punctuation in headings, lists
    for i, line in enumerate(lines):
        # Allow 2 spaces for hard breaks, otherwise strip all trailing whitespaces
        if line.endswith("  ") and not line.endswith("   "):
            pass
        else:
            line = line.rstrip(" \t")

        # MD035: Horizontal rule style
        if line == "----":
            line = "---"

        # MD026: Trailing punctuation in heading
        if line.startswith("# "):
            # We strip common punctuation at the end of headings
            match = re.search(r'^(#+\s+.*)([\.\:\!\?\;]+)$', line)
            if match:
                line = match.group(1).rstrip()
                
        # MD029: Ordered list item prefix
        # We enforce "1. " instead of "5. " or "9. "
        match = re.search(r'^(\s*)(\d+)\.\s+(.*)$', line)
        if match:
            # We replace it with 1.
            line = f"{match.group(1)}1. {match.group(3)}"

        out_lines.append(line)

    # Pass 2: Blank lines around headers and code fences
    # MD022: Headings surrounded by blank lines
    # MD031: Fences surrounded by blank lines
    in_code_block = False
    
    final_lines = []
    for i, line in enumerate(out_lines):
        is_fence = line.startswith("```")
        if is_fence:
            in_code_block = not in_code_block
            
        is_heading = line.startswith("#") and not in_code_block

        # Ensure blank line above
        if is_fence or is_heading:
            if final_lines and final_lines[-1].strip() != "":
                final_lines.append("")

        final_lines.append(line)

        # Ensure blank line below
        if is_fence or is_heading:
            # Don't add blank if it's EOF or the next line is already blank
            if i + 1 < len(out_lines) and out_lines[i+1].strip() != "":
                final_lines.append("")

    # Pass 3: Collapse multiple consecutive blank lines to 1
    collapsed = []
    for line in final_lines:
        if line.strip() == "":
            if collapsed and collapsed[-1].strip() == "":
                continue
        collapsed.append(line)
        
    # Write back, ensuring single trailing newline
    with open(filepath, 'w') as f:
        content = "\n".join(collapsed)
        f.write(content + "\n")

for f in FILES:
    process_file(f)
