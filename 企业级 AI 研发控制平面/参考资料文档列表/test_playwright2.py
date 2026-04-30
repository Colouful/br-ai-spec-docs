#!/usr/bin/env python3
"""Playwright 增强版：更真实的浏览器指纹 + 等待渲染"""
from playwright.async_api import async_playwright
import asyncio
import os

OUTPUT_DIR = "/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def download_wechat_article(page, url, output_path, retry=2):
    """下载单个微信文章"""
    for attempt in range(retry):
        try:
            print(f"  访问: {url[:70]}...")
            
            response = await page.goto(url, 
                wait_until='domcontentloaded',
                timeout=30000)
            
            if response and response.status != 200:
                print(f"  ⚠️ 状态码: {response.status}")
                continue
            
            # 等待页面主要内容渲染
            try:
                await page.wait_for_selector('#img-content, .rich_media_content, article', 
                    timeout=10000)
                print(f"  ✓ 内容已加载")
            except:
                print(f"  ⚠️ 内容选择器未找到，继续...")
            
            # 额外等待让 JS 完全执行
            await asyncio.sleep(3)
            
            # 检查页面标题
            title = await page.title()
            print(f"  标题: {title[:40]}")
            
            # 检查是否在验证页面
            content = await page.content()
            if '验证' in title or '安全验证' in content:
                print(f"  ⚠️ 遇到安全验证")
                if attempt < retry - 1:
                    await asyncio.sleep(5)
                    continue
                continue
            
            # 生成 PDF
            await page.pdf(
                path=output_path,
                format='A4',
                landscape=False,
                print_background=True,
                margin={'top': '0.3cm', 'bottom': '0.3cm', 'left': '0.3cm', 'right': '0.3cm'}
            )
            
            file_size = os.path.getsize(output_path)
            print(f"  ✓ PDF: {output_path} ({file_size/1024:.0f}KB)")
            return True
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
            if attempt < retry - 1:
                await asyncio.sleep(3)
    
    return False

async def main():
    test_url = "https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491737&idx=1&sn=7540894e1d73a1cf20da8e34ba421634"
    output_file = os.path.join(OUTPUT_DIR, "01_test2.pdf")
    
    async with async_playwright() as p:
        print("启动 Chromium（增强反检测模式）...")
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-automation',
                '--disable-infobars',
                '--disable-browser-across-features',
                '--disable-client-side-phishing-detection',
                '--disable-default-apps',
                '--disable-extensions',
                '--disable-hang-monitor',
                '--disable-popup-blocking',
                '--disable-prompt-on-repost',
                '--disable-sync',
                '--disable-translate',
                '--metrics-recording-only',
                '--safebrowsing-disable-auto-update',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--disable-gpu-compositing',
                '--disable-gpu-rasterization',
                '--disable-gpu-sandbox',
                '--disable-software-rasterizer',
                '--disable-webgl',
                '--disable-webgl2',
                '--window-size=1440,900',
                '--enable-features=NetworkService,NetworkServiceInProcess',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--ignore-certificate-errors',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='zh-CN',
            timezone_id='Asia/Shanghai',
        )
        
        # 反检测脚本
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    { name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer' },
                    { name: 'Chrome PDF Viewer', description: '', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                    { name: 'Native Client', description: '', filename: 'internal-nacl-plugin' }
                ]
            });
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en-US', 'en']});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
            Object.defineProperty(navigator, 'platform', {get: () => 'MacIntel'});
            window.chrome = { runtime: {connect: () => {}, sendMessage: () => {}}, loadTimes: () => ({}), csi: () => ({})};
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """)
        
        page = await context.new_page()
        page.set_default_timeout(30000)
        
        print("\n开始测试...\n")
        success = await download_wechat_article(page, test_url, output_file)
        
        await browser.close()
        print("\n测试完成")

if __name__ == "__main__":
    asyncio.run(main())
