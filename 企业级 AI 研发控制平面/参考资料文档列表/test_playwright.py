#!/usr/bin/env python3
"""使用 Playwright 绕过微信反爬虫下载 PDF"""
import asyncio
from playwright.async_api import async_playwright
import os

OUTPUT_DIR = "/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def test_wechat():
    test_url = "https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491737&idx=1&sn=7540894e1d73a1cf20da8e34ba421634"
    output_file = f"{OUTPUT_DIR}/test_playwright.pdf"
    
    print(f"测试 URL: {test_url[:60]}...")
    
    async with async_playwright() as p:
        # 使用系统 Chrome
        print("启动 Chromium...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--window-size=1920,1080',
                '--enable-features=NetworkService,NetworkServiceInProcess',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
            ]
        )
        
        # 创建 context（类似无痕模式）
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            }
        )
        
        page = await context.new_page()
        
        # 拦截可能的反爬虫检测
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
            window.chrome = { runtime: {} };
        """)
        
        print("导航到页面...")
        try:
            response = await page.goto(test_url, wait_until='networkidle', timeout=30000)
            print(f"响应状态: {response.status if response else 'None'}")
            
            # 等待内容加载
            await asyncio.sleep(5)
            
            # 检查页面标题
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 检查是否有反爬虫提示
            content = await page.content()
            if '验证' in content or '安全验证' in content or '拦截' in content:
                print("⚠️ 检测到安全验证页面")
            else:
                print("✓ 页面内容正常")
            
            # 生成 PDF
            print("生成 PDF...")
            await page.pdf(
                path=output_file,
                format='A4',
                landscape=False,
                print_background=True,
                margin={'top': '0.5cm', 'bottom': '0.5cm', 'left': '0.5cm', 'right': '0.5cm'}
            )
            
            file_size = os.path.getsize(output_file)
            print(f"✓ PDF 已保存: {output_file} ({file_size} bytes = {file_size/1024:.1f}KB)")
            
        except Exception as e:
            print(f"✗ 错误: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_wechat())
