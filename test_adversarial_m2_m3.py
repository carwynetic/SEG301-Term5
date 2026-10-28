import asyncio
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
from tests.test_harness import EdgeCDPDriver, CSSAnalyzer, JSAnalyzer

def run_adversarial_suite():
    driver = EdgeCDPDriver(headless=True)
    driver.start()
    time.sleep(1.0)
    
    css = CSSAnalyzer()
    js = JSAnalyzer()
    
    issues = []
    
    try:
        print("=== PROBING 1: Chapter Hero Reveal State Under .js-reveal-active ===")
        # Check computed style of .chapter-hero.reveal-on-scroll before revealed
        driver.click("#nav-knowledge")
        driver.click('#chapter-list-nav [data-ch="3"]')
        time.sleep(0.2)
        hero_style = driver.eval_js("""
        (() => {
            const el = document.createElement('div');
            el.className = 'chapter-hero reveal-on-scroll';
            document.body.appendChild(el);
            const cs = window.getComputedStyle(el);
            const res = {
                opacity: cs.opacity,
                transform: cs.transform,
                willChange: cs.willChange,
                isRootActive: document.documentElement.classList.contains('js-reveal-active')
            };
            el.remove();
            return res;
        })()
        """)
        print("Hero pending state:", hero_style)
        if hero_style and float(hero_style.get('opacity', 1.0)) > 0.1:
            issues.append(f"Chapter hero does NOT have opacity: 0 before being revealed! Opacity is {hero_style.get('opacity')}. It is not hidden before reveal.")

        print("\n=== PROBING 2: prefers-reduced-motion scroll behavior ===")
        # Test if smooth scrolling is still used when reduced-motion is requested
        driver.set_reduced_motion(True)
        time.sleep(0.1)
        reduced_js_eval = driver.eval_js("""
        (() => {
            const isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            return { isReduced };
        })()
        """)
        print("Reduced motion media match:", reduced_js_eval)
        
        # Check if getScrollBehavior is called by scrollTo or scrollIntoView in app.js
        with open('js/app.js', 'r', encoding='utf-8') as f:
            app_code = f.read()
        import re
        smooth_calls = re.findall(r"behavior:\s*'smooth'", app_code)
        print(f"Hardcoded behavior: 'smooth' calls in app.js: {len(smooth_calls)}")
        if len(smooth_calls) > 0:
            issues.append(f"Found {len(smooth_calls)} hardcoded behavior: 'smooth' calls in js/app.js ignoring prefers-reduced-motion")

        print("\n=== PROBING 3: CSS .will-change selector bug ===")
        with open('css/style.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        if ".will-change," in css_content:
            issues.append("Found '.will-change,' selector grouped with .reveal-on-scroll hiding any .will-change element with opacity: 0")

        print("\n=== PROBING 4: Horizontal Overflow (CLS) across Viewports and Tabs ===")
        viewports = [(320, 568), (360, 640), (375, 667), (768, 1024), (1024, 768), (1280, 800), (1440, 900)]
        tabs = ['knowledge', 'practice', 'exam', 'bank', 'glossary']
        
        async def test_viewports():
            for width, height in viewports:
                await driver._send_cdp("Emulation.setDeviceMetricsOverride", {
                    "width": width,
                    "height": height,
                    "deviceScaleFactor": 1,
                    "mobile": width < 768
                })
                await asyncio.sleep(0.1)
                
                for t in tabs:
                    await driver._send_cdp("Runtime.evaluate", {"expression": f"document.getElementById('nav-{t}').click()"})
                    await asyncio.sleep(0.05)
                    overflow_info = await driver._send_cdp("Runtime.evaluate", {
                        "expression": """
                        (() => {
                            const sw = document.documentElement.scrollWidth;
                            const cw = document.documentElement.clientWidth;
                            const bodySw = document.body.scrollWidth;
                            const bodyCw = document.body.clientWidth;
                            return { sw, cw, bodySw, bodyCw, diff: sw - cw };
                        })()
                        """,
                        "returnByValue": True
                    })
                    val = overflow_info.get("result", {}).get("value", {})
                    if val.get("diff", 0) > 1:
                        issues.append(f"Viewport {width}x{height} tab '{t}' has horizontal overflow: scrollWidth {val.get('sw')} > clientWidth {val.get('cw')}")
        
        driver.loop.run_until_complete(test_viewports())

        print("\n=== PROBING 5: Exam Tab Screens (Intro, Active, Results) Overflow ===")
        async def test_exam_screens():
            # Set to 375x667 (iPhone standard)
            await driver._send_cdp("Emulation.setDeviceMetricsOverride", {
                "width": 375,
                "height": 667,
                "deviceScaleFactor": 2,
                "mobile": True
            })
            await driver._send_cdp("Runtime.evaluate", {"expression": "document.getElementById('nav-exam').click()"})
            await asyncio.sleep(0.1)
            
            # Start exam
            await driver._send_cdp("Runtime.evaluate", {"expression": "document.getElementById('start-exam-btn').click()"})
            await asyncio.sleep(0.1)
            active_overflow = await driver._send_cdp("Runtime.evaluate", {
                "expression": """
                (() => {
                    const sw = document.documentElement.scrollWidth;
                    const cw = document.documentElement.clientWidth;
                    return { sw, cw, diff: sw - cw };
                })()
                """,
                "returnByValue": True
            })
            val = active_overflow.get("result", {}).get("value", {})
            if val.get("diff", 0) > 1:
                issues.append(f"Active exam screen on 375px mobile has horizontal overflow: {val.get('sw')} > {val.get('cw')}")

            # Submit exam
            await driver._send_cdp("Runtime.evaluate", {"expression": "document.getElementById('exam-submit-early-btn').click()"})
            await asyncio.sleep(0.05)
            await driver._send_cdp("Runtime.evaluate", {"expression": "document.getElementById('confirm-submit-btn').click()"})
            await asyncio.sleep(0.1)
            results_overflow = await driver._send_cdp("Runtime.evaluate", {
                "expression": """
                (() => {
                    const sw = document.documentElement.scrollWidth;
                    const cw = document.documentElement.clientWidth;
                    return { sw, cw, diff: sw - cw };
                })()
                """,
                "returnByValue": True
            })
            r_val = results_overflow.get("result", {}).get("value", {})
            if r_val.get("diff", 0) > 1:
                issues.append(f"Exam results screen on 375px mobile has horizontal overflow: {r_val.get('sw')} > {r_val.get('cw')}")

        driver.loop.run_until_complete(test_exam_screens())

        print("\n=== PROBING 6: Dynamic Question Switch Transition in Practice & Exam ===")
        # Check if animation triggers when next question is clicked
        driver.click("#nav-practice")
        anim_info = driver.eval_js("""
        (() => {
            const card = document.getElementById('practice-question-card');
            const initialAnim = card ? window.getComputedStyle(card).animationName : null;
            const nextBtn = document.getElementById('practice-next-btn');
            if (nextBtn) nextBtn.click();
            const afterClickAnim = card ? window.getComputedStyle(card).animationName : null;
            return { initialAnim, afterClickAnim };
        })()
        """)
        print("Practice question animation info:", anim_info)

        print("\n=== PROBING 7: window.SEG_ANIMATIONS API Contract Boundary Checks ===")
        boundary_errors = driver.eval_js("""
        (() => {
            const errs = [];
            try {
                window.SEG_ANIMATIONS.observeScrollReveals(null);
                window.SEG_ANIMATIONS.observeScrollReveals(undefined);
                window.SEG_ANIMATIONS.observeScrollReveals({});
                window.SEG_ANIMATIONS.observeScrollReveals("not an element");
                window.SEG_ANIMATIONS.observeScrollReveals(12345);
                window.SEG_ANIMATIONS.observeScrollReveals(document.createElement('div'));
                window.SEG_ANIMATIONS.refresh();
            } catch (e) {
                errs.push(e.toString());
            }
            return errs;
        })()
        """)
        print("API contract boundary errors:", boundary_errors)
        if boundary_errors:
            issues.append(f"window.SEG_ANIMATIONS failed boundary calls: {boundary_errors}")

    finally:
        driver.stop()

    print("\n" + "=" * 70)
    print("PROBING SUMMARY - IDENTIFIED ISSUES:")
    print("=" * 70)
    for idx, iss in enumerate(issues, 1):
        print(f"{idx}. {iss}")
    if not issues:
        print("✓ No issues found!")
    print("=" * 70)

if __name__ == '__main__':
    run_adversarial_suite()
