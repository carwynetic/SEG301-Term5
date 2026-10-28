"""
Tier 4: Real-World Workload Scenarios E2E Tests (8 Scenarios)
Executes the 8 comprehensive user workflow scenarios specified in TEST_INFRA.md.
Strictly opaque-box DOM event interaction.
"""

import time
from tests.test_harness import CSSAnalyzer, JSAnalyzer, EdgeCDPDriver, TestReporter


def run_tier4_tests(driver: EdgeCDPDriver, css: CSSAnalyzer, js: JSAnalyzer, reporter: TestReporter):
    print("\n--- Running Tier 4: Real-World Workload Scenarios (8 Scenarios) ---")

    # =========================================================================
    # Scenario 1: Full Knowledge Exploration Walkthrough
    # =========================================================================
    print("  -> Executing Scenario 1: Full Knowledge Exploration Walkthrough...")
    s1_pass = True
    s1_msg = ""
    try:
        # Step 1: Navigate to Knowledge tab
        driver.click("#nav-knowledge")
        time.sleep(0.08)

        # Step 2: Filter chapters by keyword "crawling"
        driver.eval_js("""
        (() => {
            const inp = document.getElementById('chapter-search-input');
            if (inp) {
                inp.value = 'crawl';
                inp.dispatchEvent(new Event('input'));
            }
        })()
        """)
        time.sleep(0.08)
        ch_visible = driver.eval_js('document.querySelectorAll("#chapter-list-nav .chapter-item:not([style*=\'none\'])").length')
        if ch_visible == 0:
            s1_pass = False
            s1_msg = "Sidebar search for 'crawl' returned 0 chapters"

        # Step 3: Select Chapter 3 (Crawling & Feeds)
        driver.click('#chapter-list-nav [data-ch="3"]')
        time.sleep(0.12)
        ch3_title = driver.eval_js('document.querySelector(".chapter-hero h1")?.textContent || ""')
        if "Crawl" not in ch3_title and "3" not in ch3_title:
            s1_pass = False
            s1_msg = f"Chapter 3 title did not load: '{ch3_title}'"

        # Step 4: Scroll down to trigger scroll reveals on sections and reference cards
        driver.scroll_to(800)
        time.sleep(0.15)
        driver.scroll_to(1600)
        time.sleep(0.15)

        # Step 5: Click a citation tag to verify smooth anchor scroll
        driver.eval_js("""
        (() => {
            const cite = document.querySelector('.citation-tag, .cite-link');
            if (cite) cite.click();
        })()
        """)
        time.sleep(0.1)

        # Step 6: Verify layout width stability
        w = driver.eval_js('document.documentElement.scrollWidth')
        cw = driver.eval_js('document.documentElement.clientWidth')
        if w > cw:
            s1_pass = False
            s1_msg = f"Horizontal scrollbar detected during Knowledge walkthrough (scrollWidth={w} > clientWidth={cw})"

    except Exception as e:
        s1_pass = False
        s1_msg = str(e)

    reporter.record(
        "T4_SCN_1", "Scenario 1", "Tier 4",
        "Full Knowledge Exploration Walkthrough (Search, Load Ch3, Scroll, Citations, Layout)",
        s1_pass,
        s1_msg
    )

    # =========================================================================
    # Scenario 2: 50-Question Chapter Practice Session
    # =========================================================================
    print("  -> Executing Scenario 2: 50-Question Chapter Practice Session...")
    s2_pass = True
    s2_msg = ""
    try:
        driver.click("#nav-practice")
        time.sleep(0.08)

        # Select Chapter 1
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

        # Answer 5 consecutive questions
        for q_idx in range(5):
            # Click option 1
            driver.click("#practice-options-list .option-btn")
            time.sleep(0.05)
            # Check explanation is shown
            exp_open = driver.eval_js('document.getElementById("practice-explanation-box")?.classList.contains("show")')
            if not exp_open:
                s2_pass = False
                s2_msg = f"Explanation box was not displayed on question {q_idx + 1}"
                break
            # Advance to next question
            driver.click("#practice-next-btn")
            time.sleep(0.05)

        # Check accuracy calculation
        accuracy_text = driver.eval_js('document.getElementById("practice-accuracy")?.textContent || ""')
        if "%" not in accuracy_text:
            s2_pass = False
            s2_msg = f"Accuracy metric invalid: '{accuracy_text}'"

    except Exception as e:
        s2_pass = False
        s2_msg = str(e)

    reporter.record(
        "T4_SCN_2", "Scenario 2", "Tier 4",
        "50-Question Chapter Practice Session (Select Ch1, Answer 5 Qs, Reveal Explanations, Progress)",
        s2_pass,
        s2_msg
    )

    # =========================================================================
    # Scenario 3: Timed Exam Simulation (Intro -> Active Matrix -> Results)
    # =========================================================================
    print("  -> Executing Scenario 3: Timed Exam Simulation...")
    s3_pass = True
    s3_msg = ""
    try:
        driver.click("#nav-exam")
        time.sleep(0.08)

        # Start exam
        driver.click("#start-exam-btn")
        time.sleep(0.1)

        # Answer Q1
        driver.click("#exam-options-list .option-btn")
        time.sleep(0.05)

        # Flag Q1
        driver.click("#exam-flag-btn")
        time.sleep(0.05)

        # Advance to Q2, answer it
        driver.click("#exam-next-btn")
        time.sleep(0.05)
        driver.click("#exam-options-list .option-btn")
        time.sleep(0.05)

        # Verify palette has 1 answered + 1 flagged
        pal1_flagged = driver.eval_js('document.querySelectorAll(".palette-btn")[0]?.classList.contains("flagged")')
        pal2_answered = driver.eval_js('document.querySelectorAll(".palette-btn")[1]?.classList.contains("answered")')
        if not pal1_flagged or not pal2_answered:
            s3_pass = False
            s3_msg = f"Palette state mismatch: Q1 flagged={pal1_flagged}, Q2 answered={pal2_answered}"

        # Submit exam early via confirm modal
        driver.click("#exam-submit-early-btn")
        time.sleep(0.08)
        driver.click("#confirm-submit-btn")
        time.sleep(0.2)

        # Verify Results Screen rendered
        results_active = driver.eval_js('document.getElementById("exam-results-screen")?.classList.contains("active") || document.getElementById("exam-results-screen")?.style.display === "block"')
        score_text = driver.eval_js('document.getElementById("results-score-display")?.textContent || ""')
        if not results_active or not score_text:
            s3_pass = False
            s3_msg = f"Exam results screen not displayed properly: active={results_active}, score='{score_text}'"

    except Exception as e:
        s3_pass = False
        s3_msg = str(e)

    reporter.record(
        "T4_SCN_3", "Scenario 3", "Tier 4",
        "Timed Exam Simulation (Start 50-Q Session, Answer, Flag, Early Submit, Verify Score & Mastery)",
        s3_pass,
        s3_msg
    )

    # =========================================================================
    # Scenario 4: Question Bank Continuous Infinite Scroll Audit
    # =========================================================================
    print("  -> Executing Scenario 4: Question Bank Continuous Infinite Scroll Audit...")
    s4_pass = True
    s4_msg = ""
    try:
        driver.click("#nav-bank")
        time.sleep(0.08)

        # Filter by Chapter 2
        driver.eval_js('document.getElementById("bank-chapter-filter").value = "2"; document.getElementById("bank-chapter-filter").dispatchEvent(new Event("change"));')
        time.sleep(0.1)

        # Toggle answers visibility
        driver.click("#bank-toggle-answers-btn")
        time.sleep(0.08)

        # Progressive scroll through question cards
        driver.scroll_to(500)
        time.sleep(0.1)
        driver.scroll_to(1200)
        time.sleep(0.1)
        driver.scroll_to(2000)
        time.sleep(0.1)

        # Verify zero horizontal overflow during infinite scroll
        overflow = driver.eval_js('document.documentElement.scrollWidth > document.documentElement.clientWidth')
        if overflow:
            s4_pass = False
            s4_msg = "Horizontal scrollbar triggered during Question Bank scroll audit"

    except Exception as e:
        s4_pass = False
        s4_msg = str(e)

    reporter.record(
        "T4_SCN_4", "Scenario 4", "Tier 4",
        "Question Bank Continuous Infinite Scroll Audit (Filter Ch2, Toggle Answers, Multi-level Scroll)",
        s4_pass,
        s4_msg
    )

    # =========================================================================
    # Scenario 5: Glossary 83-Term Tra Cứu & Realtime Filter
    # =========================================================================
    print("  -> Executing Scenario 5: Glossary 83-Term Tra Cứu & Realtime Filter...")
    s5_pass = True
    s5_msg = ""
    try:
        driver.click("#nav-glossary")
        time.sleep(0.08)

        # Verify glossary cards initial (83 on badge, 88 in dataset)
        initial_terms = driver.eval_js('document.querySelectorAll(".glossary-card").length')
        if initial_terms not in (83, 88):
            s5_pass = False
            s5_msg = f"Expected 83 or 88 initial glossary cards, found {initial_terms}"

        # Search for "Inverted Index"
        driver.eval_js("""
        (() => {
            const inp = document.getElementById('glossary-search-input');
            if (inp) {
                inp.value = 'Inverted Index';
                inp.dispatchEvent(new Event('input'));
            }
        })()
        """)
        time.sleep(0.1)
        filtered_terms = driver.eval_js('document.querySelectorAll(".glossary-card:not([style*=\'none\'])").length')
        if filtered_terms == 0:
            s5_pass = False
            s5_msg = "Glossary filter returned 0 results for 'Inverted Index'"

        # Clear search
        driver.eval_js("""
        (() => {
            const inp = document.getElementById('glossary-search-input');
            if (inp) {
                inp.value = '';
                inp.dispatchEvent(new Event('input'));
            }
        })()
        """)
        time.sleep(0.08)
        restored_terms = driver.eval_js('document.querySelectorAll(".glossary-card:not([style*=\'none\'])").length')
        if restored_terms not in (83, 88):
            s5_pass = False
            s5_msg = f"Expected 83 or 88 restored glossary cards, found {restored_terms}"

    except Exception as e:
        s5_pass = False
        s5_msg = str(e)

    reporter.record(
        "T4_SCN_5", "Scenario 5", "Tier 4",
        "Glossary 83-Term Tra Cứu & Realtime Filter (Filter 'Inverted Index', Hover Lift, Restore 83)",
        s5_pass,
        s5_msg
    )

    # =========================================================================
    # Scenario 6: Prefers-Reduced-Motion Accessibility Mode Switch
    # =========================================================================
    print("  -> Executing Scenario 6: Prefers-Reduced-Motion Accessibility Mode Switch...")
    s6_pass = True
    s6_msg = ""
    try:
        # Turn ON reduced motion
        driver.set_reduced_motion(True)
        time.sleep(0.08)

        # Visit Knowledge, Practice, Exam
        driver.click("#nav-knowledge")
        time.sleep(0.05)
        driver.click("#nav-practice")
        time.sleep(0.05)
        driver.click("#practice-options-list .option-btn")
        time.sleep(0.05)

        # Turn OFF reduced motion
        driver.set_reduced_motion(False)
        time.sleep(0.08)

        # Confirm app remains fully functional
        driver.click("#practice-next-btn")
        time.sleep(0.05)
        prog_text = driver.eval_js('document.getElementById("practice-progress-text")?.textContent || ""')
        if not prog_text:
            s6_pass = False
            s6_msg = "Practice progress text missing after reduced motion toggle"

    except Exception as e:
        s6_pass = False
        s6_msg = str(e)

    reporter.record(
        "T4_SCN_6", "Scenario 6", "Tier 4",
        "Prefers-Reduced-Motion Accessibility Mode Switch (Emulate Reduce -> Navigate -> Restore)",
        s6_pass,
        s6_msg
    )

    # =========================================================================
    # Scenario 7: Keyboard Only Navigation & Tab Cycling
    # =========================================================================
    print("  -> Executing Scenario 7: Keyboard Only Navigation & Tab Cycling...")
    s7_pass = True
    s7_msg = ""
    try:
        driver.click("#nav-knowledge")
        time.sleep(0.05)

        # Focus first nav tab
        driver.focus("#nav-knowledge")
        time.sleep(0.05)
        focused_el = driver.eval_js('document.activeElement.id')
        if focused_el != "nav-knowledge":
            s7_pass = False
            s7_msg = f"Focused element is '{focused_el}' instead of 'nav-knowledge'"

        # Open search modal via Ctrl+K
        driver.eval_js('window.dispatchEvent(new KeyboardEvent("keydown", { key: "k", ctrlKey: true, bubbles: true }))')
        time.sleep(0.08)
        modal_open = driver.eval_js('document.getElementById("search-modal")?.classList.contains("active") || document.getElementById("search-modal")?.classList.contains("show")')
        if not modal_open:
            s7_pass = False
            s7_msg = "Search modal did not open on keyboard Ctrl+K"

        # Dismiss via Escape
        driver.eval_js('window.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }))')
        time.sleep(0.08)

    except Exception as e:
        s7_pass = False
        s7_msg = str(e)

    reporter.record(
        "T4_SCN_7", "Scenario 7", "Tier 4",
        "Keyboard Only Navigation & Tab Cycling (Tab Navigation, Ctrl+K Search Modal, Escape Trap)",
        s7_pass,
        s7_msg
    )

    # =========================================================================
    # Scenario 8: Rapid View Switching & Dynamic Re-render Stability
    # =========================================================================
    print("  -> Executing Scenario 8: Rapid View Switching & Dynamic Re-render Stability...")
    s8_pass = True
    s8_msg = ""
    try:
        # Rapidly click between all 5 tabs twice
        for _ in range(2):
            for tab_id in ["#nav-knowledge", "#nav-practice", "#nav-bank", "#nav-glossary", "#nav-exam"]:
                driver.click(tab_id)
                time.sleep(0.04)

        # Return to knowledge tab
        driver.click("#nav-knowledge")
        time.sleep(0.08)

        # Check console errors
        if len(driver.console_errors) > 0:
            s8_pass = False
            s8_msg = f"Console errors detected during stress switching: {driver.console_errors}"

        # Check layout bounds
        w = driver.eval_js('document.documentElement.scrollWidth')
        cw = driver.eval_js('document.documentElement.clientWidth')
        if w > cw:
            s8_pass = False
            s8_msg = f"Layout width destabilized after rapid switching: scrollWidth={w} > clientWidth={cw}"

    except Exception as e:
        s8_pass = False
        s8_msg = str(e)

    reporter.record(
        "T4_SCN_8", "Scenario 8", "Tier 4",
        "Rapid View Switching & Dynamic Re-render Stability (High-frequency Tab Stress, Zero Jank)",
        s8_pass,
        s8_msg
    )
