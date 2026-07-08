import re

# Define file paths
input_file_path = '48_Inc50.script'
output_file_path = '48_Inc50_ZeroECC.script'

# Regular expression pattern to catch ECC lines (e.g., ASC_074_01.ECC = 4.930039516175627e-16;)
ecc_pattern = re.compile(r'^(\s*\w+\.ECC\s*=\s*)[^;]+(;)')

modified_lines = []

with open(input_file_path, 'r') as file:
    for line in file:
        # Check if the line sets an ECC value
        if ecc_pattern.search(line):
            # Replace the value with 0
            line = ecc_pattern.sub(r'\g<1>0\2', line)
        modified_lines.append(line)

# Save the updated script to a new file
with open(output_file_path, 'w') as file:
    file.writelines(modified_lines)

print(f"Modification complete! Saved as: {output_file_path}")