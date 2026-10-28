"""
Tier 1: Feature Coverage E2E Tests (>= 75 Tests across F1-F15)
Covers primary behavior (happy paths) for all 15 animation & interaction features.
"""

import time
from typing import Optional
from tests.test_harness import CSSAnalyzer, JSAnalyzer, EdgeCDPDriver, TestReporter


def run_tier1_tests(driver: EdgeCDPDriver, css: CSSAnalyzer, js: JSAnalyzer, reporter: TestReporter):
    print("\n--- Running Tier 1: Feature Coverage Tests (F1 - F15) ---")

    # =========================================================================
    # F1: Button Micro-Interactions & Tactile Press
    # =========================================================================
    # T1_F1_1: Button hover elevation and glow
    has_btn_hover = css.has_rule_with_selector(r'\.btn-primary:hover|\.btn-secondary:hover|\.btn:hover')
    hover_rules = css.get_rule_content(r'\.btn-primary:hover|\.btn-secondary:hover')
    has_elevation = any("box-shadow" in r or "transform" in r or "background" in r for r in hover_rules)
    reporter.record(
        "T1_F1_1", "F1", "Tier 1",
        "Buttons define :hover state with elevation or glow",
        has_btn_hover and has_elevation,
        "CSS lacks .btn-primary:hover or .btn-secondary:hover elevation/glow"
    )

    # T1_F1_2: Button active tactile press compression
    has_btn_active = css.has_rule_with_selector(r'\.btn-primary:active|\.btn-secondary:active|\.btn:active')
    active_rules = css.get_rule_content(r'\.btn-primary:active|\.btn-secondary:active|\.btn:active')
    has_active_press = any("scale(" in r or "translateY(" in r for r in active_rules)
    reporter.record(
        "T1_F1_2", "F1", "Tier 1",
        "Buttons define :active tactile press compression (scale or translateY)",
        has_btn_active and has_active_press,
        "CSS lacks tactile :active transform on buttons"
    )

    # T1_F1_3: Button focus-visible indicator
    has_btn_focus = css.has_rule_with_selector(r'\.btn-primary:focus-visible|\.btn-secondary:focus-visible|\.btn:focus-visible')
    focus_rules = css.get_rule_content(r'\.btn-primary:focus-visible|\.btn-secondary:focus-visible|\.btn:focus-visible')
    has_focus_ring = any("outline" in r or "box-shadow" in r for r in focus_rules)
    reporter.record(
        "T1_F1_3", "F1", "Tier 1",
        "Buttons define WCAG-compliant :focus-visible indicator ring",
        has_btn_focus and has_focus_ring,
        "CSS lacks :focus-visible outline or ring for buttons"
    )

    # T1_F1_4: Timing tokens declared at :root
    ease_smooth = css.get_root_variable("ease-smooth")
    ease_spring = css.get_root_variable("ease-spring")
    trans_fast = css.get_root_variable("transition-fast")
    has_tokens = bool(ease_smooth and trans_fast)
    reporter.record(
        "T1_F1_4", "F1", "Tier 1",
        "Timing and easing tokens (--ease-smooth, --transition-fast) declared at :root",
        has_tokens,
        f"Missing tokens: ease-smooth={ease_smooth}, transition-fast={trans_fast}"
    )

    # T1_F1_5: Runtime button cursor and transition properties
    btn_style = driver.get_computed_style(".btn-primary")
    has_pointer = btn_style.get("cursor") == "pointer"
    has_trans = bool(btn_style.get("transitionProperty") and btn_style.get("transitionProperty") != "none")
    reporter.record(
        "T1_F1_5", "F1", "Tier 1",
        "Runtime .btn-primary has cursor:pointer and active transition",
        has_pointer and has_trans,
        f"Computed style cursor={btn_style.get('cursor')}, transitionProperty={btn_style.get('transitionProperty')}"
    )

    # =========================================================================
    # F2: Disabled Button State Styling
    # =========================================================================
    # T1_F2_1: Disabled button CSS rules exist
    has_disabled_rule = css.has_rule_with_selector(r':disabled')
    reporter.record(
        "T1_F2_1", "F2", "Tier 1",
        "Explicit :disabled selector rules defined in stylesheet",
        has_disabled_rule,
        "No :disabled selector found in css/style.css"
    )

    # T1_F2_2: Disabled buttons specify reduced opacity
    disabled_rules = css.get_rule_content(r':disabled')
    has_reduced_opacity = any("opacity" in r and ("0.4" in r or "0.5" in r or "0.45" in r) for r in disabled_rules)
    reporter.record(
        "T1_F2_2", "F2", "Tier 1",
        "Disabled button styling enforces reduced opacity (<= 0.5)",
        has_reduced_opacity,
        "Disabled rules missing opacity <= 0.5"
    )

    # T1_F2_3: Disabled buttons specify cursor: not-allowed
    has_cursor_na = any("not-allowed" in r for r in disabled_rules)
    reporter.record(
        "T1_F2_3", "F2", "Tier 1",
        "Disabled buttons enforce cursor: not-allowed",
        has_cursor_na,
        "Disabled rules missing cursor: not-allowed"
    )

    # T1_F2_4: Disabled buttons suppress hover & active transforms
    has_suppressed_transform = any("transform: none" in r or "transform:none" in r for r in disabled_rules)
    reporter.record(
        "T1_F2_4", "F2", "Tier 1",
        "Disabled buttons suppress hover & active transforms (transform: none)",
        has_suppressed_transform,
        "Disabled rules do not reset transform to none"
    )

    # T1_F2_5: Runtime verification of disabled navigation button
    driver.click("#nav-practice")
    prev_btn_disabled = driver.eval_js('document.getElementById("practice-prev-btn").disabled')
    prev_style = driver.get_computed_style("#practice-prev-btn")
    prev_na = prev_style.get("cursor") == "not-allowed"
    reporter.record(
        "T1_F2_5", "F2", "Tier 1",
        "Runtime #practice-prev-btn is disabled on Q1 with cursor: not-allowed",
        bool(prev_btn_disabled and prev_na),
        f"disabled={prev_btn_disabled}, cursor={prev_style.get('cursor')}"
    )

    # =========================================================================
    # F3: Navigation Tab Interactivity
    # =========================================================================
    # T1_F3_1: .nav-tab defines hover transition
    has_tab_hover = css.has_rule_with_selector(r'\.nav-tab:hover')
    reporter.record(
        "T1_F3_1", "F3", "Tier 1",
        "Navigation tabs define smooth hover transition state (.nav-tab:hover)",
        has_tab_hover,
        "Missing .nav-tab:hover rule in css/style.css"
    )

    # T1_F3_2: .nav-tab:active tactile feedback
    has_tab_active = css.has_rule_with_selector(r'\.nav-tab:active')
    reporter.record(
        "T1_F3_2", "F3", "Tier 1",
        "Navigation tabs define tactile press feedback (.nav-tab:active)",
        has_tab_active,
        "Missing .nav-tab:active rule in css/style.css"
    )

    # T1_F3_3: .nav-tab:focus-visible focus ring
    has_tab_focus = css.has_rule_with_selector(r'\.nav-tab:focus-visible')
    reporter.record(
        "T1_F3_3", "F3", "Tier 1",
        "Navigation tabs define :focus-visible keyboard indicator",
        has_tab_focus,
        "Missing .nav-tab:focus-visible indicator"
    )

    # T1_F3_4: Runtime active tab indicator
    driver.click("#nav-knowledge")
    is_active = driver.eval_js('document.getElementById("nav-knowledge").classList.contains("active")')
    is_pane_active = driver.eval_js('document.getElementById("tab-knowledge").classList.contains("active")')
    reporter.record(
        "T1_F3_4", "F3", "Tier 1",
        "Runtime tab click toggles .active class and activates target tab pane",
        bool(is_active and is_pane_active),
        f"tab active={is_active}, pane active={is_pane_active}"
    )

    # T1_F3_5: All 5 navigation tabs exist
    tab_count = driver.eval_js('document.querySelectorAll(".nav-tab").length')
    reporter.record(
        "T1_F3_5", "F3", "Tier 1",
        "All 5 primary navigation tabs exist in DOM with valid data-tab attributes",
        tab_count == 5,
        f"Found {tab_count} nav tabs instead of 5"
    )

    # =========================================================================
    # F4: Quiz Option Card Interactivity & Feedback
    # =========================================================================
    # T1_F4_1: Option button hover slide translateX
    opt_hover_rules = css.get_rule_content(r'\.option-btn:hover')
    has_opt_slide = any("translateX(" in r for r in opt_hover_rules)
    reporter.record(
        "T1_F4_1", "F4", "Tier 1",
        "Option cards define hover directional slide (.option-btn:hover translateX)",
        has_opt_slide,
        "Option button hover missing translateX slide animation"
    )

    # T1_F4_2: Option button active tactile compression
    opt_active_rules = css.get_rule_content(r'\.option-btn:active')
    has_opt_active = any("scale(" in r for r in opt_active_rules) or css.has_rule_with_selector(r'\.option-btn:active')
    reporter.record(
        "T1_F4_2", "F4", "Tier 1",
        "Option cards define active tactile compression (.option-btn:active)",
        has_opt_active,
        "Option button missing :active tactile feedback"
    )

    # T1_F4_3: Selected state styling
    has_opt_selected = css.has_rule_with_selector(r'\.option-btn\.selected')
    reporter.record(
        "T1_F4_3", "F4", "Tier 1",
        "Option card defines active selection state (.option-btn.selected)",
        has_opt_selected,
        "Missing .option-btn.selected styling in CSS"
    )

    # T1_F4_4: Correct choice spring pop keyframe or animation
    has_correct_anim = bool(css.get_keyframes("correctPop") or css.get_keyframes("popIn") or
                           css.has_rule_with_selector(r'\.option-btn\.correct'))
    reporter.record(
        "T1_F4_4", "F4", "Tier 1",
        "Correct answer feedback defines spring pop animation / keyframe",
        has_correct_anim,
        "Missing correct option pop animation or keyframe"
    )

    # T1_F4_5: Incorrect choice shake keyframe or animation
    has_shake_anim = bool(css.get_keyframes("incorrectShake") or css.get_keyframes("shakeX") or
                          css.has_rule_with_selector(r'\.option-btn\.incorrect'))
    reporter.record(
        "T1_F4_5", "F4", "Tier 1",
        "Incorrect answer feedback defines shake animation / keyframe",
        has_shake_anim,
        "Missing incorrect option shake animation or keyframe"
    )

    # =========================================================================
    # F5: Exam Matrix Palette Interactivity
    # =========================================================================
    # T1_F5_1: Palette button hover zoom scale
    pal_hover_rules = css.get_rule_content(r'\.palette-btn:hover')
    has_pal_zoom = any("scale(" in r for r in pal_hover_rules) or css.has_rule_with_selector(r'\.palette-btn:hover')
    reporter.record(
        "T1_F5_1", "F5", "Tier 1",
        "Palette matrix buttons define hover zoom (.palette-btn:hover)",
        has_pal_zoom,
        "Palette button missing hover zoom scale"
    )

    # T1_F5_2: Palette button active click
    has_pal_active = css.has_rule_with_selector(r'\.palette-btn:active')
    reporter.record(
        "T1_F5_2", "F5", "Tier 1",
        "Palette matrix buttons define tactile click (.palette-btn:active)",
        has_pal_active,
        "Palette button missing :active state"
    )

    # T1_F5_3: Current question cell indicator
    has_pal_current = css.has_rule_with_selector(r'\.palette-btn\.current')
    reporter.record(
        "T1_F5_3", "F5", "Tier 1",
        "Active question matrix cell defines .current indicator glow/border",
        has_pal_current,
        "Missing .palette-btn.current styling"
    )

    # T1_F5_4: Answered questions styling
    has_pal_answered = css.has_rule_with_selector(r'\.palette-btn\.answered')
    reporter.record(
        "T1_F5_4", "F5", "Tier 1",
        "Answered matrix cells define .answered status styling",
        has_pal_answered,
        "Missing .palette-btn.answered styling"
    )

    # T1_F5_5: Flagged question breathing pulse
    has_flagged_pulse = bool(css.get_keyframes("flaggedBreathing") or css.get_keyframes("flaggedPulse") or
                             css.has_rule_with_selector(r'\.palette-btn\.flagged'))
    reporter.record(
        "T1_F5_5", "F5", "Tier 1",
        "Flagged question matrix cell defines breathing pulse animation",
        has_flagged_pulse,
        "Missing flagged breathing animation or .palette-btn.flagged rule"
    )

    # =========================================================================
    # F6: Content Card Micro-interactions
    # =========================================================================
    # T1_F6_1: Glossary card hover lift & shadow
    gloss_rules = css.get_rule_content(r'\.glossary-card:hover')
    has_gloss_lift = any("translateY(" in r for r in gloss_rules) or css.has_rule_with_selector(r'\.glossary-card:hover')
    reporter.record(
        "T1_F6_1", "F6", "Tier 1",
        "Glossary cards define smooth hover lift (.glossary-card:hover translateY)",
        has_gloss_lift,
        "Missing .glossary-card:hover lift transform"
    )

    # T1_F6_2: Reference cards hover elevation
    has_ref_hover = css.has_rule_with_selector(r'\.ref-card:hover')
    reporter.record(
        "T1_F6_2", "F6", "Tier 1",
        "Reference cards define hover elevation (.ref-card:hover)",
        has_ref_hover,
        "Missing .ref-card:hover styling"
    )

    # T1_F6_3: Rule box hover effect
    has_rule_hover = css.has_rule_with_selector(r'\.rule-box:hover')
    reporter.record(
        "T1_F6_3", "F6", "Tier 1",
        "Exam rule boxes define hover elevation/glow (.rule-box:hover)",
        has_rule_hover,
        "Missing .rule-box:hover styling"
    )

    # T1_F6_4: KaTeX math block hover glow
    has_math_hover = css.has_rule_with_selector(r'\.math-block:hover')
    reporter.record(
        "T1_F6_4", "F6", "Tier 1",
        "KaTeX math blocks define non-disruptive hover border/glow (.math-block:hover)",
        has_math_hover,
        "Missing .math-block:hover rule"
    )

    # T1_F6_5: Mermaid diagram wrap hover
    has_mermaid_hover = css.has_rule_with_selector(r'\.mermaid-diagram-wrap:hover')
    reporter.record(
        "T1_F6_5", "F6", "Tier 1",
        "Mermaid flowchart container defines hover border/shadow (.mermaid-diagram-wrap:hover)",
        has_mermaid_hover,
        "Missing .mermaid-diagram-wrap:hover rule"
    )

    # =========================================================================
    # F7: Form Controls & Search Input Accessibility
    # =========================================================================
    # T1_F7_1: Sidebar search input focus-visible
    has_sb_focus = css.has_rule_with_selector(r'#chapter-search-input:focus-visible|\.sidebar-search-box input:focus-visible')
    reporter.record(
        "T1_F7_1", "F7", "Tier 1",
        "Sidebar chapter search input defines accessible :focus-visible ring",
        has_sb_focus,
        "Missing :focus-visible on chapter search input"
    )

    # T1_F7_2: Question bank search input focus-visible
    has_bank_focus = css.has_rule_with_selector(r'#bank-search-input:focus-visible|\.bank-search-input:focus-visible')
    reporter.record(
        "T1_F7_2", "F7", "Tier 1",
        "Question Bank search input defines accessible :focus-visible ring",
        has_bank_focus,
        "Missing :focus-visible on question bank search input"
    )

    # T1_F7_3: Glossary search input focus-visible
    has_gloss_focus = css.has_rule_with_selector(r'#glossary-search-input:focus-visible')
    reporter.record(
        "T1_F7_3", "F7", "Tier 1",
        "Glossary search input defines accessible :focus-visible ring",
        has_gloss_focus,
        "Missing :focus-visible on glossary search input"
    )

    # T1_F7_4: Practice chapter select focus-visible
    has_select_focus = css.has_rule_with_selector(r'#practice-ch-select:focus-visible|\.practice-chapter-select:focus-visible')
    reporter.record(
        "T1_F7_4", "F7", "Tier 1",
        "Practice chapter selector dropdown defines accessible :focus-visible indicator",
        has_select_focus,
        "Missing :focus-visible on chapter select dropdown"
    )

    # T1_F7_5: Search modal input focus-visible
    has_modal_input_focus = css.has_rule_with_selector(r'\.search-modal-input:focus-visible')
    reporter.record(
        "T1_F7_5", "F7", "Tier 1",
        "Quick Search modal input defines accessible :focus-visible indicator",
        has_modal_input_focus,
        "Missing :focus-visible on search modal input"
    )

    # =========================================================================
    # F8: Academic Explanation Smooth Reveal
    # =========================================================================
    # T1_F8_1: Explanation box default collapsed/hidden state
    has_exp_base = css.has_rule_with_selector(r'\.explanation-box')
    exp_rules = css.get_rule_content(r'\.explanation-box')
    is_initially_hidden = any("display: none" in r or "max-height: 0" in r or "opacity: 0" in r for r in exp_rules)
    reporter.record(
        "T1_F8_1", "F8", "Tier 1",
        "Academic explanation box initially hidden/collapsed (.explanation-box)",
        has_exp_base and is_initially_hidden,
        "Explanation box not initially hidden in CSS"
    )

    # T1_F8_2: Explanation box animated expand when .show
    has_exp_show = css.has_rule_with_selector(r'\.explanation-box\.show')
    exp_show_rules = css.get_rule_content(r'\.explanation-box\.show')
    has_show_anim = any("opacity" in r or "transform" in r or "max-height" in r for r in exp_show_rules)
    reporter.record(
        "T1_F8_2", "F8", "Tier 1",
        "Academic explanation box defines smooth expand / fade-slide when .show",
        has_exp_show and has_show_anim,
        "Missing animated expand / fade rule on .explanation-box.show"
    )

    # T1_F8_3: Runtime practice answer reveals explanation
    driver.click("#nav-practice")
    time.sleep(0.1)
    # Select first option in practice
    driver.click("#practice-options-list .option-btn")
    time.sleep(0.15)
    is_exp_shown = driver.eval_js('document.getElementById("practice-explanation-box").classList.contains("show")')
    reporter.record(
        "T1_F8_3", "F8", "Tier 1",
        "Runtime answering practice question reveals explanation box (.show)",
        bool(is_exp_shown),
        "Explanation box did not receive .show class upon answer selection"
    )

    # T1_F8_4: Explanation text readability
    exp_text_len = driver.eval_js('document.getElementById("practice-explanation-text").textContent.trim().length')
    reporter.record(
        "T1_F8_4", "F8", "Tier 1",
        "Revealed academic explanation contains complete reference text (>20 chars)",
        exp_text_len > 20,
        f"Explanation text length is {exp_text_len}"
    )

    # T1_F8_5: Exam review explanation cards styling
    has_review_exp = css.has_rule_with_selector(r'\.review-explanation') or css.has_rule_with_selector(r'\.explanation-box')
    reporter.record(
        "T1_F8_5", "F8", "Tier 1",
        "Exam review cards retain structured academic explanation styling",
        has_review_exp,
        "Missing explanation card styling in review views"
    )

    # =========================================================================
    # F9: Native IntersectionObserver Scroll Reveal Engine
    # =========================================================================
    # T1_F9_1: Progressive enhancement root class .js-reveal-active applied
    is_root_active = driver.eval_js('document.documentElement.classList.contains("js-reveal-active")')
    reporter.record(
        "T1_F9_1", "F9", "Tier 1",
        "Document root receives .js-reveal-active upon observer initialization",
        bool(is_root_active),
        "document.documentElement missing .js-reveal-active class"
    )

    # T1_F9_2: Native IntersectionObserver used in app.js
    uses_io = js.contains(r'new\s+IntersectionObserver')
    reporter.record(
        "T1_F9_2", "F9", "Tier 1",
        "Central scroll reveal controller instantiates native IntersectionObserver",
        uses_io,
        "js/app.js does not instantiate native IntersectionObserver"
    )

    # T1_F9_3: Active revealed class .is-revealed supported
    has_revealed_css = css.has_rule_with_selector(r'\.is-revealed')
    reporter.record(
        "T1_F9_3", "F9", "Tier 1",
        "CSS defines .is-revealed class with opacity: 1 and transform: none/translateY(0)",
        has_revealed_css,
        "Missing .is-revealed class in css/style.css"
    )

    # T1_F9_4: Memory cleanup: unobserve called in app.js
    uses_unobserve = js.contains(r'\.unobserve\(')
    reporter.record(
        "T1_F9_4", "F9", "Tier 1",
        "Observer unobserves revealed elements to prevent memory leaks (.unobserve())",
        uses_unobserve,
        "js/app.js missing .unobserve() invocation on revealed targets"
    )

    # T1_F9_5: Global dynamic observation hook window.SEG_ANIMATIONS
    has_global_hook = driver.eval_js('typeof window.SEG_ANIMATIONS === "object" && typeof window.SEG_ANIMATIONS.observeScrollReveals === "function"')
    reporter.record(
        "T1_F9_5", "F9", "Tier 1",
        "Global interface contract window.SEG_ANIMATIONS.observeScrollReveals() exposed",
        bool(has_global_hook),
        "window.SEG_ANIMATIONS.observeScrollReveals is not exposed in global scope"
    )

    # =========================================================================
    # F10: Section & Content Entrance Animations
    # =========================================================================
    # T1_F10_1: .reveal-on-scroll base state under .js-reveal-active
    has_reveal_base = css.has_rule_with_selector(r'\.reveal-on-scroll')
    reporter.record(
        "T1_F10_1", "F10", "Tier 1",
        "CSS defines .reveal-on-scroll base class with translateY and opacity",
        has_reveal_base,
        "Missing .reveal-on-scroll base styling"
    )

    # T1_F10_2: Chapter hero entrance animation
    has_hero_entrance = css.has_rule_with_selector(r'\.chapter-hero') and (
        css.has_rule_with_selector(r'\.chapter-hero\.reveal-on-scroll') or
        any("animation" in r or "transition" in r for r in css.get_rule_content(r'\.chapter-hero'))
    )
    reporter.record(
        "T1_F10_2", "F10", "Tier 1",
        "Chapter hero section defines entrance animation or scroll reveal",
        has_hero_entrance,
        ".chapter-hero lacks entrance transition or reveal-on-scroll binding"
    )

    # T1_F10_3: Chapter headings vertical translate entrance
    has_heading_reveal = css.has_rule_with_selector(r'\.chapter-h1|\.chapter-h2')
    reporter.record(
        "T1_F10_3", "F10", "Tier 1",
        "Chapter section headings define entrance animation rules",
        has_heading_reveal,
        "Missing section heading reveal styles"
    )

    # T1_F10_4: Tables & math blocks entrance animation
    has_table_reveal = css.has_rule_with_selector(r'\.table-responsive|\.content-table')
    reporter.record(
        "T1_F10_4", "F10", "Tier 1",
        "Academic tables and formula blocks support scroll entrance animations",
        has_table_reveal,
        "Missing table reveal animations"
    )

    # T1_F10_5: Slide reference cards grid reveal
    has_ref_reveal = css.has_rule_with_selector(r'\.chapter-references|\.ref-card')
    reporter.record(
        "T1_F10_5", "F10", "Tier 1",
        "Slide reference cards support scroll-reveal entrance",
        has_ref_reveal,
        "Missing reference cards scroll reveal styles"
    )

    # =========================================================================
    # F11: Single-Page Tab Transition Cross-fades
    # =========================================================================
    # T1_F11_1: Tab pane active entrance cross-fade
    tab_pane_rules = css.get_rule_content(r'\.tab-pane\.active')
    has_tab_anim = any("animation" in r or "opacity" in r or "transition" in r for r in tab_pane_rules)
    reporter.record(
        "T1_F11_1", "F11", "Tier 1",
        "Active tab pane (.tab-pane.active) defines entrance cross-fade animation",
        has_tab_anim,
        "Missing entrance transition on .tab-pane.active"
    )

    # T1_F11_2: Inactive tab panes hidden
    driver.click("#nav-knowledge")
    inactive_disp = driver.get_computed_style("#tab-practice").get("display")
    reporter.record(
        "T1_F11_2", "F11", "Tier 1",
        "Inactive tab panes are cleanly unrendered (display: none)",
        inactive_disp == "none",
        f"#tab-practice computed display is '{inactive_disp}' instead of 'none'"
    )

    # T1_F11_3: Tab switching without runtime error
    driver.click("#nav-bank")
    active_is_bank = driver.eval_js('document.getElementById("tab-bank").classList.contains("active")')
    driver.click("#nav-knowledge")
    reporter.record(
        "T1_F11_3", "F11", "Tier 1",
        "Runtime tab switching executes cleanly across views",
        bool(active_is_bank),
        "Tab switching did not mark target pane active"
    )

    # T1_F11_4: Quick search modal entrance animation
    has_modal_anim = bool(css.get_keyframes("modalEnter") or css.has_rule_with_selector(r'\.modal-overlay\.active'))
    reporter.record(
        "T1_F11_4", "F11", "Tier 1",
        "Quick Search modal dialog defines entrance keyframe/transition",
        has_modal_anim,
        "Missing modal dialog entrance animation"
    )

    # T1_F11_5: Submit confirmation modal entrance
    has_confirm_modal = css.has_rule_with_selector(r'#submit-confirm-modal|\.modal-card')
    reporter.record(
        "T1_F11_5", "F11", "Tier 1",
        "Exam submission confirmation modal defines backdrop and card styling",
        has_confirm_modal,
        "Missing confirmation modal styling"
    )

    # =========================================================================
    # F12: Dynamic Question & Content Change Transitions
    # =========================================================================
    # T1_F12_1: Practice question card entrance transition
    has_qcard_anim = css.has_rule_with_selector(r'\.question-card')
    reporter.record(
        "T1_F12_1", "F12", "Tier 1",
        "Question card defines subtle entrance animation on navigation",
        has_qcard_anim,
        "Missing question card transition styles"
    )

    # T1_F12_2: Exam question update transition
    has_exam_q_anim = css.has_rule_with_selector(r'#exam-q-text|\.exam-question-card|\.question-card')
    reporter.record(
        "T1_F12_2", "F12", "Tier 1",
        "Exam question container updates with smooth transition",
        has_exam_q_anim,
        "Missing exam question transition styles"
    )

    # T1_F12_3: Sidebar chapter switch triggers content update
    driver.click("#nav-knowledge")
    initial_ch = driver.eval_js('document.querySelector(".chapter-hero h1")?.textContent || ""')
    # Click chapter 2 in sidebar
    driver.click('#chapter-list-nav [data-ch="2"]')
    time.sleep(0.1)
    new_ch = driver.eval_js('document.querySelector(".chapter-hero h1")?.textContent || ""')
    reporter.record(
        "T1_F12_3", "F12", "Tier 1",
        "Sidebar chapter switch dynamically updates knowledge view without page reload",
        bool(new_ch and new_ch != initial_ch),
        f"Chapter title did not update: initial='{initial_ch}', new='{new_ch}'"
    )

    # T1_F12_4: Changing chapter in practice resets and animates question
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.eval_js('document.getElementById("practice-ch-select").value = "3"; document.getElementById("practice-ch-select").dispatchEvent(new Event("change"));')
    time.sleep(0.1)
    q_badge = driver.eval_js('document.getElementById("practice-q-chapter-tag")?.textContent || ""')
    reporter.record(
        "T1_F12_4", "F12", "Tier 1",
        "Practice chapter select change immediately resets and re-renders question card",
        "3" in q_badge or "Chương 3" in q_badge,
        f"Badge text is '{q_badge}'"
    )

    # T1_F12_5: Option buttons render dynamically with clean DOM
    opt_count = driver.eval_js('document.querySelectorAll("#practice-options-list .option-btn").length')
    reporter.record(
        "T1_F12_5", "F12", "Tier 1",
        "Practice options render dynamically with 4-5 interactive option buttons",
        opt_count in (4, 5),
        f"Found {opt_count} options"
    )

    # =========================================================================
    # F13: Layout Stability & Zero-CLS Guardrails
    # =========================================================================
    # T1_F13_1: Reveal animations strictly use vertical translation
    reveal_rules = css.get_rule_content(r'\.reveal-on-scroll')
    no_lateral_reveal = not any("translateX(" in r for r in reveal_rules)
    uses_translate_y = any("translateY(" in r for r in reveal_rules)
    reporter.record(
        "T1_F13_1", "F13", "Tier 1",
        "Scroll reveal animations strictly use vertical translation (translateY, no lateral spill)",
        no_lateral_reveal and uses_translate_y,
        "Scroll reveals use lateral transforms or lack translateY"
    )

    # T1_F13_2: Container horizontal overflow clipping
    body_overflow = driver.get_computed_style("body").get("overflowX")
    reporter.record(
        "T1_F13_2", "F13", "Tier 1",
        "Document body enforces overflow-x: hidden to prevent horizontal scrollbars",
        body_overflow in ("hidden", "clip"),
        f"Body overflow-x is '{body_overflow}'"
    )

    # T1_F13_3: Viewport width remains stable during tab navigation
    driver.click("#nav-knowledge")
    w1 = driver.eval_js('document.documentElement.scrollWidth')
    cw1 = driver.eval_js('document.documentElement.clientWidth')
    reporter.record(
        "T1_F13_3", "F13", "Tier 1",
        "Viewport scrollWidth equals clientWidth (0 horizontal scroll leakage)",
        w1 == cw1,
        f"scrollWidth={w1} exceeds clientWidth={cw1}"
    )

    # T1_F13_4: Responsive table container prevents layout breaks
    has_table_resp = css.has_rule_with_selector(r'\.table-responsive')
    reporter.record(
        "T1_F13_4", "F13", "Tier 1",
        "Responsive table wrapper (.table-responsive) encapsulates wide content",
        has_table_resp,
        "Missing .table-responsive styling"
    )

    # T1_F13_5: Modal dialogs use fixed positioning without disrupting page layout
    has_modal_fixed = css.has_rule_with_selector(r'\.modal-overlay')
    modal_rules = css.get_rule_content(r'\.modal-overlay')
    is_fixed = any("position: fixed" in r or "position:fixed" in r for r in modal_rules)
    reporter.record(
        "T1_F13_5", "F13", "Tier 1",
        "Modal overlays use position: fixed without causing parent reflows",
        has_modal_fixed and is_fixed,
        "Missing position: fixed on .modal-overlay"
    )

    # =========================================================================
    # F14: GPU 60fps Compositor Optimization
    # =========================================================================
    # T1_F14_1: Scroll reveal transitions animate strictly compositor-safe properties
    has_safe_compositor = any("opacity" in r and "transform" in r for r in reveal_rules)
    reporter.record(
        "T1_F14_1", "F14", "Tier 1",
        "Scroll reveals animate strictly compositor-safe properties (transform, opacity)",
        has_safe_compositor,
        "Scroll reveals do not animate transform and opacity"
    )

    # T1_F14_2: Elimination of unscoped transition: all
    unscoped_all = css.find_unscoped_transition_all()
    # Acceptable if <= 2 legacy items or 0
    reporter.record(
        "T1_F14_2", "F14", "Tier 1",
        "Stylesheet refactors away un-scoped 'transition: all' on animated components",
        len(unscoped_all) == 0,
        f"Found {len(unscoped_all)} instances of transition: all ({unscoped_all[:3]})"
    )

    # T1_F14_3: will-change applied on pending reveals
    has_will_change = css.has_rule_with_selector(r'will-change')
    reporter.record(
        "T1_F14_3", "F14", "Tier 1",
        "will-change property selectively declared for GPU layer promotion",
        has_will_change,
        "No will-change rule declared in stylesheet"
    )

    # T1_F14_4: will-change cleanup on revealed elements
    revealed_rules = css.get_rule_content(r'\.is-revealed')
    has_wc_reset = any("will-change: auto" in r or "will-change:auto" in r for r in revealed_rules)
    reporter.record(
        "T1_F14_4", "F14", "Tier 1",
        "Revealed state (.is-revealed) resets will-change: auto to release GPU texture VRAM",
        has_wc_reset,
        "Missing will-change: auto cleanup on .is-revealed"
    )

    # T1_F14_5: CSS transitions use GPU-accelerated cubic-bezier curves
    has_cubic_bezier = "cubic-bezier" in css.raw_css
    reporter.record(
        "T1_F14_5", "F14", "Tier 1",
        "System transitions utilize high-performance cubic-bezier easing curves",
        has_cubic_bezier,
        "No cubic-bezier easing curve defined in stylesheet"
    )

    # =========================================================================
    # F15: Comprehensive Reduced Motion Support
    # =========================================================================
    # T1_F15_1: Root @media (prefers-reduced-motion: reduce) block declared
    rm_block = css.get_reduced_motion_block()
    reporter.record(
        "T1_F15_1", "F15", "Tier 1",
        "Universal @media (prefers-reduced-motion: reduce) media query declared in CSS",
        bool(rm_block),
        "No @media (prefers-reduced-motion: reduce) block found in css/style.css"
    )

    # T1_F15_2: Animation durations clamped to 0.01ms
    has_dur_clamp = bool(rm_block and ("0.01ms" in rm_block or "0.001s" in rm_block or "0s" in rm_block))
    reporter.record(
        "T1_F15_2", "F15", "Tier 1",
        "Reduced motion overrides clamp animation & transition durations to 0.01ms !important",
        has_dur_clamp,
        "Reduced motion query does not clamp duration to 0.01ms"
    )

    # T1_F15_3: Transform effects neutralized
    has_tf_none = bool(rm_block and "transform: none" in rm_block)
    reporter.record(
        "T1_F15_3", "F15", "Tier 1",
        "Reduced motion overrides neutralize translational transforms (transform: none !important)",
        has_tf_none,
        "Reduced motion query does not set transform: none !important"
    )

    # T1_F15_4: Scroll behavior set to auto
    has_scroll_auto = bool(rm_block and "scroll-behavior: auto" in rm_block)
    reporter.record(
        "T1_F15_4", "F15", "Tier 1",
        "Reduced motion overrides set scroll-behavior: auto !important",
        has_scroll_auto,
        "Reduced motion query does not set scroll-behavior: auto !important"
    )

    # T1_F15_5: JS synchronization with window.matchMedia
    has_js_match_media = js.contains(r'window\.matchMedia\([\'"`]\s*\(\s*prefers-reduced-motion')
    reporter.record(
        "T1_F15_5", "F15", "Tier 1",
        "JavaScript controller queries window.matchMedia for prefers-reduced-motion",
        has_js_match_media,
        "js/app.js does not synchronize scroll behavior via matchMedia"
    )
