import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.test_harness import EdgeCDPDriver

driver = EdgeCDPDriver(headless=True)
driver.start()
time.sleep(1.0)

driver.click('#nav-knowledge')
time.sleep(0.5)

errors = []
for ch in range(1, 18):
    driver.click(f'#chapter-list-nav [data-ch="{ch}"]')
    time.sleep(0.35)
    info = driver.eval_js('''
    (() => {
        const area = document.getElementById('chapter-content-area');
        const doc = document.documentElement;
        const errs = document.querySelectorAll('.katex-error, .mermaid-error');
        return {
            scrollW: doc.scrollWidth,
            clientW: doc.clientWidth,
            errCount: errs.length,
            title: area ? area.querySelector('h1')?.innerText : ''
        };
    })()
    ''')
    if info['scrollW'] > info['clientW']:
        errors.append(f'Ch {ch}: Horizontal overflow scrollW={info["scrollW"]} > clientW={info["clientW"]}')
    if info['errCount'] > 0:
        errors.append(f'Ch {ch}: Has {info["errCount"]} render errors')
    print(f'Ch {ch:2d}: OK (Width={info["clientW"]}px, Errors={info["errCount"]}) - {info["title"][:40]}')

driver.stop()
if errors:
    print('FOUND ISSUES:', errors)
    sys.exit(1)
else:
    print('ALL 17 CHAPTERS RENDER FLAWLESSLY WITH 0 OVERFLOW AND 0 RENDER ERRORS!')
