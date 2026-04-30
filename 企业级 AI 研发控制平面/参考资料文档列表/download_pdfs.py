#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量下载微信文章为PDF"""

import subprocess
import re
import time
import os

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR = "/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs"
MARKDOWN_FILE = "/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/微信文章链接列表.md"

# 从markdown中提取所有短格式微信文章链接
with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# 匹配 mp.weixin.qq.com/s/xxx 格式的短链接
pattern = r'https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+'
urls = re.findall(pattern, content)

# 去重保持顺序
seen = set()
unique_urls = []
for url in urls:
    if url not in seen:
        seen.add(url)
        unique_urls.append(url)

print(f"找到 {len(unique_urls)} 个有效链接")
print("=" * 50)

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

success = 0
failed = 0

for i, url in enumerate(unique_urls, 1):
    output_file = os.path.join(OUTPUT_DIR, f"{i:02d}.pdf")
    
    # 如果文件已存在且大于10KB，跳过
    if os.path.exists(output_file) and os.path.getsize(output_file) > 10000:
        print(f"[{i}/{len(unique_urls)}] 跳过 (已存在)")
        success += 1
        continue
    
    print(f"[{i}/{len(unique_urls)}] 正在下载: {url[:60]}...")
    
    try:
        result = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
             f"--print-to-pdf={output_file}",
             "--no-pdf-header-footer",
             url],
            capture_output=True,
            timeout=30
        )
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 5000:
            size = os.path.getsize(output_file) / 1024 / 1024
            print(f"  ✓ 成功 ({size:.1f}MB)")
            success += 1
        else:
            print(f"  ✗ 失败 (文件无效)")
            failed += 1
            
    except Exception as e:
        print(f"  ✗ 错误: {str(e)[:50]}")
        failed += 1
    
    # 每3个暂停一下
    if i % 3 == 0 and i < len(unique_urls):
        print(f"--- 已下载 {i} 篇，暂停5秒 ---")
        time.sleep(5)

print("")
print("=" * 50)
print(f"下载完成！成功: {success} | 失败: {failed}")
print(f"保存位置: {OUTPUT_DIR}")
print("=" * 50)

# 显示文件列表
files = sorted(os.listdir(OUTPUT_DIR))
pdfs = [f for f in files if f.endswith('.pdf')]
print(f"\n共 {len(pdfs)} 个 PDF 文件:")
for f in pdfs[:10]:
    size = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
    print(f"  {f} ({size:.0f}KB)")
if len(pdfs) > 10:
    print(f"  ... 还有 {len(pdfs) - 10} 个文件")
