import json
import os

INDEX_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>表结构索引</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.min.js"></script>
    <style>
        body { padding: 2rem; }
        .table-hover tbody tr:hover { background: #f5f5f5; }
        .modal-dialog { max-width: 900px; }
        .field-table th, .field-table td { font-size: 0.95rem; }
        mark { background: #ffe066; color: #d35400; padding: 0 2px; border-radius: 2px; }
    </style>
</head>
<body>
    <h1>表结构索引</h1>
    <div class="mb-3">
        <input id="searchInput" type="text" class="form-control" placeholder="搜索表名、中文名、字段名、类型、说明...">
    </div>
    <table class="table table-bordered table-hover" id="tableList">
        <thead class="table-light">
            <tr>
                <th>表名</th>
                <th>中文名</th>
                <th>数据库</th>
                <th>字段数</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody id="tableBody">
        </tbody>
    </table>

    <!-- Modal -->
    <div class="modal fade" id="detailModal" tabindex="-1" aria-labelledby="detailModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="detailModalLabel">表详情</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" id="modalBody">
          </div>
        </div>
      </div>
    </div>

    <script>
    let tables = [];
    let lastQuery = '';
    fetch('all_tables.json')
      .then(res => res.json())
      .then(data => {
        tables = data;
        renderTable(tables, '');
        window.fuse = new Fuse(tables, {
          keys: [
            'table_name',
            'table_comment',
            'fields.name',
            'fields.comment',
            'fields.type',
            'fields.description'
          ],
          threshold: 0.3,
          minMatchCharLength: 1
        });
      });

    function highlight(text, query) {
      if (!query) return text;
      // 支持多关键词高亮
      let q = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      let re = new RegExp(q, 'gi');
      return text.replace(re, match => `<mark>${match}</mark>`);
    }

    function renderTable(data, query) {
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';
      data.forEach((t, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${highlight(t.table_name || '', query)}</td>
          <td>${highlight(t.table_comment || '', query)}</td>
          <td>${highlight(t.db_name || '', query)}</td>
          <td>${t.fields ? t.fields.length : 0}</td>
          <td><button class="btn btn-sm btn-primary" onclick="showDetail(${idx}, '${encodeURIComponent(query)}')">详情</button></td>
        `;
        tbody.appendChild(tr);
      });
    }

    document.getElementById('searchInput').addEventListener('input', function(e) {
      const q = e.target.value.trim();
      lastQuery = q;
      if (!q) {
        renderTable(tables, '');
      } else {
        const result = window.fuse.search(q).map(r => r.item);
        renderTable(result, q);
      }
    });

    window.showDetail = function(idx, query) {
      query = decodeURIComponent(query || lastQuery || '');
      const t = tables[idx];
      let html = `<div><b>表名：</b>${highlight(t.table_name || '', query)} &nbsp; <b>中文名：</b>${highlight(t.table_comment || '', query)}</div>`;
      html += `<div><b>数据库：</b>${highlight(t.db_name || '', query)} &nbsp; <b>模块：</b>${highlight(t.module || '', query)}</div>`;
      html += `<div><b>描述：</b>${highlight(t.description || '', query)}</div>`;
      html += `<hr/><h6>字段详细信息</h6>`;
      html += `<div style="max-height:400px;overflow:auto;"><table class="table table-striped field-table"><thead><tr><th>字段名</th><th>中文名</th><th>类型</th><th>长度</th><th>可空</th><th>外键</th><th>自增</th><th>默认值</th><th>主键</th><th>外键信息</th><th>说明</th></tr></thead><tbody>`;
      if (t.fields && t.fields.length) {
        t.fields.forEach(f => {
          html += `<tr><td>${highlight(f.name || '', query)}</td><td>${highlight(f.comment || '', query)}</td><td>${highlight(f.type || '', query)}</td><td>${highlight(f.length || '', query)}</td><td>${highlight(f.nullable || '', query)}</td><td>${highlight(f.is_foreign_key || '', query)}</td><td>${highlight(f.is_auto_increment || '', query)}</td><td>${highlight(f.default || '', query)}</td><td>${highlight(f.is_primary_key || '', query)}</td><td>${highlight(f.foreign_key_info || '', query)}</td><td>${highlight(f.description || '', query)}</td></tr>`;
        });
      } else {
        html += '<tr><td colspan="11">无字段信息</td></tr>';
      }
      html += '</tbody></table></div>';
      document.getElementById('modalBody').innerHTML = html;
      var modal = new bootstrap.Modal(document.getElementById('detailModal'));
      modal.show();
    }
    </script>
</body>
</html>
"""

def main():
    if not os.path.exists('all_tables.json'):
        print('all_tables.json 不存在，请先运行解析脚本！')
        return
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    print('已生成 index.html，可直接本地打开或部署到静态服务器。')

if __name__ == '__main__':
    main() 