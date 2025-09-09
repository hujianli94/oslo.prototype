#!/bin/bash
# -*- coding: utf-8 -*-
# @Project Name : oslo.$1
# @Author       : hjl
# @Time         : 2025/9/6 21:37
# @File         : generate.sh
# @Software     : PyCharm
# @Description  : scripts function describe

if [ $# -ne 2 ]; then
  echo "⚠️ Error: Invalid arguments."
  echo "Usage: $0 <old_project_name> <project_name>"
  exit 1
fi

PROJECT_ROOT="."
old_project_name=$1
project_name=$2

find . -type f -name "*.pyc" -exec rm -f {} \;
find . -type d -name "__pycache__" -exec rm -rf {} \;

function convert_project_dir_name() {
    local old_project_name=$1
    local project_name=$2
    find "${PROJECT_ROOT}" -depth -type d -a -not -path "./.git/*" \
    -a -not -path "./.idea/*" \
    -a -not -path "./venv/*" \
    -a -not -path "./.vscode/*" \
    -name "*${old_project_name}*" -print0  | while IFS= read -r -d '' dir; do
        dir_name=$(basename "${dir}")
        new_dir_name="${dir_name//${old_project_name}/${project_name}}"

        if [ "${dir_name}" = "${new_dir_name}" ]; then
            continue
        fi

        new_dir_path="${dir%/${dir_name}}/${new_dir_name}"
        if [ -e "${new_dir_path}" ]; then
            continue
        fi

        echo " 🔄 重命名目录：${dir} → ${new_dir_path}"
        if ! mv -v "${dir}" "${new_dir_path}"; then
            echo "❌ 重命名失败：${dir} → ${new_dir_path}"
        fi
    done

}

function convert_project_file_name() {
    local old_project_name=$1
    local project_name=$2
    find "${PROJECT_ROOT}" -depth -type f  \
    -a -not -path "./.git/*" \
    -a -not -path "./.idea/*" \
    -a -not -path "./venv/*" \
    -a -not -path "./.vscode/*" \
    -type f -name "*${old_project_name}*" | while read -r file; do
    new_file="${file//${old_project_name}/${project_name}}"
    echo " 🔄 重命名文件：${file} → ${new_file}"
    mv -v "$file" "$new_file"
done
}

# 替换项目目录下所有文件内容
function convert_project_file_content() {
    local old_project_name=$1
    local project_name=$2

    # 将首字母转换为大写
    local old_project_name_capitalized=$(echo "${old_project_name:0:1}" | tr '[:lower:]' '[:upper:]')${old_project_name:1}
    local project_name_capitalized=$(echo "${project_name:0:1}" | tr '[:lower:]' '[:upper:]')${project_name:1}

    # 将字符串转换为全大写
    local old_project_name_upper=$(echo "${old_project_name}" | tr '[:lower:]' '[:upper:]')
    local project_name_upper=$(echo "${project_name}" | tr '[:lower:]' '[:upper:]')

    # 替换普通字符串
    # grep -Erl "*${old_project_name}*" --exclude-dir={.git,.idea} .
    if grep -Erq "*${old_project_name}*" --exclude-dir={.git,.idea} .; then
        echo " 🔄 替换文件内容：${old_project_name} → ${project_name}"
        grep -Erl "*${old_project_name}*" --exclude-dir={.git,.idea}  . | xargs -n 1 -t sed -i "s/${old_project_name}/${project_name}/g"
    else
        echo "⚠️ Error: No files containing the old project name found."
    fi

    # 替换首字母大写的字符串
    if grep -Erq "${old_project_name_capitalized}" --exclude-dir={.git,.idea} .; then
        echo " 🔄 替换文件内容：${old_project_name_capitalized} → ${project_name_capitalized}"
        grep -Erl "${old_project_name_capitalized}" --exclude-dir={.git,.idea} . | xargs -n 1 -t sed -i "s/${old_project_name_capitalized}/${project_name_capitalized}/g"
    else
        echo "⚠️ No files were found that contained the old project name with the initial capitalized: ${old_project_name_capitalized}"
    fi

    # 替换全大写的字符串
    if grep -Erq "${old_project_name_upper}" --exclude-dir={.git,.idea} .; then
        echo " 🔄 替换文件内容：${old_project_name_upper} → ${project_name_upper}"
        grep -Erl "${old_project_name_upper}" --exclude-dir={.git,.idea} . | xargs -n 1 -t sed -i "s/${old_project_name_upper}/${project_name_upper}/g"
    else
        echo "⚠️ 未找到包含全大写旧项目名的文件: ${old_project_name_upper}"
    fi
}

function main() {
    convert_project_dir_name $old_project_name $project_name
    sleep 1
    convert_project_file_name $old_project_name $project_name
    sleep 1
    convert_project_file_content $old_project_name $project_name
}

main $*