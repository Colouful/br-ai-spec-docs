#!/bin/bash
# 批量下载微信文章为PDF

OUTPUT_DIR="/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs"
MARKDOWN_FILE="/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/微信文章链接列表.md"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 确保输出目录存在
mkdir -p "$OUTPUT_DIR"

# 从markdown中提取所有微信文章链接
echo "正在提取链接..."
urls=$(grep -E 'https://mp\.weixin\.qq\.com/s' "$MARKDOWN_FILE" | grep -oE 'https://mp\.weixin\.qq\.com/s\?[^ )]+' | head -20)

# 初始化计数器
count=1

echo "开始下载PDF（共20篇测试）..."
echo "========================"

# 遍历链接并下载为PDF
while IFS= read -r url; do
    # 跳过空行
    [ -z "$url" ] && continue
    
    # 生成文件名（从URL中提取短ID）
    filename=$(echo "$url" | md5 | cut -c1-8)
    # 获取URL中的关键标识
    sn=$(echo "$url" | grep -oE '(sn=[a-z0-9]+)' | head -1)
    if [ -z "$sn" ]; then
        sn="id_$count"
    fi
    
    output="$OUTPUT_DIR/${count}_$(echo $sn | tr '=' '_').pdf"
    
    echo "[$count] 正在下载: ${url:0:60}..."
    
    # 使用Chrome headless模式生成PDF
    "$CHROME" --headless --disable-gpu \
        --print-to-pdf="$output" \
        --no-pdf-header-footer \
        "$url" 2>/dev/null
    
    if [ -f "$output" ]; then
        size=$(ls -lh "$output" | awk '{print $5}')
        echo "  ✓ 保存成功: $(basename "$output") ($size)"
    else
        echo "  ✗ 下载失败"
    fi
    
    count=$((count + 1))
    
    # 每5个暂停一下，避免被限制
    if [ $((count % 5)) -eq 0 ]; then
        echo "--- 已下载 $count 篇，暂停3秒 ---"
        sleep 3
    fi
    
done <<< "$urls"

echo ""
echo "========================"
echo "下载完成！共处理 $((count-1)) 篇"
echo "保存位置: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR" | head -20
