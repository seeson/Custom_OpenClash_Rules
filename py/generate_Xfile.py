# 文件路径
file1_path = "cfg/Custom_Clash.ini"
file2_path = "cfg/Custom_Clash_X.ini"

import os
import sys
import re

# List of region keywords to remove from custom_proxy_group fields
def get_regions():
    return [
        "香港节点",
        "新加坡节点",
        "台湾节点",
        "韩国节点",
        "英国节点",
        "法国节点",
        "德国节点",
        "荷兰节点",
        "土耳其节点"
    ]

# Regex pattern template to remove a region field encapsulated by backticks
# Matches patterns like `[]🇸🇬 新加坡节点`
pattern_template = r"`\[\][^`]*{region}[^`]*`"


def generate_Xfile():
    """
    Read the input ini file, remove unwanted region fields from custom_proxy_group lines,
    and write the cleaned content to the output file.
    """
    # Ensure input file exists
    if not os.path.isfile(file1_path):
        print(f"Error: Input file '{file1_path}' does not exist.")
        sys.exit(1)

    regions = get_regions()

    with open(file1_path, "r", encoding="utf-8") as fin, \
         open(file2_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if line.startswith("custom_proxy_group="):
                # Remove each unwanted region field segment
                for region in regions:
                    pat = pattern_template.format(region=re.escape(region))
                    line = re.sub(pat, "", line)
                # Collapse multiple backticks into a single
                line = re.sub(r"`{2,}", "`", line)
            fout.write(line)


if __name__ == "__main__":
    generate_Xfile()
    print(f"File '{file2_path}' has been updated based on '{file1_path}'.")
