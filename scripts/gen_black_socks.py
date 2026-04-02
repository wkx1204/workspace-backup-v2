#!/usr/bin/env python3
import urllib.request, json, base64

api_key = "sk-6c77177dd0ba457cb05f7e0c15289c61"
avatar_path = "/Users/wf/.openclaw/workspace-main/xiaobai-site/images/avatar.jpg"
out_path = "/Users/wf/.openclaw/workspace-main/inbox/xiaobai_black_socks.png"

with open(avatar_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

payload = json.dumps({
    "model": "qwen-image-2.0",
    "input": {
        "messages": [{
            "role": "user",
            "content": [
                {"image": "data:image/jpeg;base64," + b64},
                {"text": "时尚女性造型，黑色丝袜，优雅气质，精致妆容，影棚灯光，高清摄影"}
            ]
        }]
    }
}, ensure_ascii=False).encode('utf-8')

print(f"Payload size: {len(payload)}, B64 size: {len(b64)}")

req = urllib.request.Request(
    'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation',
    data=payload,
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json; charset=utf-8'
    }
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        result = json.loads(r.read())
        url = result['output']['choices'][0]['message']['content'][0]['image']
        print('SUCCESS:', url)
        
        img_req = urllib.request.Request(url)
        with urllib.request.urlopen(img_req, timeout=30) as img_r:
            data = img_r.read()
            with open(out_path, 'wb') as f:
                f.write(data)
        print(f'Downloaded: {len(data)} bytes')
except Exception as e:
    print(f'Error: {e}')
