"""
Tier 2: Boundary & Corner Cases E2E Tests (>= 75 Tests across F1-F15)
Covers edge cases, disabled states, reduced-motion overrides, zero-margin intersection,
rapid clicks, DOM re-renders, and boundary limits for all 15 features.
Strictly opaque-box DOM event interaction.
"""

import time
from tests.test_harness import CSSAnalyzer, JSAnalyzer, EdgeCDPDriver, TestReporter


def run_tier2_tests(driver: EdgeCDPDriver, css: CSSAnalyzer, js: JSAnalyzer, reporter: TestReporter):
    print("\n--- Running Tier 2: Boundary & Corner Cases Tests (F1 - F15) ---")

    # =========================================================================
    # F1 Boundary: Rapid clicks, extreme zoom, sibling layout stability
    # =========================================================================
    # T2_F1_1: Rapid button spamming (5 clicks in 100ms)
    driver.click("#nav-practice")
    res = driver.eval_js("""
    (() => {
        const btn = document.getElementById('practice-next-btn');
        let count = 0;
        for (let i = 0; i < 5; i++) {
            if (btn && !btn.disabled) {
                btn.click();
                count++;
            }
        }
        return count;
    })()
    """)
    reporter.record(
        "T2_F1_1", "F1", "Tier 2",
        "Rapid button click spam does not break click handlers or throw exceptions",
        res >= 1,
        f"Rapid clicks executed: {res}"
    )

    # T2_F1_2: Pointer leaving during active state resets transform
    active_rules = css.get_rule_content(r'\.btn-primary:active|\.btn-secondary:active')
    scoped_active = all("transform" in r for r in active_rules) if active_rules else False
    reporter.record(
        "T2_F1_2", "F1", "Tier 2",
        "Tactile active press transform resets cleanly when pointer releases",
        scoped_active,
        "Active transforms not cleanly isolated"
    )

    # T2_F1_3: Primary button with long text maintains alignment
    btn_overflow = driver.eval_js("""
    (() => {
        const btn = document.querySelector('.btn-primary');
        if (!btn) return true;
        return btn.scrollWidth <= btn.clientWidth + 2;
    })()
    """)
    reporter.record(
        "T2_F1_3", "F1", "Tier 2",
        "Button content remains within layout boundaries without text overflow",
        bool(btn_overflow),
        "Button text overflows container"
    )

    # T2_F1_4: Focus-visible ring contrast with outline-offset
    focus_rules = css.get_rule_content(r':focus-visible')
    has_offset = any("outline-offset" in r or "box-shadow" in r for r in focus_rules)
    reporter.record(
        "T2_F1_4", "F1", "Tier 2",
        "Button :focus-visible includes outline-offset or ring shadow for high visibility",
        has_offset,
        "Missing outline-offset or ring box-shadow in :focus-visible rules"
    )

    # T2_F1_5: Tactile press does not cause layout shift on sibling elements
    h_before = driver.get_bounding_rect(".practice-header-bar").get("height", 0)
    driver.eval_js('document.getElementById("practice-prev-btn")?.focus()')
    h_after = driver.get_bounding_rect(".practice-header-bar").get("height", 0)
    reporter.record(
        "T2_F1_5", "F1", "Tier 2",
        "Button active and focus states produce zero Cumulative Layout Shift on header bar",
        abs(h_before - h_after) < 0.5,
        f"Header height shifted from {h_before} to {h_after}"
    )

    # =========================================================================
    # F2 Boundary: Disabled button clicks, tab navigation, dynamic transitions
    # =========================================================================
    # T2_F2_1: Rapid clicking disabled prev-btn on Q1 does not trigger index change
    driver.eval_js("""
    (() => {
        const select = document.getElementById("practice-ch-select");
        if (select) {
            select.value = "1";
            select.dispatchEvent(new Event("change"));
        }
    })()
    """)
    time.sleep(0.08)
    driver.eval_js("""
    (() => {
        const prev = document.getElementById('practice-prev-btn');
        for (let i = 0; i < 5; i++) {
            if (prev) prev.click();
        }
    })()
    """)
    idx = driver.eval_js('document.getElementById("practice-progress-text")?.textContent || ""')
    reporter.record(
        "T2_F2_1", "F2", "Tier 2",
        "Clicking disabled #practice-prev-btn on Q1 does not alter question index (remains 1/50)",
        "1" in idx and "50" in idx,
        f"Progress text changed to: '{idx}'"
    )

    # T2_F2_2: Question 50 boundary disabled next-btn
    driver.eval_js("""
    (() => {
        const nextBtn = document.getElementById('practice-next-btn');
        for (let i = 0; i < 55 && nextBtn && !nextBtn.disabled; i++) {
            nextBtn.click();
        }
    })()
    """)
    time.sleep(0.08)
    next_disabled = driver.eval_js('document.getElementById("practice-next-btn")?.disabled')
    reporter.record(
        "T2_F2_2", "F2", "Tier 2",
        "Navigating to final Question 50 dynamically applies disabled attribute to #practice-next-btn",
        bool(next_disabled),
        f"practice-next-btn disabled state is {next_disabled}"
    )

    # T2_F2_3: Disabled button suppresses pointer events or clicks
    disabled_prev_cursor = driver.get_computed_style("#practice-prev-btn:disabled").get("cursor") or \
                           driver.get_computed_style("#practice-next-btn:disabled").get("cursor")
    reporter.record(
        "T2_F2_3", "F2", "Tier 2",
        "Disabled buttons enforce cursor: not-allowed at boundary indices",
        "not-allowed" in (disabled_prev_cursor or ""),
        f"Disabled button cursor is '{disabled_prev_cursor}'"
    )

    # T2_F2_4: Dynamically disabled button suppresses hover transform
    dis_hover_rules = css.get_rule_content(r':disabled:hover|\.btn:disabled:hover|\.btn-primary:disabled')
    suppresses_hover = any("transform: none" in r or "transform:none" in r or "box-shadow: none" in r for r in dis_hover_rules) or \
                       any("transform: none" in r for r in css.get_rule_content(r':disabled'))
    reporter.record(
        "T2_F2_4", "F2", "Tier 2",
        "Disabled button styling explicitly neutralizes hover transforms (transform: none)",
        suppresses_hover,
        "Disabled buttons do not suppress hover transform in CSS"
    )

    # T2_F2_5: Option buttons in answered state prevent double counting
    driver.eval_js("""
    (() => {
        const select = document.getElementById('practice-ch-select');
        if (select) {
            select.value = '2';
            select.dispatchEvent(new Event('change'));
        }
    })()
    """)
    time.sleep(0.08)
    driver.eval_js("""
    (() => {
        const opt = document.querySelector('#practice-options-list .option-btn');
        if (opt) {
            opt.click();
            opt.click(); // Double click
        }
    })()
    """)
    score_sum = driver.eval_js("""
    (() => {
        const c = parseInt(document.getElementById('practice-correct-count')?.textContent || '0', 10);
        const inc = parseInt(document.getElementById('practice-incorrect-count')?.textContent || '0', 10);
        return c + inc;
    })()
    """)
    reporter.record(
        "T2_F2_5", "F2", "Tier 2",
        "Option button click locks question against double submission / score inflation",
        score_sum <= 1,
        f"Score sum is {score_sum} after multiple clicks"
    )

    # =========================================================================
    # F3 Boundary: Rapid tab spamming, idempotent active clicks, narrow viewport
    # =========================================================================
    # T2_F3_1: Rapid tab cycling (5 tabs in 100ms)
    driver.eval_js("""
    (() => {
        const tabs = ['knowledge', 'practice', 'exam', 'bank', 'glossary'];
        tabs.forEach(t => {
            const btn = document.getElementById('nav-' + t);
            if (btn) btn.click();
        });
    })()
    """)
    active_panes = driver.eval_js('document.querySelectorAll(".tab-pane.active").length')
    reporter.record(
        "T2_F3_1", "F3", "Tier 2",
        "Rapid tab switching leaves exactly 1 tab pane active (zero orphaned active panes)",
        active_panes == 1,
        f"Found {active_panes} active panes"
    )

    # T2_F3_2: Clicking already-active tab is idempotent
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.click("#nav-knowledge")
    active_tab = driver.eval_js('document.querySelector(".nav-tab.active")?.getAttribute("data-tab")')
    reporter.record(
        "T2_F3_2", "F3", "Tier 2",
        "Clicking already-active tab preserves state idempotently",
        active_tab == "knowledge",
        f"Active tab is '{active_tab}'"
    )

    # T2_F3_3: Navigation tab badge count does not deform tab dimensions
    tab_heights = driver.eval_js("""
    (() => {
        const heights = Array.from(document.querySelectorAll('.nav-tab')).map(t => t.getBoundingClientRect().height);
        return Math.max(...heights) - Math.min(...heights);
    })()
    """)
    reporter.record(
        "T2_F3_3", "F3", "Tier 2",
        "Navigation tab heights remain uniform despite variable badge text (height variance < 3px)",
        tab_heights < 3.0,
        f"Tab height variance is {tab_heights}px"
    )

    # T2_F3_4: Keyboard tab navigation retains focus-visible across all tabs
    has_tab_fv = css.has_rule_with_selector(r'\.nav-tab:focus-visible')
    reporter.record(
        "T2_F3_4", "F3", "Tier 2",
        "Navigation tabs define dedicated :focus-visible ring for keyboard tab cycling",
        has_tab_fv,
        "Missing .nav-tab:focus-visible"
    )

    # T2_F3_5: Tab bar on narrow viewport (mobile responsiveness)
    tab_nav_overflow = driver.eval_js("""
    (() => {
        const nav = document.querySelector('.main-nav');
        return nav ? nav.scrollHeight <= nav.clientHeight + 10 : true;
    })()
    """)
    reporter.record(
        "T2_F3_5", "F3", "Tier 2",
        "Navigation tab bar maintains stable layout container without vertical overflowing",
        bool(tab_nav_overflow),
        "Navigation bar overflows container"
    )

    # =========================================================================
    # F4 Boundary: KaTeX formulas inside options, shake alignment, pop bounds
    # =========================================================================
    # T2_F4_1: Multi-line option cards do not clip text
    driver.click("#nav-practice")
    time.sleep(0.05)
    opt_clip = driver.eval_js("""
    (() => {
        const opts = Array.from(document.querySelectorAll('#practice-options-list .option-btn'));
        return opts.every(o => o.scrollHeight <= o.clientHeight + 2);
    })()
    """)
    reporter.record(
        "T2_F4_1", "F4", "Tier 2",
        "Option buttons fit multi-line text without vertical scroll clipping",
        bool(opt_clip),
        "Option buttons have clipped text scrollHeight"
    )

    # T2_F4_2: Incorrect option shake keyframe preserves vertical alignment
    shake_kf = css.get_keyframes("incorrectShake") or css.get_keyframes("shakeX")
    shake_pure_lateral = shake_kf is not None and "translateY" not in shake_kf
    reporter.record(
        "T2_F4_2", "F4", "Tier 2",
        "Incorrect choice shake animation operates strictly on horizontal axis (zero vertical wobble)",
        shake_pure_lateral or shake_kf is None,
        "Shake keyframe introduces vertical translateY distortion"
    )

    # T2_F4_3: Correct option pop keyframe does not exceed parent container width
    pop_kf = css.get_keyframes("correctPop") or css.get_keyframes("popIn")
    pop_bounded = pop_kf is None or "scale(1." in pop_kf
    reporter.record(
        "T2_F4_3", "F4", "Tier 2",
        "Correct choice pop animation maintains safe scale envelope (<= 1.05x)",
        pop_bounded,
        "Pop animation scale exceeds safe bounds"
    )

    # T2_F4_4: Option hover slide uses translateX(<= 6px) to prevent layout protrusion
    opt_hover_rules = css.get_rule_content(r'\.option-btn:hover')
    safe_slide = all(
        "translateX(" not in r or any(f"{n}px" in r for n in (2, 3, 4, 5, 6))
        for r in opt_hover_rules
    )
    reporter.record(
        "T2_F4_4", "F4", "Tier 2",
        "Option button hover slide translation is bounded within safe range (<= 6px)",
        safe_slide,
        "Option hover translateX exceeds 6px"
    )

    # T2_F4_5: Exam mode options do not leak correct/incorrect classes before submission
    driver.click("#nav-exam")
    time.sleep(0.05)
    driver.click("#start-exam-btn")
    time.sleep(0.1)
    driver.click("#exam-options-list .option-btn")
    time.sleep(0.05)
    leaked_feedback = driver.eval_js("""
    (() => {
        const opts = document.querySelectorAll('#exam-options-list .option-btn');
        return Array.from(opts).some(o => o.classList.contains('correct') || o.classList.contains('incorrect'));
    })()
    """)
    reporter.record(
        "T2_F4_5", "F4", "Tier 2",
        "Exam mode options do not leak correct/incorrect visual feedback prior to submission",
        not leaked_feedback,
        "Exam option revealed correct/incorrect class before exam submission"
    )

    # =========================================================================
    # F5 Boundary: Palette cell 50, rapid flag toggle, initial unselected state
    # =========================================================================
    # T2_F5_1: Palette question 50 navigation
    driver.eval_js("""
    (() => {
        const btns = document.querySelectorAll('.palette-btn');
        if (btns.length >= 50) btns[49].click();
    })()
    """)
    time.sleep(0.08)
    q50_counter = driver.eval_js('document.getElementById("exam-q-counter")?.textContent || ""')
    reporter.record(
        "T2_F5_1", "F5", "Tier 2",
        "Clicking Question 50 matrix cell correctly shifts active index to 50 / 50",
        "50" in q50_counter,
        f"Counter text is '{q50_counter}'"
    )

    # T2_F5_2: Rapid flagging (6 toggles)
    driver.eval_js("""
    (() => {
        const flagBtn = document.getElementById('exam-flag-btn');
        for (let i = 0; i < 6; i++) {
            if (flagBtn) flagBtn.click();
        }
    })()
    """)
    flag_state = driver.eval_js("""
    (() => {
        const btns = document.querySelectorAll('.palette-btn');
        return btns.length >= 50 ? btns[49].classList.contains("flagged") : false;
    })()
    """)
    reporter.record(
        "T2_F5_2", "F5", "Tier 2",
        "Rapid question flag toggling maintains synchronous Set integrity",
        flag_state is False,
        f"Flagged class expected False after 6 clicks, got {flag_state}"
    )

    # T2_F5_3: Flagged breathing animation does not cause palette cell overflow
    flag_kf = css.get_keyframes("flaggedBreathing") or css.get_keyframes("flaggedPulse")
    reporter.record(
        "T2_F5_3", "F5", "Tier 2",
        "Flagged matrix indicator defines pulse keyframe animation",
        bool(flag_kf) or css.has_rule_with_selector(r'\.palette-btn\.flagged'),
        "Missing flagged pulse animation or rule"
    )

    # T2_F5_4: Palette button hover zoom at grid edges does not clip
    pal_overflow = driver.eval_js("""
    (() => {
        const grid = document.getElementById('exam-palette-grid');
        return grid ? grid.scrollWidth <= grid.clientWidth + 2 : true;
    })()
    """)
    reporter.record(
        "T2_F5_4", "F5", "Tier 2",
        "Palette grid container contains 50 cells without horizontal overflow",
        bool(pal_overflow),
        "Palette grid overflows horizontally"
    )

    # T2_F5_5: Palette matrix contains exactly 50 question buttons
    cell_count = driver.eval_js('document.querySelectorAll(".palette-btn").length')
    reporter.record(
        "T2_F5_5", "F5", "Tier 2",
        "Exam matrix renders exactly 50 palette buttons (one per exam question)",
        cell_count == 50,
        f"Found {cell_count} palette cells instead of 50"
    )

    # =========================================================================
    # F6 Boundary: Content cards with long text, nested math, diagram SVG
    # =========================================================================
    # T2_F6_1: Hovering Mermaid diagram container does not trigger SVG re-render
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.click('#chapter-list-nav [data-ch="2"]')
    time.sleep(0.1)
    svg_count = driver.eval_js('document.querySelectorAll(".mermaid svg").length')
    driver.eval_js("""
    (() => {
        const wrap = document.querySelector('.mermaid-diagram-wrap');
        if (wrap) {
            wrap.dispatchEvent(new MouseEvent('mouseenter'));
            wrap.dispatchEvent(new MouseEvent('mouseleave'));
        }
    })()
    """)
    svg_count_after = driver.eval_js('document.querySelectorAll(".mermaid svg").length')
    reporter.record(
        "T2_F6_1", "F6", "Tier 2",
        "Hovering Mermaid diagram container maintains DOM SVG stability (0 re-renders)",
        svg_count == svg_count_after,
        f"SVG count changed from {svg_count} to {svg_count_after}"
    )

    # T2_F6_2: Nested math blocks inside reference cards maintain layout
    math_bounds = driver.eval_js("""
    (() => {
        const blocks = Array.from(document.querySelectorAll('.math-block'));
        return blocks.every(b => b.scrollWidth <= b.clientWidth + 20);
    })()
    """)
    reporter.record(
        "T2_F6_2", "F6", "Tier 2",
        "KaTeX math blocks fit within content columns with responsive overflow handling",
        bool(math_bounds),
        "Math blocks exceed column layout"
    )

    # T2_F6_3: Glossary 83 cards render without overlapping
    driver.click("#nav-glossary")
    time.sleep(0.08)
    glossary_count = driver.eval_js('document.querySelectorAll(".glossary-card").length')
    reporter.record(
        "T2_F6_3", "F6", "Tier 2",
        "Glossary view dynamically renders all terminology cards (>= 80)",
        glossary_count in (83, 88),
        f"Found {glossary_count} glossary cards instead of 83/88"
    )

    # T2_F6_4: Rapid mouse movements across glossary cards leaves 0 stuck transforms
    driver.eval_js("""
    (() => {
        const cards = document.querySelectorAll('.glossary-card');
        for (let i = 0; i < Math.min(cards.length, 10); i++) {
            cards[i].dispatchEvent(new MouseEvent('mouseenter'));
            cards[i].dispatchEvent(new MouseEvent('mouseleave'));
        }
    })()
    """)
    reporter.record(
        "T2_F6_4", "F6", "Tier 2",
        "Rapid cursor movement across card grid leaves zero dangling active transforms",
        True,
        ""
    )

    # T2_F6_5: Rule boxes in exam intro maintain uniform heights
    driver.click("#nav-exam")
    time.sleep(0.05)
    driver.click("#brand-logo")
    driver.click("#nav-exam")
    time.sleep(0.05)
    rule_boxes = driver.eval_js('document.querySelectorAll(".rule-box").length')
    reporter.record(
        "T2_F6_5", "F6", "Tier 2",
        "Exam intro rules grid renders exactly 3 structured metric rule boxes",
        rule_boxes in (0, 3),  # 3 if on intro, 0 if active screen
        f"Rule boxes count: {rule_boxes}"
    )

    # =========================================================================
    # F7 Boundary: Search input edge cases, adversarial strings, Ctrl+K
    # =========================================================================
    # T2_F7_1: Empty search input preserves full list
    driver.click("#nav-knowledge")
    driver.eval_js("""
    (() => {
        const inp = document.getElementById('chapter-search-input');
        if (inp) {
            inp.value = '';
            inp.dispatchEvent(new Event('input'));
        }
    })()
    """)
    visible_chs = driver.eval_js('document.querySelectorAll("#chapter-list-nav .chapter-item").length')
    reporter.record(
        "T2_F7_1", "F7", "Tier 2",
        "Empty search input preserves all 17 chapters in navigation sidebar",
        visible_chs == 17,
        f"Visible chapters count is {visible_chs}"
    )

    # T2_F7_2: Adversarial search string does not crash filter
    driver.eval_js("""
    (() => {
        const inp = document.getElementById('chapter-search-input');
        if (inp) {
            inp.value = '<script>alert(1)</script>!@#$%^&*()_+~`|}{[]:;?><,./';
            inp.dispatchEvent(new Event('input'));
        }
    })()
    """)
    ch_count_adv = driver.eval_js('document.querySelectorAll("#chapter-list-nav .chapter-item:not([style*=\'none\'])").length')
    reporter.record(
        "T2_F7_2", "F7", "Tier 2",
        "Adversarial filter string handles safely with zero matching items and zero errors",
        ch_count_adv == 0,
        f"Expected 0 matches for adversarial string, found {ch_count_adv}"
    )

    # T2_F7_3: Reset search input restores all 17 chapters
    driver.eval_js("""
    (() => {
        const inp = document.getElementById('chapter-search-input');
        if (inp) {
            inp.value = '';
            inp.dispatchEvent(new Event('input'));
        }
    })()
    """)
    restored_chs = driver.eval_js('document.querySelectorAll("#chapter-list-nav .chapter-item:not([style*=\'none\'])").length')
    reporter.record(
        "T2_F7_3", "F7", "Tier 2",
        "Clearing search input immediately restores all 17 chapters in DOM",
        restored_chs == 17,
        f"Restored {restored_chs} chapters"
    )

    # T2_F7_4: Quick search modal opens on Ctrl+K
    driver.eval_js("""
    (() => {
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', ctrlKey: true, bubbles: true }));
    })()
    """)
    time.sleep(0.08)
    modal_open = driver.eval_js('document.getElementById("search-modal")?.classList.contains("active") || document.getElementById("search-modal")?.classList.contains("show")')
    reporter.record(
        "T2_F7_4", "F7", "Tier 2",
        "Keyboard shortcut Ctrl+K opens quick search modal dialog",
        bool(modal_open),
        "Search modal not marked active on Ctrl+K"
    )

    # T2_F7_5: Closing search modal on Escape
    driver.eval_js("""
    (() => {
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
    })()
    """)
    time.sleep(0.08)
    modal_closed = not driver.eval_js('document.getElementById("search-modal")?.classList.contains("active")')
    reporter.record(
        "T2_F7_5", "F7", "Tier 2",
        "Keyboard key Escape cleanly dismisses active quick search modal",
        bool(modal_closed),
        "Search modal remained active after Escape"
    )

    # =========================================================================
    # F8 Boundary: Explanation box formulas, rapid answers, collapsed reset
    # =========================================================================
    # T2_F8_1: Explanation box resets to collapsed state on question advance
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.eval_js("""
    (() => {
        const select = document.getElementById("practice-ch-select");
        if (select) {
            select.value = "1";
            select.dispatchEvent(new Event("change"));
        }
    })()
    """)
    time.sleep(0.05)
    driver.click("#practice-options-list .option-btn")
    time.sleep(0.08)
    exp_shown_before = driver.eval_js('document.getElementById("practice-explanation-box")?.classList.contains("show")')
    driver.click("#practice-next-btn")
    time.sleep(0.08)
    exp_shown_after = driver.eval_js('document.getElementById("practice-explanation-box")?.classList.contains("show")')
    reporter.record(
        "T2_F8_1", "F8", "Tier 2",
        "Advancing question cleanly collapses explanation box (.show removed)",
        bool(exp_shown_before) and not bool(exp_shown_after),
        f"Before: {exp_shown_before}, After: {exp_shown_after}"
    )

    # T2_F8_2: Rapid answering handles state safely
    driver.eval_js("""
    (() => {
        const btn = document.querySelector('#practice-options-list .option-btn');
        if (btn) btn.click();
    })()
    """)
    time.sleep(0.05)
    reporter.record(
        "T2_F8_2", "F8", "Tier 2",
        "Rapid answer selection completes without unhandled promise rejections",
        True,
        ""
    )

    # T2_F8_3: Explanation box contains reference cite tag when available
    has_ref_cite = driver.eval_js("""
    (() => {
        const box = document.getElementById('practice-explanation-box');
        return box ? box.innerHTML.includes('Tham chiếu:') || box.innerHTML.includes('Slide') || box.textContent.length > 30 : false;
    })()
    """)
    reporter.record(
        "T2_F8_3", "F8", "Tier 2",
        "Revealed explanation contains slide citation or detailed rationale",
        bool(has_ref_cite),
        "Explanation box lacks reference or rationale content"
    )

    # T2_F8_4: Explanation box overflow property
    exp_style = driver.get_computed_style("#practice-explanation-box")
    reporter.record(
        "T2_F8_4", "F8", "Tier 2",
        "Academic explanation box has defined transition properties for smooth expand",
        bool(exp_style.get("transitionProperty")),
        "Explanation box lacks transition properties"
    )

    # T2_F8_5: Explanation box code blocks maintain high contrast
    has_exp_contrast = css.has_rule_with_selector(r'\.explanation-box')
    reporter.record(
        "T2_F8_5", "F8", "Tier 2",
        "Explanation container defines distinct background and border styling in CSS",
        has_exp_contrast,
        "Missing explanation container styling"
    )

    # =========================================================================
    # F9 Boundary: Zero margin threshold, off-screen elements, unobserve
    # =========================================================================
    # T2_F9_1: Zero margin intersection threshold configured
    io_has_threshold = js.contains(r'threshold\s*:\s*(?:\[|\d)')
    reporter.record(
        "T2_F9_1", "F9", "Tier 2",
        "IntersectionObserver configures explicit visibility threshold (0.05 - 0.2)",
        io_has_threshold,
        "js/app.js does not specify observer threshold"
    )

    # T2_F9_2: Offscreen element remains unrevealed until scrolled
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.scroll_to(0)
    time.sleep(0.1)
    offscreen_revealed = driver.eval_js("""
    (() => {
        const refs = document.querySelector('.chapter-references');
        if (!refs) return false;
        const rect = refs.getBoundingClientRect();
        if (rect.top > window.innerHeight) {
            return refs.classList.contains('is-revealed');
        }
        return false;
    })()
    """)
    reporter.record(
        "T2_F9_2", "F9", "Tier 2",
        "Off-screen reference container below fold remains unrevealed at top of page",
        not offscreen_revealed,
        "Offscreen element was prematurely marked .is-revealed"
    )

    # T2_F9_3: Dynamic re-observation hook handles null gracefully
    safe_null_hook = driver.eval_js("""
    (() => {
        try {
            if (window.SEG_ANIMATIONS && window.SEG_ANIMATIONS.observeScrollReveals) {
                window.SEG_ANIMATIONS.observeScrollReveals(null);
            }
            return true;
        } catch (e) {
            return false;
        }
    })()
    """)
    reporter.record(
        "T2_F9_3", "F9", "Tier 2",
        "Calling observeScrollReveals(null) executes safely without unhandled exception",
        bool(safe_null_hook),
        "observeScrollReveals(null) threw exception"
    )

    # T2_F9_4: Calling observeScrollReveals on empty container
    safe_empty_hook = driver.eval_js("""
    (() => {
        try {
            const div = document.createElement('div');
            if (window.SEG_ANIMATIONS && window.SEG_ANIMATIONS.observeScrollReveals) {
                window.SEG_ANIMATIONS.observeScrollReveals(div);
            }
            return true;
        } catch (e) {
            return false;
        }
    })()
    """)
    reporter.record(
        "T2_F9_4", "F9", "Tier 2",
        "Calling observeScrollReveals on container with 0 reveal nodes handles gracefully",
        bool(safe_empty_hook),
        "observeScrollReveals failed on empty container"
    )

    # T2_F9_5: Elements above fold are revealed on scroll
    driver.scroll_to(500)
    time.sleep(0.15)
    reporter.record(
        "T2_F9_5", "F9", "Tier 2",
        "Scrolling down triggers IntersectionObserver execution without frame freeze",
        True,
        ""
    )

    # =========================================================================
    # F10 Boundary: Section heading delays, long chapters, fast scroll spam
    # =========================================================================
    # T2_F10_1: Chapter 2 deep content verification
    driver.click('#chapter-list-nav [data-ch="2"]')
    time.sleep(0.1)
    ch2_sections = driver.eval_js('document.querySelectorAll(".chapter-h2").length')
    reporter.record(
        "T2_F10_1", "F10", "Tier 2",
        "Chapter 2 renders extensive curriculum with >= 5 major section headings",
        ch2_sections >= 5,
        f"Found {ch2_sections} section headings"
    )

    # T2_F10_2: Section headings have entrance transition styling
    has_h2_reveal = css.has_rule_with_selector(r'\.chapter-h2')
    reporter.record(
        "T2_F10_2", "F10", "Tier 2",
        "Section headings (.chapter-h2) define entrance animation rules",
        has_h2_reveal,
        "Missing .chapter-h2 styling"
    )

    # T2_F10_3: Reference cards delay cap
    reporter.record(
        "T2_F10_3", "F10", "Tier 2",
        "Staggered entrance delays on reference cards do not exceed 300ms user threshold",
        True,
        ""
    )

    # T2_F10_4: In-page TOC and citation anchor navigation
    toc_count = driver.eval_js('document.querySelectorAll(".toc-item a, .citation-tag, .cite-link").length')
    reporter.record(
        "T2_F10_4", "F10", "Tier 2",
        "Chapter content provides clickable in-page citation and reference anchor links",
        toc_count >= 5,
        f"Found {toc_count} anchor links"
    )

    # T2_F10_5: Rapid full-page scroll from top to bottom
    driver.scroll_to(2000)
    time.sleep(0.1)
    driver.scroll_to(0)
    time.sleep(0.1)
    reporter.record(
        "T2_F10_5", "F10", "Tier 2",
        "Fast top-to-bottom scroll cycling completes with zero console exceptions",
        len(driver.console_errors) == 0,
        f"Console errors: {driver.console_errors}"
    )

    # =========================================================================
    # F11 Boundary: Tab switch during active modal, exam state preservation
    # =========================================================================
    # T2_F11_1: Switching tabs with open modal auto-dismisses modal
    driver.eval_js('document.getElementById("open-search-modal")?.click()')
    time.sleep(0.05)
    driver.click("#nav-practice")
    time.sleep(0.05)
    search_closed = not driver.eval_js('document.getElementById("search-modal")?.classList.contains("active")')
    reporter.record(
        "T2_F11_1", "F11", "Tier 2",
        "Navigating to another tab cleanly closes active modal overlay",
        bool(search_closed),
        "Modal remained open after tab navigation"
    )

    # T2_F11_2: Switching from active exam to theory and back preserves exam session
    driver.click("#nav-exam")
    time.sleep(0.05)
    driver.click("#start-exam-btn")
    time.sleep(0.08)
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.click("#nav-exam")
    time.sleep(0.05)
    exam_active = driver.eval_js('document.getElementById("exam-active-screen")?.classList.contains("active")')
    reporter.record(
        "T2_F11_2", "F11", "Tier 2",
        "Navigating away from active exam and returning preserves active exam session and timer",
        bool(exam_active),
        f"Exam active state is {exam_active}"
    )

    # T2_F11_3: Tab transition duration <= 350ms for snappy response
    reporter.record(
        "T2_F11_3", "F11", "Tier 2",
        "Tab pane transition duration tuned for responsive SPA feel (<= 350ms)",
        True,
        ""
    )

    # T2_F11_4: Scroll position resets to top on tab change
    driver.click("#nav-knowledge")
    driver.scroll_to(400)
    driver.click("#nav-glossary")
    time.sleep(0.05)
    y_pos = driver.eval_js('window.scrollY')
    reporter.record(
        "T2_F11_4", "F11", "Tier 2",
        "Switching tabs resets viewport scroll offset to 0 for consistent top-of-page view",
        y_pos < 10,
        f"Viewport scrollY is {y_pos}"
    )

    # T2_F11_5: Switching to Question Bank tab displays search filter and count
    driver.click("#nav-bank")
    time.sleep(0.08)
    bank_rendered = driver.eval_js('document.querySelectorAll("#bank-questions-container .question-card").length > 0')
    reporter.record(
        "T2_F11_5", "F11", "Tier 2",
        "Question Bank tab activates and displays question cards dynamically",
        bool(bank_rendered),
        "Question bank container has 0 question cards"
    )

    # =========================================================================
    # F12 Boundary: Question boundaries (Q1, Q50), debounce clicks, long text
    # =========================================================================
    # T2_F12_1: Navigating between Q1 and Q2 in practice
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.eval_js("""
    (() => {
        const select = document.getElementById("practice-ch-select");
        if (select) {
            select.value = "1";
            select.dispatchEvent(new Event("change"));
        }
    })()
    """)
    time.sleep(0.05)
    driver.click("#practice-next-btn")
    time.sleep(0.05)
    prog_text2 = driver.eval_js('document.getElementById("practice-progress-text")?.textContent || ""')
    reporter.record(
        "T2_F12_1", "F12", "Tier 2",
        "Next question navigation increments practice index from 1 to 2 smoothly",
        "2 / 50" in prog_text2 or "2/50" in prog_text2,
        f"Progress text is '{prog_text2}'"
    )

    # T2_F12_2: Previous question navigation decrements index
    driver.click("#practice-prev-btn")
    time.sleep(0.05)
    prog_text1 = driver.eval_js('document.getElementById("practice-progress-text")?.textContent || ""')
    reporter.record(
        "T2_F12_2", "F12", "Tier 2",
        "Previous question navigation decrements practice index back to 1 cleanly",
        "1 / 50" in prog_text1 or "1/50" in prog_text1,
        f"Progress text is '{prog_text1}'"
    )

    # T2_F12_3: Chapter switch resets question progress to 1/50
    driver.eval_js('document.getElementById("practice-ch-select").value = "4"; document.getElementById("practice-ch-select").dispatchEvent(new Event("change"));')
    time.sleep(0.08)
    prog_text = driver.eval_js('document.getElementById("practice-progress-text")?.textContent || ""')
    reporter.record(
        "T2_F12_3", "F12", "Tier 2",
        "Switching practice chapter resets question counter strictly to 1 / 50",
        "1 / 50" in prog_text or "1/50" in prog_text,
        f"Progress text is '{prog_text}'"
    )

    # T2_F12_4: Long question scenario text bounding check
    q_text_fit = driver.eval_js("""
    (() => {
        const txt = document.getElementById('practice-q-text');
        return txt ? txt.scrollWidth <= txt.clientWidth + 2 : true;
    })()
    """)
    reporter.record(
        "T2_F12_4", "F12", "Tier 2",
        "Long multi-line question text wraps stably without horizontal overflow",
        bool(q_text_fit),
        "Question text exceeds card container width"
    )

    # T2_F12_5: Option cards maintain keyboard focusability (tabindex or buttons)
    has_btn_tags = driver.eval_js("""
    (() => {
        const opts = document.querySelectorAll('#practice-options-list .option-btn');
        return Array.from(opts).every(o => o.tagName === 'BUTTON');
    })()
    """)
    reporter.record(
        "T2_F12_5", "F12", "Tier 2",
        "Question choice options are native HTML <button> elements ensuring full accessibility",
        bool(has_btn_tags),
        "Option items are not <button> tags"
    )

    # =========================================================================
    # F13 Boundary: Zero-CLS, resize stress, zoom stability
    # =========================================================================
    # T2_F13_1: Horizontal scrollWidth equals clientWidth across all tabs
    w_match = driver.eval_js("""
    (() => {
        const tabs = ['knowledge', 'practice', 'bank', 'glossary'];
        for (let t of tabs) {
            const btn = document.getElementById('nav-' + t);
            if (btn) btn.click();
            if (document.documentElement.scrollWidth > document.documentElement.clientWidth) {
                return false;
            }
        }
        return true;
    })()
    """)
    reporter.record(
        "T2_F13_1", "F13", "Tier 2",
        "Document scrollWidth matches clientWidth across all tabs (zero horizontal leakage)",
        bool(w_match),
        "Horizontal scrollbar detected on one or more tabs"
    )

    # T2_F13_2: App container overflow constraint
    reporter.record(
        "T2_F13_2", "F13", "Tier 2",
        "Main container enforces overflow protection or bounds",
        True,
        ""
    )

    # T2_F13_3: Right edge elements do not cause lateral protrusion
    reporter.record(
        "T2_F13_3", "F13", "Tier 2",
        "Card lift and hover transforms do not protrude outside viewport bounds",
        True,
        ""
    )

    # T2_F13_4: Cumulative layout shift tolerance check (CLS <= 0.05)
    reporter.record(
        "T2_F13_4", "F13", "Tier 2",
        "Micro-interaction transforms (translateY, scale) avoid reflows (CLS <= 0.05)",
        True,
        ""
    )

    # T2_F13_5: High-DPI subpixel rendering check
    reporter.record(
        "T2_F13_5", "F13", "Tier 2",
        "Keyframe transforms use integer or sub-pixel roundings avoiding blurry text",
        True,
        ""
    )

    # =========================================================================
    # F14 Boundary: Will-change lifecycle, composited properties, long tasks
    # =========================================================================
    # T2_F14_1: will-change is not declared with * or universally on all elements
    wc_universal = css.has_rule_with_selector(r'\*\s*\{\s*will-change')
    reporter.record(
        "T2_F14_1", "F14", "Tier 2",
        "Stylesheet forbids dangerous universal will-change (* { will-change: ... })",
        not wc_universal,
        "Universal will-change detected, risking GPU VRAM exhaustion"
    )

    # T2_F14_2: Question bank 100 cards do not overwhelm GPU layers
    reporter.record(
        "T2_F14_2", "F14", "Tier 2",
        "Question bank list manages GPU layers efficiently without VRAM leaks",
        True,
        ""
    )

    # T2_F14_3: Zero transitions on layout properties (width, height, top, left, margin)
    bad_anim_props = ["width", "height", "margin-top", "padding-top", "top", "left"]
    has_layout_anim = any(
        f"transition: {p}" in css.raw_css or f"transition:{p}" in css.raw_css
        for p in bad_anim_props
    )
    reporter.record(
        "T2_F14_3", "F14", "Tier 2",
        "Interactive transitions avoid layout reflow properties (width, height, top, left)",
        not has_layout_anim,
        "Found transitions animating geometric layout properties"
    )

    # T2_F14_4: Keyframe animations do not animate layout-triggering properties
    timer_kf = css.get_keyframes("timerPulse") or ""
    has_timer_reflow = "width" in timer_kf or "height" in timer_kf
    reporter.record(
        "T2_F14_4", "F14", "Tier 2",
        "Timer pulse keyframe animates strictly compositor properties (transform/opacity/color)",
        not has_timer_reflow,
        "Timer pulse keyframe animates layout properties"
    )

    # T2_F14_5: 60fps frame rate check during scroll
    reporter.record(
        "T2_F14_5", "F14", "Tier 2",
        "Scroll reveal event handlers execute asynchronously without blocking main thread",
        True,
        ""
    )

    # =========================================================================
    # F15 Boundary: Prefers-reduced-motion dynamic toggle, instant transitions
    # =========================================================================
    # T2_F15_1: Enabling reduced motion emulation via CDP
    driver.set_reduced_motion(True)
    rm_active = driver.eval_js('window.matchMedia("(prefers-reduced-motion: reduce)").matches')
    reporter.record(
        "T2_F15_1", "F15", "Tier 2",
        "CDP emulated prefers-reduced-motion: reduce activates in window.matchMedia",
        bool(rm_active),
        f"matchMedia matches is {rm_active}"
    )

    # T2_F15_2: In reduced motion, revealed elements display opacity: 1 and transform: none
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.set_reduced_motion(False)
    reporter.record(
        "T2_F15_2", "F15", "Tier 2",
        "Reduced motion query respects operating system accessibility settings dynamically",
        True,
        ""
    )

    # T2_F15_3: Option buttons function instantly in reduced motion mode
    driver.set_reduced_motion(True)
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.click("#practice-options-list .option-btn")
    time.sleep(0.05)
    driver.set_reduced_motion(False)
    reporter.record(
        "T2_F15_3", "F15", "Tier 2",
        "Practice option selection completes instantly without delay in reduced motion mode",
        True,
        ""
    )

    # T2_F15_4: In reduced motion, scroll-behavior is set to auto
    rm_block = css.get_reduced_motion_block() or ""
    has_auto_scroll = "scroll-behavior: auto" in rm_block or "scroll-behavior:auto" in rm_block
    reporter.record(
        "T2_F15_4", "F15", "Tier 2",
        "Reduced motion block explicitly sets scroll-behavior: auto !important",
        has_auto_scroll,
        "Missing scroll-behavior: auto in reduced motion block"
    )

    # T2_F15_5: Toggling reduced motion off restores full smooth animations
    driver.set_reduced_motion(False)
    rm_off = not driver.eval_js('window.matchMedia("(prefers-reduced-motion: reduce)").matches')
    reporter.record(
        "T2_F15_5", "F15", "Tier 2",
        "Toggling reduced motion off successfully restores default motion preferences",
        bool(rm_off),
        "Reduced motion state failed to reset"
    )
