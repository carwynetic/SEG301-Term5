import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/knowledge.json', 'r', encoding='utf-8') as f:
    kdata = json.load(f)

# Helper function to escape HTML tags inside inline-code
def fix_inline_code(match):
    code_content = match.group(1)
    # If it contains unescaped HTML tags like <h1>, <title>, <a ...>, <meta ...>
    # replace < with &lt; and > with &gt;
    escaped = code_content.replace('<', '&lt;').replace('>', '&gt;')
    return f'<code class="inline-code">{escaped}</code>'

for ch in kdata:
    old_html = kdata[ch]['content_html']
    # Replace any <code class="inline-code">...</code> where content has tags
    new_html = re.sub(r'<code class="inline-code">(.*?)</code>', fix_inline_code, old_html)
    if new_html != old_html:
        print(f"Fixed inline code tags in Chapter {ch}")
        kdata[ch]['content_html'] = new_html

with open('data/knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(kdata, f, ensure_ascii=False, indent=2)

with open('data/knowledge.js', 'w', encoding='utf-8') as f:
    f.write('// Auto-generated knowledge database for SEG301 Exam Prep Portal\n')
    f.write('window.SEG_KNOWLEDGE = ')
    json.dump(kdata, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("Successfully fixed and synchronized knowledge.json and knowledge.js!")

