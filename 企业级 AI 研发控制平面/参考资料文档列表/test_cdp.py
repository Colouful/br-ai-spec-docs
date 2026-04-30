#!/usr/bin/env python3
"""通过CDP连接Chrome并生成PDF"""
import json
import time
import subprocess
import sys

CDP_URL = "http://127.0.0.1:9223"

def get_chrome_debugger_info():
    """获取Chrome调试端点"""
    import urllib.request
    try:
        with urllib.request.urlopen(f"{CDP_URL}/json", timeout=5) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"连接失败: {e}")
        return None

def main():
    # 测试URL（之前被拦截的）
    test_url = "https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491737&idx=1&sn=7540894e1d73a1cf20da8e34ba421634"
    
    print("获取Chrome调试信息...")
    tabs = get_chrome_debugger_info()
    if not tabs:
        print("无法连接到Chrome调试端口")
        return
    
    print(f"找到 {len(tabs)} 个标签页")
    for i, tab in enumerate(tabs):
        print(f"  [{i}] {tab.get('title', '无标题')[:50]} - {tab.get('url', '')[:80]}")
    
    # 获取第一个可用的 WS URL
    ws_url = None
    for tab in tabs:
        if tab.get('webSocketDebuggerUrl'):
            ws_url = tab['webSocketDebuggerUrl']
            break
    
    if not ws_url:
        print("没有找到可用的调试URL")
        return
    
    print(f"\n连接到: {ws_url[:50]}...")
    
    # 使用 websocket-client 连接
    try:
        import websocket
        ws = websocket.create_connection(ws_url, timeout=10)
        print("WebSocket连接成功!")
        
        # 导航到目标URL
        cmd_id = 1
        ws.send(json.dumps({"id": cmd_id, "method": "Page.navigate", "params": {"url": test_url}}))
        
        # 等待页面加载
        print(f"导航到: {test_url[:60]}...")
        time.sleep(8)  # 等待微信页面加载
        
        # 打印所有接收到的消息
        print("\n接收到的消息:")
        for _ in range(20):
            try:
                msg = ws.recv()
                data = json.loads(msg)
                if data.get('method', '').startswith('Page.'):
                    print(f"  {data.get('method')}: {str(data.get('params', ''))[:100]}")
                elif data.get('id') == cmd_id:
                    print(f"  导航结果: {data.get('result', {}).get('frameId', 'ok')}")
            except:
                break
        
        # 等待更多内容加载
        print("\n等待页面完全加载...")
        time.sleep(5)
        
        # 尝试打印PDF
        print("\n生成PDF...")
        cmd_id = 2
        ws.send(json.dumps({
            "id": cmd_id,
            "method": "Page.printToPDF",
            "params": {
                "paperWidth": 8.5,
                "paperHeight": 11,
                "marginTop": 0.4,
                "marginBottom": 0.4,
                "marginLeft": 0.4,
                "marginRight": 0.4,
                "printBackground": True,
                "landscape": False
            }
        }))
        
        for _ in range(10):
            try:
                msg = ws.recv()
                data = json.loads(msg)
                if data.get('id') == cmd_id:
                    if 'result' in data and 'data' in data['result']:
                        pdf_data = data['result']['data']
                        import base64
                        pdf_bytes = base64.b64decode(pdf_data)
                        
                        output_path = "/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs/test_cdp.pdf"
                        with open(output_path, 'wb') as f:
                            f.write(pdf_bytes)
                        print(f"PDF已保存: {output_path} ({len(pdf_bytes)} bytes)")
                    else:
                        print(f"结果: {data}")
                    break
            except Exception as e:
                print(f"接收错误: {e}")
                break
        
        ws.close()
        
    except ImportError:
        print("需要安装 websocket-client: pip3 install websocket-client")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
