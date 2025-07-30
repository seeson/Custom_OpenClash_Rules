# 文件路径
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

def generate_Xfile():
    """
    读取输入 ini，处理 custom_proxy_group 行：
    1. 如果行仅为某一 simple_region，则删除整行；
    2. 否则，移除 regions 列表中的字段，并合并多余的反引号；
    并写入输出文件。
    """
    if not os.path.isfile(file1_path):
        print(f"Error: Input file '{file1_path}' does not exist.")
        sys.exit(1)

    with open(file1_path, 'r', encoding='utf-8') as fin, \
         open(file2_path, 'w', encoding='utf-8') as fout:
        for line in fin:
            if line.startswith('custom_proxy_group='):
                # Check for full-line simple region matches
                skip = False
                for simple in simple_regions:
                    if f"custom_proxy_group={simple}`" in line:
                        skip = True
                        break
                if skip:
                    continue
                # Otherwise, remove detailed segments
                for segment in regions:
                    line = line.replace(segment, '')
                # Collapse multiple backticks into one
                while '``' in line:
                    line = line.replace('``', '`')
            fout.write(line)


if __name__ == "__main__":
    generate_Xfile()
    print(f"File '{file2_path}' has been updated based on '{file1_path}'")
