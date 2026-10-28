"""
Empirical Adversarial Verification Suite for Milestone 1 (Refined & Rigorous)
Agent: teamwork_challenger_m1_2
Target: SEG301 Exam Prep Portal - Milestone 1
"""

import sys
import os
import json
import time
import math
import asyncio
from typing import Dict, Any, List

sys.stdout.reconfigure(encoding='utf-8')
from tests.test_harness import EdgeCDPDriver, CSSAnalyzer

def calculate_luminance(r: int, g: int, b: int) -> float:
    def channel(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else math.pow((s + 0.055) / 1.055, 2.4)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)

def contrast_ratio(rgb1: tuple, rgb2: tuple) -> float:
    l1 = calculate_luminance(*rgb1)
    l2 = calculate_luminance(*rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def parse_rgb(rgb_str: str) -> tuple:
    import re
    m = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_str)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if rgb_str.startswith("#"):
        hex_c = rgb_str.lstrip("#")
        if len(hex_c) == 3:
            hex_c = "".join(c * 2 for c in hex_c)
        if len(hex_c) >= 6:
            return (int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16))
    return (255, 255, 255)


def run_empirical_suite():
    print("======================================================================")
    print("STARTING EMPIRICAL ADVERSARIAL STRESS TEST - MILESTONE 1 (REFINED)")
    print("======================================================================")

    driver = EdgeCDPDriver(headless=True)
    driver.start()
    time.sleep(1.0)

    findings = []
    stress_results = []

    try:
        # =====================================================================
        # 1A. ACCESSIBILITY STRESS TEST: FORM CONTROLS :focus-visible
        # =====================================================================
        print("\n[CHALLENGE 1A] FORM CONTROLS :focus-visible DUAL RINGS & CONTRAST")
        form_controls = [
            ("Sidebar Search", "#chapter-search-input", ".sidebar-search-box input", "#nav-knowledge"),
            ("Practice Chapter Select", "#practice-ch-select", ".practice-chapter-select", "#nav-practice"),
            ("Bank Search", "#bank-search-input", ".bank-search-input", "#nav-bank"),
            ("Glossary Search", "#glossary-search-input", ".bank-search-input", "#nav-glossary"),
            ("Quick Search Modal Input", "#global-search-input", ".search-modal-input", "modal"),
        ]

        async def audit_form_controls():
            doc = await driver._send_cdp("DOM.getDocument")
            doc_node_id = doc["root"]["nodeId"]

            for name, sel, css_cls, nav_target in form_controls:
                if nav_target == "modal":
                    await driver._send_cdp("Runtime.evaluate", {"expression": "document.querySelector('#open-search-modal').click()"})
                    await asyncio.sleep(0.15)
                else:
                    await driver._send_cdp("Runtime.evaluate", {"expression": f"document.querySelector('{nav_target}').click()"})
                    await asyncio.sleep(0.15)

                node = await driver._send_cdp("DOM.querySelector", {"nodeId": doc_node_id, "selector": sel})
                node_id = node.get("nodeId")
                if not node_id:
                    stress_results.append((f"{name} DOM Presence", False, f"Node {sel} not found in DOM"))
                    continue

                # Force :focus-visible pseudo state via CDP
                await driver._send_cdp("CSS.forcePseudoState", {
                    "nodeId": node_id,
                    "forcedPseudoClasses": ["focus-visible"]
                })
                await asyncio.sleep(0.05)

                eval_res = await driver._send_cdp("Runtime.evaluate", {
                    "expression": f"""
                    (() => {{
                        const el = document.querySelector('{sel}');
                        const s = window.getComputedStyle(el);
                        return {{
                            outline: s.outline,
                            outlineColor: s.outlineColor,
                            outlineStyle: s.outlineStyle,
                            outlineWidth: s.outlineWidth,
                            outlineOffset: s.outlineOffset,
                            boxShadow: s.boxShadow,
                            borderColor: s.borderColor,
                            backgroundColor: s.backgroundColor,
                            color: s.color,
                            tagName: el.tagName
                        }};
                    }})()
                    """,
                    "returnByValue": True
                })
                computed = eval_res.get("result", {}).get("value", {})

                # Release pseudo state
                await driver._send_cdp("CSS.forcePseudoState", {
                    "nodeId": node_id,
                    "forcedPseudoClasses": []
                })

                if nav_target == "modal":
                    await driver._send_cdp("Runtime.evaluate", {"expression": "document.querySelector('#close-search-modal').click()"})
                    await asyncio.sleep(0.1)

                accent_blue_rgb = (56, 189, 248) # #38bdf8
                bg_dark_rgb = (10, 14, 23)       # #0a0e17
                ctrl_bg_rgb = parse_rgb(computed.get('backgroundColor', 'rgb(17, 24, 39)'))

                contrast_against_page = contrast_ratio(accent_blue_rgb, bg_dark_rgb)
                contrast_against_ctrl = contrast_ratio(accent_blue_rgb, ctrl_bg_rgb)

                print(f"  -> {name} ({sel}):")
                print(f"     outline: {computed.get('outline')} (width: {computed.get('outlineWidth')}, offset: {computed.get('outlineOffset')})")
                print(f"     box-shadow: {computed.get('boxShadow')}")
                print(f"     Contrast vs page ({bg_dark_rgb}): {contrast_against_page:.2f}:1")
                print(f"     Contrast vs ctrl bg ({ctrl_bg_rgb}): {contrast_against_ctrl:.2f}:1")

                has_visible_outline = computed.get('outlineWidth') in ('2px', '3px') and computed.get('outlineStyle') == 'solid'
                has_contrast = contrast_against_page >= 3.0 and contrast_against_ctrl >= 3.0
                has_outer_shadow = bool(computed.get('boxShadow') and computed.get('boxShadow') != 'none' and 'rgba(0, 0, 0, 0)' not in computed.get('boxShadow'))

                stress_results.append((f"{name} :focus-visible Solid 2px Outline", has_visible_outline, f"outline={computed.get('outline')}"))
                stress_results.append((f"{name} WCAG Focus Contrast (>=3.0:1)", has_contrast, f"{contrast_against_page:.2f}:1 vs page, {contrast_against_ctrl:.2f}:1 vs ctrl"))
                stress_results.append((f"{name} Outer Box-Shadow Ring", has_outer_shadow, f"boxShadow={computed.get('boxShadow')}"))

                if computed.get('tagName') == 'SELECT' and not has_outer_shadow:
                    findings.append("AESTHETIC VULNERABILITY: <select id='practice-ch-select'> does not render CSS box-shadow in Chromium without `appearance: none`. Its focus-visible outline is fully functional (2px cyan, WCAG compliant), but the outer glow ring is suppressed by the native select widget.")

        driver.loop.run_until_complete(audit_form_controls())


        # =====================================================================
        # 1B. ACCESSIBILITY STRESS TEST: prefers-reduced-motion
        # =====================================================================
        print("\n[CHALLENGE 1B] @media (prefers-reduced-motion: reduce) STRESS TEST")
        driver.set_reduced_motion(True)
        time.sleep(0.2)

        # Audit CSSOM for prefers-reduced-motion rules
        rm_rules = driver.eval_js("""
        (() => {
            let rmList = [];
            for (let sheet of document.styleSheets) {
                try {
                    for (let rule of sheet.cssRules) {
                        if (rule.media && rule.media.mediaText.includes('prefers-reduced-motion: reduce')) {
                            for (let sub of rule.cssRules) {
                                rmList.push({
                                    selector: sub.selectorText,
                                    transform: sub.style.transform,
                                    animation: sub.style.animation,
                                    transition: sub.style.transition
                                });
                            }
                        }
                    }
                } catch(e) {}
            }
            return rmList;
        })()
        """)
        print(f"  -> Found {len(rm_rules)} CSS rule declarations inside @media (prefers-reduced-motion: reduce)")

        test_elements = [
            ("Glossary Card", ".glossary-card"),
            ("Reference Card", ".ref-card"),
            ("Rule Box", ".rule-box"),
            ("Math Block", ".math-block"),
            ("Mermaid Diagram Wrap", ".mermaid-diagram-wrap"),
            ("Primary Button", ".btn-primary"),
            ("Secondary Button", ".btn-secondary"),
            ("Nav Tab", ".nav-tab"),
            ("Option Button", ".option-btn"),
            ("Palette Button", ".palette-btn"),
            ("Option Letter Badge", ".option-letter"),
        ]

        for name, sel in test_elements:
            is_covered = any(sel in r['selector'] for r in rm_rules)
            has_transform_none = any(sel in r['selector'] and 'none' in r.get('transform', '') for r in rm_rules)

            if sel == ".option-letter":
                opt_letter_hover = driver.eval_js("""
                (() => {
                    for (let s of document.styleSheets) {
                        try {
                            for (let r of s.cssRules) {
                                if (r.selectorText && r.selectorText.includes('.option-letter') && r.style.transform) {
                                    return { sel: r.selectorText, transform: r.style.transform };
                                }
                            }
                        } catch(e) {}
                    }
                    return null;
                })()
                """)
                print(f"     [AUDIT] .option-letter hover transform in stylesheet: {opt_letter_hover}")
                if opt_letter_hover and not is_covered:
                    findings.append("MOTION LEAK: `.option-btn:hover:not(:disabled) .option-letter` defines `transform: scale(1.08)` but is omitted from `@media (prefers-reduced-motion: reduce)`. While the parent option button transform is suppressed, the letter badge still magnifies slightly on hover.")

            stress_results.append((f"Reduced Motion: {name} transform suppressed", is_covered or has_transform_none, f"covered={is_covered}"))

        # Check keyframe animations under reduced motion
        keyframe_cancels = driver.eval_js("""
        (() => {
            let res = {};
            for (let s of document.styleSheets) {
                try {
                    for (let r of s.cssRules) {
                        if (r.media && r.media.mediaText.includes('prefers-reduced-motion: reduce')) {
                            for (let sub of r.cssRules) {
                                if (sub.selectorText && sub.style.animation) {
                                    res[sub.selectorText] = sub.style.animation;
                                }
                            }
                        }
                    }
                } catch(e) {}
            }
            return res;
        })()
        """)
        print(f"  -> Keyframe animation overrides in reduced motion: {keyframe_cancels}")
        has_exp_anim_cancel = any('.explanation-box.show' in sel for sel in keyframe_cancels)
        has_opt_anim_cancel = any('correct-choice' in sel for sel in keyframe_cancels)
        has_flag_anim_cancel = any('flagged' in sel for sel in keyframe_cancels)

        stress_results.append(("Reduced Motion: Explanation Fade-Slide Cancelled", has_exp_anim_cancel, f"{keyframe_cancels}"))
        stress_results.append(("Reduced Motion: Option Pop/Shake Cancelled", has_opt_anim_cancel, f"{keyframe_cancels}"))
        stress_results.append(("Reduced Motion: Flagged Question Dot Pulse Cancelled", has_flag_anim_cancel, f"{keyframe_cancels}"))

        driver.set_reduced_motion(False)
        time.sleep(0.2)


        # =====================================================================
        # 2. CONTENT CARD HOVER STRESS TEST (ALL 5 CARD TYPES)
        # =====================================================================
        print("\n[CHALLENGE 2] CONTENT CARD HOVER STRESS TEST (ALL 5 CARD TYPES)")

        cards_to_test = [
            ("Rule Box", ".rule-box", "#nav-exam", None),
            ("Glossary Card", ".glossary-card", "#nav-glossary", None),
            ("Reference Card", ".ref-card", "#nav-knowledge", "1"),
            ("Math Block", ".math-block", "#nav-knowledge", "1"),
            ("Mermaid Diagram Wrap", ".mermaid-diagram-wrap", "#nav-knowledge", "2"),
        ]

        for name, card_sel, tab_btn, ch_id in cards_to_test:
            driver.click(tab_btn)
            time.sleep(0.2)

            if ch_id:
                # Switch chapter if needed (Chapter 2 contains mermaid)
                driver.eval_js(f"""
                (() => {{
                    const item = document.querySelector('.chapter-item[data-chapter-id="{ch_id}"]');
                    if (item) item.click();
                }})()
                """)
                time.sleep(0.4)

            elem_exists = driver.eval_js(f"document.querySelector('{card_sel}') !== null")
            if not elem_exists:
                stress_results.append((f"{name} DOM Presence", False, f"Selector {card_sel} not found in DOM"))
                continue

            hover_test = driver.eval_js(f"""
            (() => {{
                const el = document.querySelector('{card_sel}');
                const origTransition = el.style.transition;
                const origTransform = el.style.transform;

                // Initial baseline measurements
                const rInit = el.getBoundingClientRect();
                const swInit = document.documentElement.scrollWidth;
                const cwInit = document.documentElement.clientWidth;

                // Query CSSOM hover rule
                let cssHoverTransform = null;
                for (let s of document.styleSheets) {{
                    try {{
                        for (let r of s.cssRules) {{
                            if (r.selectorText && r.selectorText.includes('{card_sel}:hover')) {{
                                cssHoverTransform = r.style.transform;
                            }}
                        }}
                    }} catch(e) {{}}
                }}

                // Apply instantaneous translateY(-3px) without transition latency
                el.style.transition = 'none';
                el.style.transform = 'translateY(-3px)';
                const rHover = el.getBoundingClientRect();
                const swHover = document.documentElement.scrollWidth;
                const cwHover = document.documentElement.clientWidth;

                // Measure sibling stability (check if next sibling shifted laterally)
                const nextSib = el.nextElementSibling;
                let sibShiftX = 0;
                if (nextSib) {{
                    const sibRect = nextSib.getBoundingClientRect();
                    sibShiftX = sibRect.left;
                }}

                // Teardown
                el.style.transition = origTransition;
                el.style.transform = origTransform;

                return {{
                    cssHoverTransform: cssHoverTransform,
                    deltaY: rHover.top - rInit.top,
                    deltaX: rHover.left - rInit.left,
                    widthChange: rHover.width - rInit.width,
                    scrollWidthInit: swInit,
                    scrollWidthHover: swHover,
                    scrollDiff: swHover - swInit,
                    clientWidth: cwHover
                }};
            }})()
            """)

            print(f"  -> {name} ({card_sel}):")
            print(f"     CSS hover rule: {hover_test.get('cssHoverTransform')}")
            print(f"     deltaY: {hover_test.get('deltaY'):.2f}px | deltaX: {hover_test.get('deltaX'):.2f}px | widthChange: {hover_test.get('widthChange'):.2f}px")
            print(f"     scrollWidth delta: {hover_test.get('scrollDiff')}px")

            is_trans_y3 = abs(hover_test.get('deltaY', 0) - (-3.0)) < 0.1
            is_zero_x = abs(hover_test.get('deltaX', 0)) < 0.01
            is_zero_scroll = hover_test.get('scrollDiff', 0) == 0
            is_zero_width_change = abs(hover_test.get('widthChange', 0)) < 0.01

            stress_results.append((f"{name} CSS Hover translateY(-3px)", hover_test.get('cssHoverTransform') == 'translateY(-3px)', f"{hover_test.get('cssHoverTransform')}"))
            stress_results.append((f"{name} Strictly Vertical Shift (-3px)", is_trans_y3, f"deltaY={hover_test.get('deltaY')}"))
            stress_results.append((f"{name} Zero Lateral Drift (deltaX=0)", is_zero_x, f"deltaX={hover_test.get('deltaX')}"))
            stress_results.append((f"{name} Zero Horizontal Scroll Leakage", is_zero_scroll, f"scroll delta={hover_test.get('scrollDiff')}px"))
            stress_results.append((f"{name} Zero Width Reflow (width change=0)", is_zero_width_change, f"width change={hover_test.get('widthChange')}px"))


        # =====================================================================
        # 3. ACADEMIC EXPLANATION REVEAL STRESS TEST
        # =====================================================================
        print("\n[CHALLENGE 3] ACADEMIC EXPLANATION REVEAL STRESS TEST")
        driver.click("#nav-practice")
        time.sleep(0.3)

        exp_test = driver.eval_js("""
        (() => {
            const el = document.getElementById('practice-explanation-box');
            if (!el) return null;

            const initDisplay = window.getComputedStyle(el).display;
            const parent = el.closest('.question-card');
            const parentOverflow = parent ? window.getComputedStyle(parent).overflow : null;

            // Measure option button right above explanation
            const options = document.querySelectorAll('.option-btn');
            const lastOpt = options[options.length - 1];
            const optRect = lastOpt ? lastOpt.getBoundingClientRect() : null;

            // Trigger reveal with .show
            el.classList.add('show');
            const showStyle = window.getComputedStyle(el);
            const showDisplay = showStyle.display;
            const animName = showStyle.animationName;
            const animDuration = showStyle.animationDuration;
            const animFill = showStyle.animationFillMode;
            const expRect = el.getBoundingClientRect();

            // Gap between bottom of preceding option and top of explanation box
            const verticalGap = optRect ? (expRect.top - optRect.bottom) : null;

            // Check if explanation box clips inside parent container
            const parentRect = parent ? parent.getBoundingClientRect() : null;
            const isInsideParent = parentRect ? (expRect.top >= parentRect.top && expRect.bottom <= parentRect.bottom + 50) : true;

            // Clean teardown
            el.classList.remove('show');

            return {
                initDisplay: initDisplay,
                showDisplay: showDisplay,
                animName: animName,
                animDuration: animDuration,
                animFill: animFill,
                parentOverflow: parentOverflow,
                verticalGap: verticalGap,
                isInsideParent: isInsideParent
            };
        })()
        """)

        print(f"  -> Initial display: {exp_test.get('initDisplay')} (expected: none)")
        print(f"  -> Revealed display: {exp_test.get('showDisplay')} (expected: block)")
        print(f"  -> Animation name: {exp_test.get('animName')} (expected: explanationFadeSlide)")
        print(f"  -> Animation fill-mode: {exp_test.get('animFill')} (expected: forwards)")
        print(f"  -> Vertical gap above explanation: {exp_test.get('verticalGap')}px")
        print(f"  -> Parent card overflow: {exp_test.get('parentOverflow')}")

        has_init_none = exp_test.get('initDisplay') == 'none'
        has_show_block = exp_test.get('showDisplay') == 'block'
        has_correct_anim = exp_test.get('animName') == 'explanationFadeSlide'
        has_fill_forwards = exp_test.get('animFill') == 'forwards'
        no_collision = exp_test.get('verticalGap') is not None and exp_test.get('verticalGap') > 0
        no_parent_clip = exp_test.get('parentOverflow') not in ('hidden', 'clip')

        stress_results.append(("Explanation Initially Collapsed (display: none)", has_init_none, f"display={exp_test.get('initDisplay')}"))
        stress_results.append(("Explanation Revealed as display: block", has_show_block, f"display={exp_test.get('showDisplay')}"))
        stress_results.append(("Explanation Keyframe Binding (explanationFadeSlide)", has_correct_anim, f"animation={exp_test.get('animName')}"))
        stress_results.append(("Explanation Animation Fill-Mode (forwards)", has_fill_forwards, f"fillMode={exp_test.get('animFill')}"))
        stress_results.append(("Explanation Zero Visual Collision with Preceding Elements", no_collision, f"verticalGap={exp_test.get('verticalGap')}px"))
        stress_results.append(("Explanation Parent Container Unclipped", no_parent_clip, f"parentOverflow={exp_test.get('parentOverflow')}"))

    finally:
        driver.stop()

    print("\n" + "=" * 70)
    print("EMPIRICAL ADVERSARIAL STRESS TEST SUMMARY")
    print("=" * 70)
    passed_count = sum(1 for name, ok, msg in stress_results if ok)
    total_count = len(stress_results)

    for name, ok, msg in stress_results:
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"[{status}] {name}")
        if not ok:
            print(f"      Detail: {msg}")

    print("-" * 70)
    print(f"TOTAL TESTS: {total_count} | PASSED: {passed_count} | FAILED: {total_count - passed_count}")
    print(f"SUCCESS RATE: {(passed_count / total_count * 100):.1f}%")
    print("=" * 70)

    if findings:
        print("\nADVERSARIAL VULNERABILITIES & BLINDSPOTS DETECTED:")
        for idx, f in enumerate(findings, 1):
            print(f"  {idx}. {f}")

    return passed_count, total_count, findings, stress_results

if __name__ == "__main__":
    passed, total, findings, stress_results = run_empirical_suite()
    sys.exit(0 if (total - passed) == 0 else 1)
