#!/usr/bin/env python3
"""
清理 archetype-metadata.xml，移除不需要的目录（.github, .idea 等）

使用方法:
    python3 .github/scripts/clean-archetype-metadata.py <metadata-file-path>

参数:
    metadata-file-path: archetype-metadata.xml 文件路径
"""
import xml.etree.ElementTree as ET
import sys
import os

# 需要排除的目录列表
EXCLUDED_DIRECTORIES = ['.github', '.idea', '.vscode', '.settings', 'target']


def clean_archetype_metadata(metadata_file):
    """清理 archetype-metadata.xml，移除不需要的目录"""
    if not os.path.exists(metadata_file):
        print(f"Error: {metadata_file} not found")
        sys.exit(1)
    
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    
    # 定义命名空间
    ns = '{https://maven.apache.org/plugins/maven-archetype-plugin/archetype-descriptor/1.2.0}'
    
    # 查找所有 fileSets
    file_sets = root.findall(f'{ns}fileSets/{ns}fileSet')
    
    # 需要删除的 fileSet
    to_remove = []
    
    for file_set in file_sets:
        directory = file_set.find(f'{ns}directory')
        if directory is not None:
            dir_path = directory.text
            # 检查是否是需要排除的目录
            for excluded_dir in EXCLUDED_DIRECTORIES:
                if dir_path.startswith(excluded_dir) or dir_path == excluded_dir:
                    to_remove.append(file_set)
                    print(f"Removing fileSet for directory: {dir_path}")
                    break
    
    # 删除不需要的 fileSet
    file_sets_parent = root.find(f'{ns}fileSets')
    if file_sets_parent is not None:
        for file_set in to_remove:
            file_sets_parent.remove(file_set)
    
    # 保存更新后的文件
    tree.write(metadata_file, encoding='utf-8', xml_declaration=True)
    print(f"Successfully cleaned {metadata_file}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 .github/scripts/clean-archetype-metadata.py <metadata-file-path>")
        sys.exit(1)
    
    metadata_file = sys.argv[1]
    clean_archetype_metadata(metadata_file)

