#!/usr/bin/env node
// 通过 CDP (Chrome DevTools Protocol) 控制 Chrome
const http = require('http');
const WebSocket = require('ws');

const CDP_HOST = '127.0.0.1';
const CDP_PORT = 9222;

function httpGet(path) {
    return new Promise((resolve, reject) => {
        const options = { hostname: CDP_HOST, port: CDP_PORT, path, method: 'GET' };
        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(JSON.parse(data)));
        });
        req.on('error', reject);
        req.end();
    });
}

function wsSend(ws, id, method, params) {
    return new Promise(resolve => {
        const msg = JSON.stringify({ id, method, params });
        ws.send(msg);
        // 收集响应
        ws._pending = ws._pending || {};
        ws._pending[id] = { resolve };
    });
}

function wsHandleMessage(ws, data) {
    const msg = JSON.parse(data);
    if (msg.id && ws._pending && ws._pending[msg.id]) {
        ws._pending[msg.id].resolve(msg);
        delete ws._pending[msg.id];
    }
}

async function main() {
    // 1. 获取页面列表
    const pages = await httpGet('/json/list');
    console.log('页面列表:', pages.length);
    
    const targetPage = pages.find(p => p.type === 'page');
    console.log('目标页面:', targetPage?.id, targetPage?.title);
    
    if (!targetPage) {
        console.log('没有找到页面');
        return;
    }

    // 2. 连接到页面的 WebSocket
    const wsUrl = `ws://${CDP_HOST}:${CDP_PORT}${targetPage.webSocketDebuggerUrl.replace('ws://127.0.0.1:9222', '')}`;
    console.log('连接:', wsUrl);
    
    const ws = new WebSocket(wsUrl);
    await new Promise(r => ws.on('open', r));
    console.log('WebSocket 已连接');
    
    ws.on('message', data => wsHandleMessage(ws, data.toString()));
    
    let msgId = 1;
    
    // 3. 导航到微信文章
    const testUrl = 'https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491737&idx=1&sn=7540894e1d73a1cf20da8e34ba421634';
    console.log('\n导航到:', testUrl);
    
    const navResp = await wsSend(ws, msgId++, 'Page.navigate', { url: testUrl });
    console.log('导航响应:', navResp);
    
    // 4. 等待页面加载
    console.log('等待 8 秒让页面渲染...');
    await new Promise(r => setTimeout(r, 8000));
    
    // 5. 打印页面标题
    const titleResp = await wsSend(ws, msgId++, 'Runtime.evaluate', { 
        expression: 'document.title' 
    });
    console.log('页面标题:', titleResp.result?.result?.value);
    
    // 6. 检查是否遇到验证
    const bodyResp = await wsSend(ws, msgId++, 'Runtime.evaluate', { 
        expression: 'document.body.innerText.substring(0, 500)' 
    });
    console.log('页面内容前500字:', bodyResp.result?.result?.value?.substring(0, 300));
    
    ws.close();
    console.log('\n完成');
}

main().catch(console.error);
