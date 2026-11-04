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
driver.click('#chapter-list-nav [data-ch="1"]')
time.sleep(0.5)

info = driver.eval_js('''
(() => {
    const errs = Array.from(document.querySelectorAll('.katex-error')).map(e => ({
        title: e.getAttribute('title') || e.innerText,
        text: e.innerText
    }));
    // find overflowing elements
    const overflows = [];
    document.querySelectorAll('*').forEach(el => {
        if (el.scrollWidth > document.documentElement.clientWidth + 5) {
            overflows.push({
                tag: el.tagName,
                cls: el.className,
                id: el.id,
                scrollW: el.scrollWidth,
                clientW: el.clientWidth
            });
        }
    });
    return { errs, overflows: overflows.slice(0, 10), docScroll: document.documentElement.scrollWidth, docClient: document.documentElement.clientWidth, bodyScroll: document.body.scrollWidth, bodyClient: document.body.clientWidth };
})()
''')
print('KaTeX errors in Ch 1:', info['errs'])
print('Overflowing elements:', info['overflows'])
print('Doc dimensions:', info['docScroll'], info['docClient'], info['bodyScroll'], info['bodyClient'])
driver.stop()
