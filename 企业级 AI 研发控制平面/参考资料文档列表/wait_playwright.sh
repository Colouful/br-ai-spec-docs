#!/bin/bash
# 监听 Playwright Chromium 安装完成
while ps aux | grep -q "[p]laywright install chromium"; do
    sleep 10
done
echo "DONE"
osascript -e 'display notification "Playwright Chromium 安装完成！" with title "下载任务"'
say "Playwright 安装完成"
