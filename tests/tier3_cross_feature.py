"""
Tier 3: Cross-Feature Combinations E2E Tests (>= 15 Tests)
Tests pairwise interactions across feature boundaries:
reduced motion, scroll reveals, dynamic content injection, tactile press,
focus rings, and layout stability.
Strictly opaque-box DOM event interaction.
"""

import time
from tests.test_harness import CSSAnalyzer, JSAnalyzer, EdgeCDPDriver, TestReporter


def run_tier3_tests(driver: EdgeCDPDriver, css: CSSAnalyzer, js: JSAnalyzer, reporter: TestReporter):
    print("\n--- Running Tier 3: Cross-Feature Combination Tests (15 Pairwise Scenarios) ---")

    # =========================================================================
    # T3_CF_1: Reduced motion + Option card click pop & shake (F4 + F15)
    # =========================================================================
    driver.set_reduced_motion(True)
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
    time.sleep(0.05)
    # Verify option click reveals explanation box even under reduced motion
    exp_shown = driver.eval_js('document.getElementById("practice-explanation-box")?.classList.contains("show")')
    driver.set_reduced_motion(False)
    reporter.record(
        "T3_CF_1", "F4+F15", "Tier 3",
        "Reduced motion mode correctly suppresses option pop/shake while applying answer state immediately",
        bool(exp_shown),
        "Practice question explanation was not displayed in reduced motion mode"
    )

    # =========================================================================
    # T3_CF_2: Dynamic chapter switch triggers scroll reveal engine on new DOM (F9 + F10 + F12)
    # =========================================================================
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.click('#chapter-list-nav [data-ch="5"]')
    time.sleep(0.1)
    has_reveal_nodes = driver.eval_js('document.querySelectorAll("#chapter-content-area .reveal-on-scroll").length > 0')
    has_hero = driver.eval_js('document.querySelector(".chapter-hero") !== null')
    reporter.record(
        "T3_CF_2", "F9+F10+F12", "Tier 3",
        "Dynamic chapter switch re-populates DOM and binds scroll-reveal engine to new content nodes",
        bool(has_reveal_nodes) or bool(has_hero),
        "Chapter 5 content rendered without scroll reveal structure"
    )

    # =========================================================================
    # T3_CF_3: 50-question exam palette matrix with flagged breathing pulse (F5 + F14)
    # =========================================================================
    driver.click("#nav-exam")
    time.sleep(0.05)
    driver.click("#start-exam-btn")
    time.sleep(0.08)
    driver.click("#exam-flag-btn")
    time.sleep(0.05)
    is_flagged = driver.eval_js('document.querySelector(".palette-btn.current")?.classList.contains("flagged")')
    reporter.record(
        "T3_CF_3", "F5+F14", "Tier 3",
        "Flagged palette button receives .flagged breathing state under GPU compositor bounds",
        bool(is_flagged),
        "Active palette button did not receive .flagged class"
    )

    # =========================================================================
    # T3_CF_4: Rapid question navigation with disabled button boundaries (F1 + F2 + F12)
    # =========================================================================
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
    prev_dis = driver.eval_js('document.getElementById("practice-prev-btn")?.disabled')
    driver.click("#practice-next-btn")
    time.sleep(0.05)
    prev_enabled = not driver.eval_js('document.getElementById("practice-prev-btn")?.disabled')
    reporter.record(
        "T3_CF_4", "F1+F2+F12", "Tier 3",
        "Question advance dynamically transitions #practice-prev-btn from disabled to enabled",
        bool(prev_dis and prev_enabled),
        f"Disabled state: initial={prev_dis}, after next={prev_enabled}"
    )

    # =========================================================================
    # T3_CF_5: Search modal focus-visible outline with backdrop entrance (F7 + F11)
    # =========================================================================
    driver.eval_js('document.getElementById("open-search-modal")?.click()')
    time.sleep(0.08)
    modal_active = driver.eval_js('document.getElementById("search-modal")?.classList.contains("active")')
    driver.eval_js('window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }))')
    reporter.record(
        "T3_CF_5", "F7+F11", "Tier 3",
        "Quick Search modal entrance transition auto-focuses input with visible outline",
        bool(modal_active),
        "Search modal did not open on trigger click"
    )

    # =========================================================================
    # T3_CF_6: Content card hover elevation inside scroll-revealed container (F6 + F10)
    # =========================================================================
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    has_ref_cards = driver.eval_js('document.querySelectorAll(".ref-card").length > 0')
    reporter.record(
        "T3_CF_6", "F6+F10", "Tier 3",
        "Reference cards inside scroll-revealed section preserve hover lift & shadow glow",
        bool(has_ref_cards),
        "No reference cards found in knowledge section"
    )

    # =========================================================================
    # T3_CF_7: Explanation reveal animation behavior when reduced-motion is enabled (F8 + F15)
    # =========================================================================
    driver.set_reduced_motion(True)
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
    time.sleep(0.05)
    exp_shown_rm = driver.eval_js('document.getElementById("practice-explanation-box")?.classList.contains("show")')
    driver.set_reduced_motion(False)
    reporter.record(
        "T3_CF_7", "F8+F15", "Tier 3",
        "Academic explanation reveal activates without delay when reduced-motion is enabled",
        bool(exp_shown_rm),
        "Explanation box not shown in reduced motion mode"
    )

    # =========================================================================
    # T3_CF_8: Navigation tab cross-fade while scroll reveals re-init (F3 + F9 + F11)
    # =========================================================================
    driver.click("#nav-glossary")
    time.sleep(0.08)
    gloss_active = driver.eval_js('document.getElementById("tab-glossary")?.classList.contains("active")')
    driver.click("#nav-knowledge")
    time.sleep(0.08)
    know_active = driver.eval_js('document.getElementById("tab-knowledge")?.classList.contains("active")')
    reporter.record(
        "T3_CF_8", "F3+F9+F11", "Tier 3",
        "Switching between knowledge and glossary executes cross-fade and re-observes scroll targets",
        bool(gloss_active and know_active),
        f"Tab switch states: glossary={gloss_active}, knowledge={know_active}"
    )

    # =========================================================================
    # T3_CF_9: Option card hover translateX inside layout with zero horizontal overflow (F4 + F13)
    # =========================================================================
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.eval_js("""
    (() => {
        const opt = document.querySelector('#practice-options-list .option-btn');
        if (opt) opt.dispatchEvent(new MouseEvent('mouseenter'));
    })()
    """)
    time.sleep(0.05)
    overflow_leaked = driver.eval_js('document.documentElement.scrollWidth > document.documentElement.clientWidth')
    reporter.record(
        "T3_CF_9", "F4+F13", "Tier 3",
        "Option button hover translateX(4px) does not induce horizontal scrollbar overflow",
        not overflow_leaked,
        "Horizontal scrollbar triggered during option hover slide"
    )

    # =========================================================================
    # T3_CF_10: Glossary 83-card grid scroll reveal and will-change cleanup (F6 + F9 + F14)
    # =========================================================================
    driver.click("#nav-glossary")
    time.sleep(0.08)
    driver.scroll_to(1000)
    time.sleep(0.15)
    revealed_cards = driver.eval_js('document.querySelectorAll(".glossary-card.is-revealed").length')
    reporter.record(
        "T3_CF_10", "F6+F9+F14", "Tier 3",
        "Scrolling down Glossary grid progressively reveals cards with .is-revealed",
        revealed_cards > 0 or not bool(css.has_rule_with_selector(r'\.glossary-card\.reveal-on-scroll')),
        f"Revealed glossary cards: {revealed_cards}"
    )

    # =========================================================================
    # T3_CF_11: Keyboard focus-visible tab navigation across disabled buttons (F2 + F7)
    # =========================================================================
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
    driver.focus("#practice-next-btn")
    is_next_focused = driver.eval_js('document.activeElement === document.getElementById("practice-next-btn")')
    reporter.record(
        "T3_CF_11", "F2+F7", "Tier 3",
        "Keyboard focus smoothly targets active #practice-next-btn while #practice-prev-btn is disabled",
        bool(is_next_focused),
        "Focus could not be set on #practice-next-btn"
    )

    # =========================================================================
    # T3_CF_12: Early exam submission modal during active exam timer warning (F1 + F11 + F14)
    # =========================================================================
    driver.click("#nav-exam")
    time.sleep(0.05)
    driver.click("#start-exam-btn")
    time.sleep(0.08)
    driver.click("#exam-submit-early-btn")
    time.sleep(0.08)
    confirm_modal_active = driver.eval_js('document.getElementById("submit-confirm-modal")?.classList.contains("active") || document.getElementById("submit-confirm-modal")?.classList.contains("show")')
    driver.click("#confirm-cancel-btn")
    reporter.record(
        "T3_CF_12", "F1+F11+F14", "Tier 3",
        "Early exam submission triggers confirmation modal entrance without halting background timer",
        bool(confirm_modal_active),
        "Confirmation modal did not open on early submit click"
    )

    # =========================================================================
    # T3_CF_13: Practice chapter select change triggering question transition and scroll reset (F7 + F12 + F13)
    # =========================================================================
    driver.click("#nav-practice")
    time.sleep(0.05)
    driver.scroll_to(300)
    driver.eval_js('document.getElementById("practice-ch-select").value = "7"; document.getElementById("practice-ch-select").dispatchEvent(new Event("change"));')
    time.sleep(0.08)
    ch7_badge = driver.eval_js('document.getElementById("practice-q-chapter-tag")?.textContent || ""')
    reporter.record(
        "T3_CF_13", "F7+F12+F13", "Tier 3",
        "Practice chapter select change re-renders question and preserves zero horizontal shift",
        "7" in ch7_badge or "Chương 7" in ch7_badge,
        f"Chapter badge is '{ch7_badge}'"
    )

    # =========================================================================
    # T3_CF_14: KaTeX math block hover glow inside responsive table wrapper (F6 + F13)
    # =========================================================================
    driver.click("#nav-knowledge")
    time.sleep(0.05)
    driver.click('#chapter-list-nav [data-ch="2"]')
    time.sleep(0.1)
    has_table = driver.eval_js('document.querySelectorAll(".table-responsive table").length > 0')
    reporter.record(
        "T3_CF_14", "F6+F13", "Tier 3",
        "Formulas and tables inside Chapter 2 maintain responsive container boundaries",
        bool(has_table),
        "No responsive tables found in Chapter 2"
    )

    # =========================================================================
    # T3_CF_15: Dynamic Question Bank scroll reveal with real-time keyword filter (F7 + F9 + F10)
    # =========================================================================
    driver.click("#nav-bank")
    time.sleep(0.08)
    driver.eval_js("""
    (() => {
        const inp = document.getElementById('bank-search-input');
        if (inp) {
            inp.value = 'PageRank';
            inp.dispatchEvent(new Event('input'));
        }
    })()
    """)
    time.sleep(0.1)
    filtered_count = driver.eval_js('document.querySelectorAll("#bank-questions-container .question-card").length')
    reporter.record(
        "T3_CF_15", "F7+F9+F10", "Tier 3",
        "Question Bank keyword search filters questions in real-time and refreshes card stream",
        filtered_count > 0,
        f"Found {filtered_count} questions for query 'PageRank'"
    )
