#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os
import mimetypes

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 为HTML文件添加UTF-8编码
        if self.path.endswith('.html') or self.path == '/':
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        # 为JSON文件添加UTF-8编码
        elif self.path.endswith('.json'):
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        # 为CSS文件添加UTF-8编码
        elif self.path.endswith('.css'):
            self.send_header('Content-Type', 'text/css; charset=utf-8')
        # 为JS文件添加UTF-8编码
        elif self.path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
        
        super().end_headers()

    def guess_type(self, path):
        """重写MIME类型猜测，确保正确处理UTF-8"""
        base, ext = os.path.splitext(path)
        if ext == '.html':
            return 'text/html; charset=utf-8'
        elif ext == '.json':
            return 'application/json; charset=utf-8'
        elif ext == '.css':
            return 'text/css; charset=utf-8'
        elif ext == '.js':
            return 'application/javascript; charset=utf-8'
        else:
            return super().guess_type(path)

if __name__ == "__main__":
    PORT = 8080
    
    # 确保端口没有被占用
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"服务器启动在端口 {PORT}")
            print(f"访问地址: http://localhost:{PORT}")
            print("按 Ctrl+C 停止服务器")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"端口 {PORT} 已被占用，请先停止其他服务器")
        else:
            print(f"启动服务器时出错: {e}")
    except KeyboardInterrupt:
        print("\n服务器已停止") 