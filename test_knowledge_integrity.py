import json
import re
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_full_knowledge_base_integrity():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE SEG301 KNOWLEDGE BASE INTEGRITY TESTS")
    print("=" * 60)
    
    # 1. Verify JSON file exists and is valid
    json_path = os.path.join("data", "knowledge.json")
    assert os.path.exists(json_path), f"File {json_path} does not exist"
    with open(json_path, "r", encoding="utf-8") as f:
        kdata = json.load(f)
        
    assert len(kdata) == 17, f"Expected 17 chapters, found {len(kdata)}"
    
    # 2. Verify JS file exists and matches JSON exactly
    js_path = os.path.join("data", "knowledge.js")
    assert os.path.exists(js_path), f"File {js_path} does not exist"
    with open(js_path, "r", encoding="utf-8") as f:
        js_text = f.read()
    assert "window.SEG_KNOWLEDGE" in js_text, "knowledge.js missing window.SEG_KNOWLEDGE"
    js_json_part = js_text[js_text.find('{'):js_text.rfind('}')+1]
    js_data = json.loads(js_json_part)
    assert set(kdata.keys()) == set(js_data.keys()), "Chapter keys mismatch between JSON and JS"
    for ch_k in kdata:
        assert kdata[ch_k]["content_html"] == js_data[ch_k]["content_html"], f"Chapter {ch_k} content mismatch between JSON and JS"
        assert kdata[ch_k]["references"] == js_data[ch_k]["references"], f"Chapter {ch_k} references mismatch between JSON and JS"
    print("✓ JSON and JS data stores are 100% synchronized and valid across all 17 chapters.")

    # 3. Verify Table coverage across all chapters
    # Chapters that must contain tables based on source material
    expected_tables = {
        1: 1, # Extended IR applications
        2: 3, # IR vs DBMS, TAAT vs DAAT, Summary by Process
        3: 1, # Crawls & Feeds Cheat-Sheet
        4: 1, # Text Processing Core Keywords Quick Reference
        5: 1, # DAAT vs TAAT comparison
        6: 1, # Queries & Interfaces Cheat-Sheet
        7: 2, # Broder's intent taxonomy, Chapter 7 Core Keywords
        8: 1, # SEO 3 branches comparison
        9: 2, # Contingency table, Efficiency metrics
        10: 2, # Generative vs Discriminative, K-means summary
        11: 3, # 5 Tag Categories, Metasearch vs P2P, Social Search Keywords
        12: 1, # Beyond Bag of Words keywords
        14: 1  # PageRank vs HITS
    }
    
    total_tables_found = 0
    for ch_num, min_tables in expected_tables.items():
        html = kdata[str(ch_num)]["content_html"]
        tbl_count = html.count("<table")
        assert tbl_count >= min_tables, f"Chapter {ch_num} expected at least {min_tables} tables, found {tbl_count}"
        assert html.count("table-responsive") >= min_tables, f"Chapter {ch_num} missing table-responsive wrapper!"
        assert html.count("content-table") >= min_tables, f"Chapter {ch_num} missing content-table class!"
        total_tables_found += tbl_count
        
    print(f"✓ Table verification passed: {total_tables_found} tables verified across required chapters.")

    # 4. Verify Hierarchical list formatting (.content-sub-li) across chapters
    chapters_with_subbullets = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    total_sub_lis = 0
    for ch_num in chapters_with_subbullets:
        html = kdata[str(ch_num)]["content_html"]
        sub_count = html.count("content-sub-li")
        assert sub_count >= 5, f"Chapter {ch_num} missing sub-bullets (found {sub_count})"
        total_sub_lis += sub_count
    print(f"✓ Hierarchical list formatting passed: {total_sub_lis} sub-bullets (.content-sub-li) verified.")

    # 5. Verify 3rd-level sub-bullets (.content-sub-sub-li) exist in deeply nested chapters
    deep_chapters = [4, 5]
    for ch_num in deep_chapters:
        html = kdata[str(ch_num)]["content_html"]
        sub_sub_count = html.count("content-sub-sub-li")
        assert sub_sub_count >= 5, f"Chapter {ch_num} expected level 3 sub-bullets (.content-sub-sub-li), found {sub_sub_count}"
    print("✓ Deep hierarchical nesting (.content-sub-sub-li) verified in chapters 4 & 5.")

    # 6. Verify Citations & Slide References in every chapter
    for ch_num in range(1, 18):
        ch = kdata[str(ch_num)]
        html = ch["content_html"]
        refs = ch.get("references", [])
        assert len(refs) == 5, f"Chapter {ch_num} expected 5 references, found {len(refs)}"
        for ref in refs:
            ref_id = ref.get("id")
            assert f'href="#ref-{ref_id}"' in html, f"Citation tag for ref-{ref_id} not linked in Ch {ch_num} HTML"
            assert f'id="ref-{ref_id}"' in html, f"Ref card id ref-{ref_id} not found in Ch {ch_num} HTML"
    print("✓ All citations and reference cards (85 total across 17 chapters) verified 100% intact.")

    # 7. Verify Chapter 2 specific topics
    ch2_html = kdata["2"]["content_html"]
    required_ch2_keywords = [
        "Text Acquisition", "Text Transformation", "Index Creation",
        "User Interaction", "Ranking", "Evaluation",
        "DBMS", "TAAT", "DAAT", "BSBI", "SPIMI", "Little's Law",
        "Query Broker", "Result Cache", "WAND", "Positional Index"
    ]
    for kw in required_ch2_keywords:
        assert kw.lower() in ch2_html.lower(), f"Chapter 2 missing core keyword: {kw}"
    print("✓ Chapter 2 core keywords and architectural concepts verified.")

    # 8. Verify No raw markdown artifacts remaining
    for ch_num in range(1, 18):
        html = kdata[str(ch_num)]["content_html"]
        assert not re.search(r'\|\s*:?-+:?\s*\|', html), f"Chapter {ch_num} contains raw markdown table delimiter!"
    print("✓ Clean HTML output confirmed: no raw markdown table delimiters in knowledge base.")
    
    print("=" * 60)
    print("ALL 8 VERIFICATION GATES PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_full_knowledge_base_integrity()
    except AssertionError as e:
        print(f"FAILED: {e}")
        sys.exit(1)
