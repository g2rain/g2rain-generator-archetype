#!/usr/bin/env python3
"""
更新生成的 archetype pom.xml，添加发布到 Maven Central 所需的配置。

使用方法:
    python3 .github/scripts/update-archetype-pom.py <archetype-pom-path> <fragment-path>

参数:
    archetype-pom-path: 生成的 archetype pom.xml 路径
    fragment-path: 配置片段文件路径 (.github/workflows/archetype-release-pom-fragment.xml)
"""
import xml.etree.ElementTree as ET
import sys
import os


def merge_fragment_to_pom(pom_file, fragment_file):
    """将配置片段合并到 pom.xml"""
    if not os.path.exists(pom_file):
        print(f"Error: {pom_file} not found")
        sys.exit(1)
    
    if not os.path.exists(fragment_file):
        print(f"Error: {fragment_file} not found")
        sys.exit(1)
    
    # 解析 pom.xml
    tree = ET.parse(pom_file)
    root = tree.getroot()
    ET.register_namespace('', 'http://maven.apache.org/POM/4.0.0')
    ns = '{http://maven.apache.org/POM/4.0.0}'
    
    # 解析 fragment
    fragment_tree = ET.parse(fragment_file)
    fragment_root = fragment_tree.getroot()
    
    # 如果根元素是 <fragment>，则使用其子元素
    if fragment_root.tag == 'fragment':
        # 创建一个临时根元素来包含所有子元素
        temp_root = ET.Element('temp')
        for child in fragment_root:
            temp_root.append(child)
        fragment_root = temp_root
    
    # 更新 name
    name_frag = fragment_root.find('name')
    if name_frag is not None:
        name_elem = root.find(f'{ns}name')
        if name_elem is not None:
            name_elem.text = name_frag.text
        else:
            # 插入到 description 之前
            desc = root.find(f'{ns}description')
            if desc is not None:
                idx = list(root).index(desc)
                root.insert(idx, ET.Element('name'))
                root[idx].text = name_frag.text
    
    # 更新 description
    desc_frag = fragment_root.find('description')
    if desc_frag is not None:
        desc_elem = root.find(f'{ns}description')
        if desc_elem is not None:
            desc_elem.text = desc_frag.text
    
    # 更新 URL
    url_frag = fragment_root.find('url')
    if url_frag is not None:
        url_elem = root.find(f'{ns}url')
        if url_elem is not None:
            url_elem.text = url_frag.text
        else:
            # 插入到 description 之后
            desc = root.find(f'{ns}description')
            if desc is not None:
                idx = list(root).index(desc) + 1
                root.insert(idx, ET.Element('url'))
                root[idx].text = url_frag.text
    
    def copy_element_with_ns(source, target_parent, insert_after=None):
        """复制元素并确保命名空间正确"""
        # 创建新元素，使用正确的命名空间
        new_elem = ET.Element(source.tag if source.tag.startswith('{') else f'{ns}{source.tag}')
        new_elem.text = source.text
        new_elem.tail = source.tail
        # 复制属性
        for key, value in source.attrib.items():
            new_elem.set(key, value)
        # 递归复制子元素
        for child in source:
            copy_element_with_ns(child, new_elem)
        # 插入到目标位置
        if insert_after is not None:
            idx = list(target_parent).index(insert_after) + 1
            target_parent.insert(idx, new_elem)
        else:
            target_parent.append(new_elem)
        return new_elem
    
    # 更新或添加 SCM
    scm_frag = fragment_root.find('scm')
    if scm_frag is not None:
        scm_elem = root.find(f'{ns}scm')
        if scm_elem is not None:
            root.remove(scm_elem)
        # 添加新的 SCM（在 URL 之后）
        url = root.find(f'{ns}url')
        if url is not None:
            copy_element_with_ns(scm_frag, root, url)
    
    # 更新或添加 developers
    developers_frag = fragment_root.find('developers')
    if developers_frag is not None:
        developers_elem = root.find(f'{ns}developers')
        if developers_elem is not None:
            root.remove(developers_elem)
        # 添加新的 developers（在 SCM 之后）
        scm = root.find(f'{ns}scm')
        if scm is not None:
            copy_element_with_ns(developers_frag, root, scm)
    
    # 更新或添加 licenses
    licenses_frag = fragment_root.find('licenses')
    if licenses_frag is not None:
        licenses_elem = root.find(f'{ns}licenses')
        if licenses_elem is not None:
            root.remove(licenses_elem)
        # 添加新的 licenses（在 developers 之后）
        developers = root.find(f'{ns}developers')
        if developers is not None:
            copy_element_with_ns(licenses_frag, root, developers)
    
    # 添加 distributionManagement
    dist_mgmt_frag = fragment_root.find('distributionManagement')
    if dist_mgmt_frag is not None:
        dist_mgmt_elem = root.find(f'{ns}distributionManagement')
        if dist_mgmt_elem is not None:
            root.remove(dist_mgmt_elem)
        # 添加新的 distributionManagement（在 licenses 之后）
        licenses = root.find(f'{ns}licenses')
        if licenses is not None:
            copy_element_with_ns(dist_mgmt_frag, root, licenses)
    
    # 合并 properties
    props_frag = fragment_root.find('properties')
    if props_frag is not None:
        props_elem = root.find(f'{ns}properties')
        if props_elem is None:
            # 创建 properties（在 distributionManagement 之后）
            dist_mgmt = root.find(f'{ns}distributionManagement')
            if dist_mgmt is not None:
                idx = list(root).index(dist_mgmt) + 1
                # 使用 ET.Element 创建，然后插入，避免 ET.SubElement 自动添加
                props_elem = ET.Element(f'{ns}properties')
                root.insert(idx, props_elem)
            else:
                # 如果没有 distributionManagement，添加到末尾
                props_elem = ET.Element(f'{ns}properties')
                root.append(props_elem)
        
        # 合并属性
        for prop in props_frag:
            tag = prop.tag if prop.tag.startswith('{') else prop.tag
            existing = props_elem.find(f'{ns}{tag}')
            if existing is not None:
                existing.text = prop.text
            else:
                new_prop = ET.Element(f'{ns}{tag}')
                new_prop.text = prop.text
                props_elem.append(new_prop)
    
    # 合并 build/plugins
    build_frag = fragment_root.find('build')
    if build_frag is not None:
        plugins_frag = build_frag.find('plugins')
        if plugins_frag is not None:
            build_elem = root.find(f'{ns}build')
            if build_elem is None:
                build_elem = ET.SubElement(root, 'build')
            
            plugins_elem = build_elem.find(f'{ns}plugins')
            if plugins_elem is None:
                plugins_elem = ET.SubElement(build_elem, 'plugins')
            
            # 合并插件（避免重复）
            for plugin_frag in plugins_frag.findall('.//plugin'):
                gid_frag = plugin_frag.find('.//groupId') or plugin_frag.find(f'{ns}groupId')
                aid_frag = plugin_frag.find('.//artifactId') or plugin_frag.find(f'{ns}artifactId')
                if gid_frag is not None and aid_frag is not None:
                    # 检查是否已存在
                    found = False
                    for existing_plugin in plugins_elem.findall(f'{ns}plugin'):
                        gid_existing = existing_plugin.find(f'{ns}groupId')
                        aid_existing = existing_plugin.find(f'{ns}artifactId')
                        if (gid_existing is not None and aid_existing is not None and
                            gid_existing.text == gid_frag.text and aid_existing.text == aid_frag.text):
                            # 替换现有插件
                            plugins_elem.remove(existing_plugin)
                            copy_element_with_ns(plugin_frag, plugins_elem)
                            found = True
                            break
                    if not found:
                        copy_element_with_ns(plugin_frag, plugins_elem)
    
    # 添加 profiles
    profiles_frag = fragment_root.find('profiles')
    if profiles_frag is not None:
        profiles_elem = root.find(f'{ns}profiles')
        if profiles_elem is None:
            profiles_elem = ET.SubElement(root, 'profiles')
        
        # 检查 release profile 是否存在
        release_profile_frag = profiles_frag.find('.//profile') or profiles_frag.find(f'{ns}profile')
        if release_profile_frag is not None:
            pid_frag = release_profile_frag.find('.//id') or release_profile_frag.find(f'{ns}id')
            if pid_frag is not None and pid_frag.text == 'release':
                # 查找现有的 release profile
                found = False
                for existing_profile in profiles_elem.findall(f'{ns}profile'):
                    pid_existing = existing_profile.find(f'{ns}id')
                    if pid_existing is not None and pid_existing.text == 'release':
                        profiles_elem.remove(existing_profile)
                        copy_element_with_ns(release_profile_frag, profiles_elem)
                        found = True
                        break
                if not found:
                    copy_element_with_ns(release_profile_frag, profiles_elem)
    
    # 保存更新后的 pom.xml
    tree.write(pom_file, encoding='utf-8', xml_declaration=True)
    print(f"Successfully updated {pom_file}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 .github/scripts/update-archetype-pom.py <archetype-pom-path> <fragment-path>")
        sys.exit(1)
    
    pom_file = sys.argv[1]
    fragment_file = sys.argv[2]
    merge_fragment_to_pom(pom_file, fragment_file)

