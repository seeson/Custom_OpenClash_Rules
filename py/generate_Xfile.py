# File paths
file1_path = "cfg/Custom_Clash.ini"
file2_path = "cfg/Custom_Clash_X.ini"

import os
import sys

# List of detailed region contents (excluding leading backtick) to remove within lines
regions = [
    "[]🇭🇰 香港节点",
    "[]🇸🇬 新加坡节点",
    "[]🇼🇸 台湾节点",
    "[]🇰🇷 韩国节点",
    "[]🇬🇧 英国节点",
    "[]🇫🇷 法国节点",
    "[]🇩🇪 德国节点",
    "[]🇳🇱 荷兰节点",
    "[]🇹🇷 土耳其节点"
]

# List of simple region identifiers to match full-line deletes
simple_regions = [
    "🇭🇰 香港节点",
    "🇸🇬 新加坡节点",
    "🇼🇸 台湾节点",
    "🇰🇷 韩国节点",
    "🇬🇧 英国节点",
    "🇫🇷 法国节点",
    "🇩🇪 德国节点",
    "🇳🇱 荷兰节点",
    "🇹🇷 土耳其节点"
]

# Marker for the auto-select group line
AUTO_SELECT_PREFIX = "custom_proxy_group=♻️ 自动选择`url-test`"

def generate_Xfile():
    """
    Read the input ini and process 'custom_proxy_group' lines:
      1) If a line is exactly one of the simple region groups, drop the whole line;
      2) Otherwise, remove the segments in 'regions' (e.g., []🇭🇰 香港节点) and collapse duplicate backticks;
      3) Additionally, for the '♻️ 自动选择' group, change the regex field to '(🇺🇸|🇨🇦)'.
    Write the result to the output file.
    """
    if not os.path.isfile(file1_path):
        print(f"Error: Input file '{file1_path}' does not exist.")
        sys.exit(1)

    with open(file1_path, 'r', encoding='utf-8') as fin, \
         open(file2_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            if line.startswith('custom_proxy_group='):
                # 1) Drop whole line if it is a simple region group definition
                skip = False
                for simple in simple_regions:
                    if f"custom_proxy_group={simple}`" in line:
                        skip = True
                        break
                if skip:
                    continue

                # 3) If this is the auto-select group, rewrite the regex part only
                # Format example:
                # custom_proxy_group=♻️ 自动选择`url-test`.*`https://www.gstatic.com/generate_204`300,,50
                if AUTO_SELECT_PREFIX in line:
                    parts = line.rstrip('\n').split('`')
                    # parts indices: 0=name, 1=url-test, 2=REGEX, 3=URL, 4=params...
                    if len(parts) >= 3 and parts[1] == 'url-test':
                        parts[2] = '(🇺🇸|🇨🇦)'
                        line = '`'.join(parts) + '\n'

                # 2) Remove unwanted region segments inside the line
                for segment in regions:
                    line = line.replace(segment, '')

                # Collapse duplicate backticks caused by removals
                while '``' in line:
                    line = line.replace('``', '`')

            fout.write(line)

if __name__ == "__main__":
    generate_Xfile()
    print(f"File '{file2_path}' has been updated based on '{file1_path}'")
