import urllib.request, json, base64, sys

ZHIPU_KEY = "a19f985d59154c05b97bfe4eae722017.H0XLQhQA9O1Ihfqi"
IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "/Users/wf/.openclaw/workspace-main/inbox/xiaobai_white_dress.png"

with open(IMAGE_PATH, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

data = json.dumps({
    'model': 'glm-4.6v-flashx',
    'messages': [{
        'role': 'user',
        'content': [
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{b64}'}},
            {'type': 'text', 'text': '描述这张图片的内容'}
        ]
    }]
}).encode()

req = urllib.request.Request(
    'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    data=data,
    headers={'Authorization': f'Bearer {ZHIPU_KEY}', 'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req, timeout=30) as r:
    result = json.loads(r.read())
    print(result['choices'][0]['message']['content'])
