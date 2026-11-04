import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
data = json.load(open('data/knowledge.json', encoding='utf-8'))

# Check all <code class="inline-code">...</code>
for ch in data:
    html = data[ch]['content_html']
    # Find all inline code blocks
    code_blocks = re.findall(r'<code class="inline-code">(.*?)</code>', html)
    for cb in code_blocks:
        # Check if cb contains unescaped <tag> or </tag>
        if re.search(r'</?[a-zA-Z][a-zA-Z0-9_-]*(?:\s+[^>]*)?>', cb):
            print(f"Ch {ch} unescaped in inline code: {repr(cb)}")

