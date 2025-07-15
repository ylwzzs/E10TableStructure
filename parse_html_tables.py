import os
import json
from bs4 import BeautifulSoup, Tag

# 1. 遍历当前目录下所有.html文件
def get_html_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.html')]

# 2. 解析单个HTML文件，提取表结构信息
def parse_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # 获取表名、中文名
    table_name = None
    table_comment = None
    db_name = None
    module = None
    description = None

    # 查找表名、中文名、数据库名、模块、描述
    for row in soup.find_all('tr'):
        if not isinstance(row, Tag):
            continue
        cells = row.find_all('td')
        if len(cells) >= 4:
            if '数据库表名' in cells[2].get_text():
                table_name = cells[3].get_text(strip=True)
            if len(cells) >= 7 and '中文名词' in cells[5].get_text():
                table_comment = cells[6].get_text(strip=True)
            if '所属数据库' in cells[2].get_text():
                db_name = cells[3].get_text(strip=True)
            if '所属模块' in cells[2].get_text():
                module = cells[3].get_text(strip=True)
            if len(cells) >= 7 and '描述' in cells[5].get_text():
                description = cells[6].get_text(strip=True)

    # 查找字段详细信息表
    fields = []
    detail_table = soup.find('table', class_='detail-table-content-table')
    if detail_table:
        for row in detail_table.find_all('tr'):
            if not isinstance(row, Tag):
                continue
            cols = row.find_all('td')
            # 跳过表头和隐藏行
            if len(cols) >= 13 and cols[1].get_text(strip=True).isdigit():
                field = {
                    'name': cols[2].get_text(strip=True),
                    'comment': cols[3].get_text(strip=True),
                    'type': cols[4].get_text(strip=True),
                    'length': cols[5].get_text(strip=True),
                    'nullable': '是' if 'checked' in str(cols[6]) else '否',
                    'is_foreign_key': '是' if 'checked' in str(cols[7]) else '否',
                    'is_auto_increment': '是' if 'checked' in str(cols[8]) else '否',
                    'default': cols[9].get_text(strip=True),
                    'is_primary_key': '是' if 'checked' in str(cols[10]) else '否',
                    'foreign_key_info': cols[11].get_text(strip=True),
                    'description': cols[12].get_text(strip=True),
                }
                fields.append(field)

    return {
        'file': os.path.basename(filepath),
        'table_name': table_name,
        'table_comment': table_comment,
        'db_name': db_name,
        'module': module,
        'description': description,
        'fields': fields
    }

if __name__ == '__main__':
    directory = '.'
    html_files = get_html_files(directory)
    all_tables = []
    for html_file in html_files:
        try:
            table_info = parse_html_file(os.path.join(directory, html_file))
            all_tables.append(table_info)
        except Exception as e:
            print(f'Error parsing {html_file}: {e}')
    # 输出为JSON
    with open('all_tables.json', 'w', encoding='utf-8') as f:
        json.dump(all_tables, f, ensure_ascii=False, indent=2)
    print(f'解析完成，共导出 {len(all_tables)} 个表结构到 all_tables.json') 