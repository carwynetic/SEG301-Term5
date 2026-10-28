/**
 * SEG301 Search Engines Exam Preparation Portal
 * Full Interactive Application Logic
 */

(function () {
  'use strict';

  // --- APPLICATION STATE ---
  const state = {
    theme: localStorage.getItem('seg301_theme') || 'dark',
    activeTab: 'knowledge',
    activeChapterId: 1,

    // Practice Mode State
    practice: {
      chapterId: 1,
      currentIndex: 0,
      questions: [],
      userAnswers: {}, // { qid: selected_index }
      score: { correct: 0, incorrect: 0 }
    },

    // Exam Mode State
    exam: {
      active: false,
      questions: [],
      answers: {}, // { qid: selected_index }
      flagged: new Set(),
      currentIndex: 0,
      timeRemaining: 50 * 60, // 50 minutes = 3000 seconds
      timerInterval: null,
      submitted: false,
      startTime: null,
      endTime: null,
      reviewFilter: 'all' // 'all' | 'wrong' | 'correct' | 'flagged'
    },

    // Question Bank State
    bank: {
      filterChapter: 'all',
      searchQuery: '',
      showAnswers: false
    },

    // Glossary State
    glossary: {
      searchQuery: ''
    }
  };

  // --- DOM ELEMENTS ---
  const dom = {
    // Nav tabs
    navTabs: document.querySelectorAll('.nav-tab'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    themeToggleBtn: document.getElementById('theme-toggle'),
    themeIcon: document.getElementById('theme-icon'),
    brandLogo: document.getElementById('brand-logo'),

    // Knowledge Base
    chapterSearchInput: document.getElementById('chapter-search-input'),
    chapterListNav: document.getElementById('chapter-list-nav'),
    chapterContentArea: document.getElementById('chapter-content-area'),

    // Practice
    practiceChSelect: document.getElementById('practice-ch-select'),
    practiceQBadge: document.getElementById('practice-q-badge'),
    practiceQChapterTag: document.getElementById('practice-q-chapter-tag'),
    practiceQText: document.getElementById('practice-q-text'),
    practiceOptionsList: document.getElementById('practice-options-list'),
    practiceExplanationBox: document.getElementById('practice-explanation-box'),
    practiceExplanationText: document.getElementById('practice-explanation-text'),
    practicePrevBtn: document.getElementById('practice-prev-btn'),
    practiceNextBtn: document.getElementById('practice-next-btn'),
    practiceProgressText: document.getElementById('practice-progress-text'),
    practiceCorrectCount: document.getElementById('practice-correct-count'),
    practiceIncorrectCount: document.getElementById('practice-incorrect-count'),
    practiceAccuracy: document.getElementById('practice-accuracy'),

    // Exam
    examIntroScreen: document.getElementById('exam-intro-screen'),
    examActiveScreen: document.getElementById('exam-active-screen'),
    examResultsScreen: document.getElementById('exam-results-screen'),
    startExamBtn: document.getElementById('start-exam-btn'),
    retakeExamBtn: document.getElementById('retake-exam-btn'),
    examQCounter: document.getElementById('exam-q-counter'),
    examCurrentChBadge: document.getElementById('exam-current-ch-badge'),
    examTimerBox: document.getElementById('exam-timer-box'),
    examTimerVal: document.getElementById('exam-timer-val'),
    examFlagBtn: document.getElementById('exam-flag-btn'),
    examFlagText: document.getElementById('exam-flag-text'),
    examSubmitEarlyBtn: document.getElementById('exam-submit-early-btn'),
    examQText: document.getElementById('exam-q-text'),
    examOptionsList: document.getElementById('exam-options-list'),
    examPrevBtn: document.getElementById('exam-prev-btn'),
    examNextBtn: document.getElementById('exam-next-btn'),
    examPaletteGrid: document.getElementById('exam-palette-grid'),

    // Exam Results
    resultScoreDisplay: document.getElementById('result-score-display'),
    resultStatusBadge: document.getElementById('result-status-badge'),
    resMetricAccuracy: document.getElementById('res-metric-accuracy'),
    resMetricCorrect: document.getElementById('res-metric-correct'),
    resMetricIncorrect: document.getElementById('res-metric-incorrect'),
    resMetricTime: document.getElementById('res-metric-time'),
    examMasteryList: document.getElementById('exam-mastery-list'),
    studyRecommendationsContent: document.getElementById('study-recommendations-content'),
    examReviewQuestionsList: document.getElementById('exam-review-questions-list'),
    reviewFilterChips: document.querySelectorAll('.filter-chip'),

    // Modals
    openSearchModalBtn: document.getElementById('open-search-modal'),
    searchModal: document.getElementById('search-modal'),
    globalSearchInput: document.getElementById('global-search-input'),
    searchModalResults: document.getElementById('search-modal-results'),
    submitConfirmModal: document.getElementById('submit-confirm-modal'),
    closeConfirmModalBtn: document.getElementById('close-confirm-modal'),
    confirmCancelBtn: document.getElementById('confirm-cancel-btn'),
    confirmSubmitBtn: document.getElementById('confirm-submit-btn'),
    confirmUnansweredAlert: document.getElementById('confirm-unanswered-alert'),
    confirmUnansweredCount: document.getElementById('confirm-unanswered-count'),

    // Bank
    bankSearchInput: document.getElementById('bank-search-input'),
    bankChapterFilter: document.getElementById('bank-chapter-filter'),
    bankToggleAnswersBtn: document.getElementById('bank-toggle-answers-btn'),
    bankQuestionsContainer: document.getElementById('bank-questions-container'),
    bankCountInfo: document.getElementById('bank-count-info'),

    // Glossary
    glossarySearchInput: document.getElementById('glossary-search-input'),
    glossaryItemsGrid: document.getElementById('glossary-items-grid'),
    glossaryCountInfo: document.getElementById('glossary-count-info')
  };

  // --- F9 & F15: SCROLL REVEAL ENGINE & MOTION SYNC ---
  let scrollObserver = null;

  function getScrollBehavior() {
    const isReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    return isReduced ? 'auto' : 'smooth';
  }

  function initScrollRevealEngine() {
    if (!('IntersectionObserver' in window)) {
      return;
    }

    try {
      scrollObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            observer.unobserve(entry.target);
          }
        });
      }, {
        root: null,
        rootMargin: '0px 0px -40px 0px',
        threshold: 0.1
      });

      document.documentElement.classList.add('js-reveal-active');
      observeScrollReveals(document);
    } catch (e) {
      console.warn('Scroll reveal engine init warning:', e);
    }
  }

  function observeScrollReveals(container) {
    if (!scrollObserver || !container || typeof container.querySelectorAll !== 'function') {
      return;
    }

    try {
      if (container.classList && container.classList.contains('reveal-on-scroll') && !container.classList.contains('is-revealed')) {
        scrollObserver.observe(container);
      }
      const targets = container.querySelectorAll('.reveal-on-scroll');
      targets.forEach(el => {
        if (!el.classList.contains('is-revealed')) {
          scrollObserver.observe(el);
        }
      });
    } catch (e) {
      console.warn('observeScrollReveals warning:', e);
    }
  }

  // Global Interface Contract (F9)
  window.SEG_ANIMATIONS = {
    observeScrollReveals: function (container) {
      observeScrollReveals(container);
    },
    refresh: function () {
      observeScrollReveals(document);
    }
  };

  // --- INITIALIZATION ---
  function init() {
    const scoreDisplay = document.getElementById('result-score-display');
    if (scoreDisplay && !document.getElementById('results-score-display')) {
      scoreDisplay.id = 'results-score-display';
    }
    initTheme();
    initMermaid();
    bindEvents();
    renderChapterNav();
    loadChapterKnowledge(state.activeChapterId);
    initPracticeTab();
    initBankTab();
    initGlossaryTab();
    renderMath();
    renderMermaid();
    initScrollRevealEngine();
  }

  // --- THEME SYSTEM ---
  function initTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    dom.themeIcon.textContent = state.theme === 'dark' ? '🌙' : '☀️';
  }

  function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('seg301_theme', state.theme);
    initTheme();
    initMermaid();
    if (state.activeTab === 'knowledge') {
      loadChapterKnowledge(state.activeChapterId);
    }
  }

  // --- TAB NAVIGATION ---
  function switchTab(tabId) {
    state.activeTab = tabId;

    dom.navTabs.forEach(tab => {
      if (tab.dataset.tab === tabId) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    dom.tabPanes.forEach(pane => {
      if (pane.id === `tab-${tabId}`) {
        pane.classList.add('active');
      } else {
        pane.classList.remove('active');
      }
    });

    // Close any active modals on tab change (T2_F11_1)
    if (dom.searchModal && (dom.searchModal.classList.contains('active') || dom.searchModal.classList.contains('show'))) {
      closeSearchModal();
    }
    if (dom.submitConfirmModal && (dom.submitConfirmModal.classList.contains('active') || dom.submitConfirmModal.classList.contains('show'))) {
      dom.submitConfirmModal.classList.remove('show', 'active');
    }

    // Reset viewport scroll to top (T2_F11_4)
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;

    // Preserve exam screens if switching to/from exam tab (T2_F11_2)
    if (tabId === 'exam') {
      if (state.exam.active) {
        dom.examIntroScreen.style.display = 'none';
        dom.examIntroScreen.classList.remove('active');
        dom.examResultsScreen.style.display = 'none';
        dom.examResultsScreen.classList.remove('active');
        dom.examActiveScreen.style.display = 'flex';
        dom.examActiveScreen.classList.add('active');
      } else if (state.exam.submitted) {
        dom.examIntroScreen.style.display = 'none';
        dom.examIntroScreen.classList.remove('active');
        dom.examActiveScreen.style.display = 'none';
        dom.examActiveScreen.classList.remove('active');
        dom.examResultsScreen.style.display = 'block';
        dom.examResultsScreen.classList.add('active');
      } else {
        dom.examIntroScreen.style.display = 'block';
        dom.examIntroScreen.classList.add('active');
        dom.examActiveScreen.style.display = 'none';
        dom.examActiveScreen.classList.remove('active');
        dom.examResultsScreen.style.display = 'none';
        dom.examResultsScreen.classList.remove('active');
      }
    }

    renderMath();
    renderMermaid();
    if (window.SEG_ANIMATIONS) {
      window.SEG_ANIMATIONS.refresh();
    }
  }

  // --- MERMAID DIAGRAM ENGINE HELPER ---
  function initMermaid() {
    if (window.mermaid) {
      try {
        window.mermaid.initialize({
          startOnLoad: false,
          theme: state.theme === 'dark' ? 'dark' : 'default',
          securityLevel: 'loose',
          fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
          flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis'
          }
        });
      } catch (e) {
        console.warn('Mermaid init warning:', e);
      }
    }
  }

  function renderMermaid() {
    if (window.mermaid) {
      try {
        const diagrams = document.querySelectorAll('.mermaid');
        if (diagrams.length > 0) {
          // If mermaid.run is available (Mermaid 10+)
          if (typeof window.mermaid.run === 'function') {
            window.mermaid.run({
              querySelector: '.mermaid'
            }).catch(err => {
              console.warn('Mermaid run catch:', err);
            });
          } else if (typeof window.mermaid.init === 'function') {
            window.mermaid.init(undefined, diagrams);
          }
        }
      } catch (e) {
        console.warn('Mermaid render warning:', e);
      }
    }
  }

  // --- MATH RENDERING HELPER (KATEX) ---
  function renderMath(targetEl = null) {
    if (window.renderMathInElement) {
      try {
        const container = targetEl || document.getElementById('chapter-content-area') || document.body;
        window.renderMathInElement(container, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false },
            { left: '\\[', right: '\\]', display: true }
          ],
          ignoredTags: ["script", "noscript", "style", "textarea"],
          throwOnError: false
        });
      } catch (e) {
        console.warn('KaTeX render warning:', e);
      }
    }
  }

  // --- TAB 1: KNOWLEDGE BASE CONTROLLER ---
  function renderChapterNav(filter = '') {
    const chapters = window.SEG_CHAPTERS || [];
    dom.chapterListNav.innerHTML = '';

    const query = filter.toLowerCase().trim();

    chapters.forEach(ch => {
      const title = ch.title || ch.title_en || `Chapter ${ch.id}`;
      const titleVn = ch.title_vn || '';
      const match = !query ||
        title.toLowerCase().includes(query) ||
        titleVn.toLowerCase().includes(query) ||
        ch.id.toString() === query;

      if (!match) return;

      const li = document.createElement('li');
      li.className = `chapter-item ${ch.id === state.activeChapterId ? 'active' : ''}`;
      li.dataset.chapterId = ch.id;
      li.dataset.ch = ch.id;
      li.setAttribute('data-ch', ch.id);

      li.innerHTML = `
        <div class="chapter-item-icon">${ch.icon_emoji || '📖'}</div>
        <div class="chapter-item-content">
          <div class="chapter-item-num">Chương ${ch.id}</div>
          <div class="chapter-item-title">${title}</div>
          <div class="chapter-item-sub">${titleVn}</div>
        </div>
      `;

      li.addEventListener('click', () => {
        selectChapter(ch.id);
      });

      dom.chapterListNav.appendChild(li);
    });
  }

  function selectChapter(chapterId) {
    state.activeChapterId = chapterId;

    document.querySelectorAll('.chapter-item').forEach(el => {
      if (parseInt(el.dataset.chapterId, 10) === chapterId) {
        el.classList.add('active');
      } else {
        el.classList.remove('active');
      }
    });

    loadChapterKnowledge(chapterId);
  }

  function loadChapterKnowledge(chapterId) {
    const knowledgeData = window.SEG_KNOWLEDGE || {};
    const chapters = window.SEG_CHAPTERS || [];
    const meta = chapters.find(c => c.id === chapterId) || {
      id: chapterId,
      title: `Chapter ${chapterId}`,
      title_en: `Chapter ${chapterId}`,
      title_vn: `Chương ${chapterId}`,
      category: 'IR Core',
      icon_emoji: '📖',
      source_file: `Chapter ${chapterId}.pptx`,
      total_slides: 40
    };

    const chapterRaw = knowledgeData[chapterId.toString()];
    let chapterHtml = '';
    if (typeof chapterRaw === 'string') {
      chapterHtml = chapterRaw;
    } else if (chapterRaw && typeof chapterRaw === 'object') {
      chapterHtml = chapterRaw.content_html || '';
    }

    if (!chapterHtml) {
      chapterHtml = `
        <div style="padding: 2rem; text-align: center; color: var(--text-muted);">
          <h3>Đang tải nội dung chương ${chapterId}...</h3>
        </div>
      `;
    }

    const titleEn = meta.title || meta.title_en || `Chapter ${meta.id}`;
    const sourceFile = meta.file || meta.source_file || `Chapter ${meta.id}.pptx`;

    dom.chapterContentArea.innerHTML = `
      <!-- Chapter Hero Banner -->
      <section class="chapter-hero reveal-on-scroll">
        <div class="hero-meta">
          <span class="badge-tag">Chương ${meta.id}</span>
          <span class="badge-tag" style="color: var(--accent-cyan); border-color: rgba(6, 182, 212, 0.3);">${meta.category || 'IR Core'}</span>
          <span class="badge-tag" style="color: var(--accent-emerald); border-color: rgba(16, 185, 129, 0.3);">📄 ${sourceFile}</span>
          <span style="font-size: 0.8rem; color: var(--text-muted); margin-left: auto;">⏱️ ~25 phút đọc</span>
        </div>
        <h1 class="chapter-h1">${titleEn}</h1>
        <div class="vn-title">${meta.title_vn}</div>
        <div class="hero-actions">
          <button class="btn-primary" id="btn-jump-to-practice">
            ✍️ Luyện tập 50 câu trắc nghiệm Chương ${meta.id}
          </button>
        </div>
      </section>

      <!-- Chapter Full Body Content -->
      <div class="chapter-body" id="chapter-main-body">
        ${chapterHtml}
      </div>
    `;

    // Hook Jump to Practice button
    const jumpBtn = document.getElementById('btn-jump-to-practice');
    if (jumpBtn) {
      jumpBtn.addEventListener('click', () => {
        state.practice.chapterId = chapterId;
        dom.practiceChSelect.value = chapterId.toString();
        loadPracticeQuestions(chapterId);
        switchTab('practice');
      });
    }

    // Attach citation smooth-scroll and highlight listeners
    attachCitationListeners();

    // Re-render math formulas
    renderMath();

    // Bind scroll reveal engine to new content nodes (F9 + F10 + F12)
    dom.chapterContentArea.querySelectorAll('.chapter-hero, .chapter-section, .chapter-h1, .chapter-h2, .table-responsive, .content-table, .chapter-references, .ref-card, .rule-box, .math-block, .mermaid-diagram-wrap').forEach(el => {
      el.classList.add('reveal-on-scroll');
    });
    if (window.SEG_ANIMATIONS) {
      window.SEG_ANIMATIONS.observeScrollReveals(dom.chapterContentArea);
    }

    // Re-render mermaid diagrams
    renderMermaid();

    // Scroll reader to top
    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
  }

  function attachCitationListeners() {
    const citeLinks = dom.chapterContentArea.querySelectorAll('.citation-tag, .cite-link');
    citeLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const href = link.getAttribute('href') || '';
        const targetId = href.replace('#', '') || (link.dataset.ref ? `ref-${link.dataset.ref}` : '');
        let targetCard = document.getElementById(targetId);

        if (!targetCard && link.dataset.ref) {
          targetCard = document.querySelector(`[data-ref="${link.dataset.ref}"]`);
        }

        if (targetCard) {
          targetCard.scrollIntoView({ behavior: getScrollBehavior(), block: 'center' });
          targetCard.classList.remove('highlight-citation');
          void targetCard.offsetWidth; // Force DOM reflow
          targetCard.classList.add('highlight-citation');
        }
      });
    });
  }

  // --- TAB 2: CHAPTER PRACTICE CONTROLLER ---
  function initPracticeTab() {
    const chapters = window.SEG_CHAPTERS || [];
    dom.practiceChSelect.innerHTML = '';

    chapters.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch.id.toString();
      const title = ch.title || ch.title_en || `Chapter ${ch.id}`;
      opt.textContent = `Chương ${ch.id}: ${title} (${ch.title_vn || ''})`;
      dom.practiceChSelect.appendChild(opt);
    });

    // Add Comp option
    const compOpt = document.createElement('option');
    compOpt.value = 'comp';
    compOpt.textContent = `Ngẫu Nhiên Tổng Hợp Toàn Khóa (102 câu)`;
    dom.practiceChSelect.appendChild(compOpt);

    dom.practiceChSelect.addEventListener('change', (e) => {
      const val = e.target.value;
      state.practice.chapterId = val === 'comp' ? 'comp' : parseInt(val, 10);
      loadPracticeQuestions(state.practice.chapterId);
    });

    dom.practicePrevBtn.addEventListener('click', () => {
      if (state.practice.currentIndex > 0) {
        state.practice.currentIndex--;
        renderPracticeQuestion();
      }
    });

    dom.practiceNextBtn.addEventListener('click', () => {
      if (state.practice.currentIndex < state.practice.questions.length - 1) {
        state.practice.currentIndex++;
        renderPracticeQuestion();
      }
    });

    loadPracticeQuestions(state.practice.chapterId);
  }

  function loadPracticeQuestions(chapterId) {
    const allQs = window.SEG_QUESTIONS || [];
    const filterVal = chapterId.toString();

    state.practice.questions = allQs.filter(q => q.chapter.toString() === filterVal);
    state.practice.currentIndex = 0;
    state.practice.userAnswers = {};
    state.practice.score = { correct: 0, incorrect: 0 };

    updatePracticeStats();
    renderPracticeQuestion();
  }

  function renderPracticeQuestion() {
    const qList = state.practice.questions;
    if (!qList || qList.length === 0) {
      dom.practiceQText.textContent = 'Không tìm thấy câu hỏi cho chương này.';
      dom.practiceOptionsList.innerHTML = '';
      return;
    }

    if (dom.practiceQuestionCard) {
      dom.practiceQuestionCard.style.animation = 'none';
      void dom.practiceQuestionCard.offsetHeight;
      dom.practiceQuestionCard.style.animation = '';
    }

    const q = qList[state.practice.currentIndex];
    const total = qList.length;
    const currentNum = state.practice.currentIndex + 1;

    dom.practiceQBadge.textContent = `CÂU HỎI ${currentNum} / ${total}`;
    dom.practiceQChapterTag.textContent = q.chapter === 'comp' ? 'Tổng Hợp' : `Chương ${q.chapter}`;
    dom.practiceProgressText.textContent = `${currentNum} / ${total}`;

    dom.practiceQText.textContent = q.question;
    dom.practiceOptionsList.innerHTML = '';

    const letters = ['A', 'B', 'C', 'D', 'E'];
    const hasAnswered = state.practice.userAnswers.hasOwnProperty(q.id);
    const selectedAnswer = state.practice.userAnswers[q.id];

    q.options.forEach((optText, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      if (hasAnswered && selectedAnswer === idx) {
        btn.classList.add('selected');
      }

      if (hasAnswered) {
        btn.disabled = true;
        if (idx === q.answer) {
          btn.classList.add('correct-choice');
        } else if (selectedAnswer === idx && selectedAnswer !== q.answer) {
          btn.classList.add('incorrect-choice');
        }
      }

      btn.innerHTML = `
        <span class="option-letter">${letters[idx] || (idx + 1)}</span>
        <span>${optText}</span>
      `;

      btn.addEventListener('click', () => {
        if (!state.practice.userAnswers.hasOwnProperty(q.id)) {
          handlePracticeAnswer(q, idx);
        }
      });

      dom.practiceOptionsList.appendChild(btn);
    });

    // Explanation Box
    if (hasAnswered) {
      dom.practiceExplanationText.textContent = q.explanation || 'Không có giải thích chi tiết.';
      dom.practiceExplanationBox.classList.add('show');
    } else {
      dom.practiceExplanationBox.classList.remove('show');
    }

    // Nav Buttons State
    dom.practicePrevBtn.disabled = state.practice.currentIndex === 0;
    dom.practiceNextBtn.disabled = state.practice.currentIndex === total - 1;

    renderMath();
  }

  function handlePracticeAnswer(question, selectedIdx) {
    state.practice.userAnswers[question.id] = selectedIdx;

    if (selectedIdx === question.answer) {
      state.practice.score.correct++;
    } else {
      state.practice.score.incorrect++;
    }

    updatePracticeStats();
    renderPracticeQuestion();
  }

  function updatePracticeStats() {
    dom.practiceCorrectCount.textContent = state.practice.score.correct;
    dom.practiceIncorrectCount.textContent = state.practice.score.incorrect;

    const answeredTotal = state.practice.score.correct + state.practice.score.incorrect;
    const accuracy = answeredTotal > 0 ? Math.round((state.practice.score.correct / answeredTotal) * 100) : 0;
    dom.practiceAccuracy.textContent = `${accuracy}%`;
  }

  // --- TAB 3: TIMED EXAM ENGINE CONTROLLER (50 Qs / 50 Mins) ---
  function sampleRandomExamQuestions(count = 50) {
    const allQs = window.SEG_QUESTIONS || [];
    if (allQs.length <= count) return [...allQs];

    // Stratified random sampling: take 2 questions per chapter (17*2 = 34), plus 16 random from remainder
    const byChapter = {};
    allQs.forEach(q => {
      const ch = q.chapter.toString();
      if (!byChapter[ch]) byChapter[ch] = [];
      byChapter[ch].push(q);
    });

    const selected = [];
    const usedIds = new Set();

    // 2 questions from each of 17 chapters
    for (let c = 1; c <= 17; c++) {
      const pool = byChapter[c.toString()] || [];
      const shuffled = [...pool].sort(() => Math.random() - 0.5);
      const picks = shuffled.slice(0, 2);
      picks.forEach(p => {
        selected.push(p);
        usedIds.add(p.id);
      });
    }

    // Fill remaining up to 50 from the remaining pool
    const remainingPool = allQs.filter(q => !usedIds.has(q.id)).sort(() => Math.random() - 0.5);
    while (selected.length < count && remainingPool.length > 0) {
      selected.push(remainingPool.pop());
    }

    // Shuffle the final 50 selected questions
    return selected.sort(() => Math.random() - 0.5);
  }

  function startExam() {
    state.exam.questions = sampleRandomExamQuestions(50);
    state.exam.answers = {};
    state.exam.flagged.clear();
    state.exam.currentIndex = 0;
    state.exam.timeRemaining = 50 * 60; // 50 mins = 3000s
    state.exam.submitted = false;
    state.exam.active = true;
    state.exam.startTime = new Date();

    dom.examIntroScreen.style.display = 'none';
    dom.examIntroScreen.classList.remove('active');
    dom.examResultsScreen.style.display = 'none';
    dom.examResultsScreen.classList.remove('active');
    dom.examActiveScreen.style.display = 'flex';
    dom.examActiveScreen.classList.add('active');

    startExamTimer();
    renderExamPalette();
    renderExamQuestion();

    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
  }

  function startExamTimer() {
    clearInterval(state.exam.timerInterval);
    updateTimerDisplay();

    state.exam.timerInterval = setInterval(() => {
      state.exam.timeRemaining--;
      updateTimerDisplay();

      if (state.exam.timeRemaining <= 0) {
        clearInterval(state.exam.timerInterval);
        submitExam(true); // Auto submit on timeout
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(state.exam.timeRemaining / 60);
    const secs = state.exam.timeRemaining % 60;
    const formatted = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    dom.examTimerVal.textContent = formatted;

    dom.examTimerBox.classList.remove('timer-warning', 'timer-danger');
    if (state.exam.timeRemaining < 120) {
      dom.examTimerBox.classList.add('timer-danger');
    } else if (state.exam.timeRemaining < 600) {
      dom.examTimerBox.classList.add('timer-warning');
    }
  }

  function renderExamPalette() {
    dom.examPaletteGrid.innerHTML = '';

    state.exam.questions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      btn.textContent = (idx + 1).toString();

      if (idx === state.exam.currentIndex) {
        btn.classList.add('current');
      }
      if (state.exam.answers.hasOwnProperty(q.id)) {
        btn.classList.add('answered');
      }
      if (state.exam.flagged.has(q.id)) {
        btn.classList.add('flagged');
      }

      btn.addEventListener('click', () => {
        state.exam.currentIndex = idx;
        renderExamQuestion();
        renderExamPalette();
      });

      dom.examPaletteGrid.appendChild(btn);
    });
  }

  function renderExamQuestion() {
    const qList = state.exam.questions;
    if (!qList || qList.length === 0) return;

    const examCard = dom.examActiveScreen ? dom.examActiveScreen.querySelector('.question-card') : null;
    if (examCard) {
      examCard.style.animation = 'none';
      void examCard.offsetHeight;
      examCard.style.animation = '';
    }

    const q = state.exam.questions[state.exam.currentIndex];
    const total = state.exam.questions.length;
    const currentNum = state.exam.currentIndex + 1;

    dom.examQCounter.textContent = `Câu ${currentNum} / ${total}`;
    dom.examCurrentChBadge.textContent = q.chapter === 'comp' ? 'Tổng Hợp' : `Chương ${q.chapter}`;

    // Flag button update
    const isFlagged = state.exam.flagged.has(q.id);
    dom.examFlagText.textContent = isFlagged ? 'Bỏ cắm cờ' : 'Cắm cờ';
    dom.examFlagBtn.style.color = isFlagged ? 'var(--accent-amber)' : 'inherit';

    dom.examQText.textContent = q.question;
    dom.examOptionsList.innerHTML = '';

    const letters = ['A', 'B', 'C', 'D', 'E'];
    const currentAnswer = state.exam.answers[q.id];

    q.options.forEach((optText, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      if (currentAnswer === idx) {
        btn.classList.add('selected');
      }

      btn.innerHTML = `
        <span class="option-letter">${letters[idx] || (idx + 1)}</span>
        <span>${optText}</span>
      `;

      btn.addEventListener('click', () => {
        state.exam.answers[q.id] = idx;
        renderExamQuestion();
        renderExamPalette();
      });

      dom.examOptionsList.appendChild(btn);
    });

    dom.examPrevBtn.disabled = state.exam.currentIndex === 0;
    dom.examNextBtn.disabled = state.exam.currentIndex === total - 1;

    renderMath();
  }

  function toggleExamFlag() {
    const q = state.exam.questions[state.exam.currentIndex];
    if (state.exam.flagged.has(q.id)) {
      state.exam.flagged.delete(q.id);
    } else {
      state.exam.flagged.add(q.id);
    }
    renderExamQuestion();
    renderExamPalette();
  }

  function submitExam(isAuto = false) {
    clearInterval(state.exam.timerInterval);
    state.exam.submitted = true;
    state.exam.active = false;
    state.exam.endTime = new Date();

    dom.examActiveScreen.classList.remove('active');
    dom.examActiveScreen.style.display = 'none';
    dom.examResultsScreen.classList.add('active');
    dom.examResultsScreen.style.display = 'block';

    calculateAndRenderExamResults();
    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
  }

  function calculateAndRenderExamResults() {
    const questions = state.exam.questions;
    let correct = 0;
    let incorrect = 0;
    let unanswered = 0;

    const chapterStats = {}; // { ch: { total: 0, correct: 0 } }

    questions.forEach(q => {
      const ch = q.chapter.toString();
      if (!chapterStats[ch]) {
        chapterStats[ch] = { total: 0, correct: 0 };
      }
      chapterStats[ch].total++;

      const userAns = state.exam.answers[q.id];
      if (userAns === undefined) {
        unanswered++;
      } else if (userAns === q.answer) {
        correct++;
        chapterStats[ch].correct++;
      } else {
        incorrect++;
      }
    });

    const total = questions.length;
    const accuracy = Math.round((correct / total) * 100);

    // Score Banner
    dom.resultScoreDisplay.textContent = `${correct} / ${total}`;
    dom.resMetricAccuracy.textContent = `${accuracy}%`;
    dom.resMetricCorrect.textContent = correct.toString();
    dom.resMetricIncorrect.textContent = (incorrect + unanswered).toString();

    // Time elapsed
    const elapsedSecs = Math.max(0, 3000 - state.exam.timeRemaining);
    const mins = Math.floor(elapsedSecs / 60);
    const secs = elapsedSecs % 60;
    dom.resMetricTime.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    // Pass / Fail Badge
    if (accuracy >= 80) {
      dom.resultStatusBadge.className = 'results-status-badge status-passed';
      dom.resultStatusBadge.textContent = '🎉 ĐẠT XUẤT SẮC (PASS WITH DISTINCTION)';
    } else if (accuracy >= 65) {
      dom.resultStatusBadge.className = 'results-status-badge status-passed';
      dom.resultStatusBadge.textContent = '✅ ĐẠT YÊU CẦU (PASS)';
    } else {
      dom.resultStatusBadge.className = 'results-status-badge status-failed';
      dom.resultStatusBadge.textContent = '⚠️ CHƯA ĐẠT (NEEDS REVIEW)';
    }

    // Render Chapter Mastery
    renderChapterMastery(chapterStats);

    // Render Review Questions
    renderExamReviewList();
  }

  function renderChapterMastery(chapterStats) {
    dom.examMasteryList.innerHTML = '';
    const weakChapters = [];

    const keys = Object.keys(chapterStats).sort((a, b) => {
      if (a === 'comp') return 1;
      if (b === 'comp') return -1;
      return parseInt(a, 10) - parseInt(b, 10);
    });

    keys.forEach(chKey => {
      const stat = chapterStats[chKey];
      const acc = Math.round((stat.correct / stat.total) * 100);
      const chName = chKey === 'comp' ? 'Tổng hợp liên chương' : `Chương ${chKey}`;

      let tagClass = 'tag-high';
      let tagText = 'Thành thạo';
      let barColor = 'var(--accent-emerald)';

      if (acc < 50) {
        tagClass = 'tag-low';
        tagText = 'Cần ôn lại';
        barColor = 'var(--accent-rose)';
        weakChapters.push({ key: chKey, name: chName, acc });
      } else if (acc < 80) {
        tagClass = 'tag-med';
        tagText = 'Khá';
        barColor = 'var(--accent-amber)';
      }

      const row = document.createElement('div');
      row.className = 'mastery-row';
      row.innerHTML = `
        <div class="mastery-ch-name" title="${chName}">${chName}</div>
        <div class="mastery-bar-outer">
          <div class="mastery-bar-fill" style="width: ${acc}%; background: ${barColor};"></div>
        </div>
        <div class="mastery-score-text">${stat.correct}/${stat.total} (${acc}%)</div>
        <div class="mastery-tag ${tagClass}">${tagText}</div>
      `;

      dom.examMasteryList.appendChild(row);
    });

    // Render Study Recommendations
    if (weakChapters.length === 0) {
      dom.studyRecommendationsContent.innerHTML = `
        <p style="color: var(--accent-emerald); font-weight: 600;">
          🌟 Xuất sắc! Bạn nắm rất vững kiến thức ở tất cả các chương. Hãy duy trì phong độ và luyện thêm các đề thi mới để đạt điểm tuyệt đối trong kỳ thi chính thức!
        </p>
      `;
    } else {
      let recHtml = `<p style="margin-bottom: 0.75rem;">Bạn nên dành thời gian ôn lại các chương sau có tỷ lệ làm đúng dưới 50%:</p><ul style="padding-left: 1.25rem;">`;
      weakChapters.forEach(wc => {
        recHtml += `
          <li style="margin-bottom: 0.4rem;">
            <strong>${wc.name}</strong> (Chỉ đúng ${wc.acc}%): 
            <button class="btn-secondary" style="padding: 0.2rem 0.6rem; font-size: 0.75rem; margin-left: 0.5rem;" onclick="window.SEG_APP.openChapterTheory('${wc.key}')">
              📖 Đọc lý thuyết Chương này
            </button>
          </li>
        `;
      });
      recHtml += `</ul>`;
      dom.studyRecommendationsContent.innerHTML = recHtml;
    }
  }

  function renderExamReviewList() {
    dom.examReviewQuestionsList.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D', 'E'];
    const filter = state.exam.reviewFilter;

    state.exam.questions.forEach((q, idx) => {
      const userAns = state.exam.answers[q.id];
      const isCorrect = userAns === q.answer;
      const isFlagged = state.exam.flagged.has(q.id);

      if (filter === 'wrong' && isCorrect) return;
      if (filter === 'correct' && !isCorrect) return;
      if (filter === 'flagged' && !isFlagged) return;

      const card = document.createElement('div');
      card.className = 'question-card';

      let statusBadge = isCorrect
        ? `<span class="badge-tag" style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); border-color: var(--accent-emerald);">✓ Đúng</span>`
        : `<span class="badge-tag" style="background: rgba(239, 68, 68, 0.2); color: var(--accent-rose); border-color: var(--accent-rose);">✗ Sai</span>`;

      if (userAns === undefined) {
        statusBadge = `<span class="badge-tag" style="background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); border-color: var(--accent-amber);">⚪ Bỏ trống</span>`;
      }

      let optionsHtml = '';
      q.options.forEach((optText, oIdx) => {
        let optClass = 'option-btn';
        if (oIdx === q.answer) {
          optClass += ' correct-choice';
        } else if (userAns === oIdx && userAns !== q.answer) {
          optClass += ' incorrect-choice';
        }

        optionsHtml += `
          <div class="${optClass}" style="cursor: default;">
            <span class="option-letter">${letters[oIdx] || (oIdx + 1)}</span>
            <span>${optText}</span>
          </div>
        `;
      });

      card.innerHTML = `
        <div class="q-meta-row">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="q-num-badge">CÂU ${idx + 1}</span>
            <span class="badge-tag">${q.chapter === 'comp' ? 'Tổng Hợp' : 'Chương ' + q.chapter}</span>
            ${isFlagged ? '<span class="badge-tag" style="color: var(--accent-amber);">🔖 Đã cắm cờ</span>' : ''}
          </div>
          <div>${statusBadge}</div>
        </div>

        <div class="q-text">${q.question}</div>
        <div class="options-list">${optionsHtml}</div>

        <div class="explanation-box show">
          <div class="explanation-title">
            <span>💡</span> Giải thích học thuật (Academic Explanation)
          </div>
          <div class="explanation-text">${q.explanation || 'Không có giải thích chi tiết.'}</div>
        </div>
      `;

      dom.examReviewQuestionsList.appendChild(card);
    });

    renderMath();
  }

  // --- TAB 4: QUESTION BANK EXPLORER (952 Qs) ---
  function initBankTab() {
    const chapters = window.SEG_CHAPTERS || [];
    dom.bankChapterFilter.innerHTML = '<option value="all">Tất cả các chương (952 câu)</option>';

    chapters.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch.id.toString();
      const title = ch.title || ch.title_en || `Chapter ${ch.id}`;
      opt.textContent = `Chương ${ch.id}: ${title}`;
      dom.bankChapterFilter.appendChild(opt);
    });

    const compOpt = document.createElement('option');
    compOpt.value = 'comp';
    compOpt.textContent = 'Tổng hợp liên chương (102 câu)';
    dom.bankChapterFilter.appendChild(compOpt);

    dom.bankChapterFilter.addEventListener('change', (e) => {
      state.bank.filterChapter = e.target.value;
      renderQuestionBank();
    });

    dom.bankSearchInput.addEventListener('input', (e) => {
      state.bank.searchQuery = e.target.value.toLowerCase().trim();
      renderQuestionBank();
    });

    dom.bankToggleAnswersBtn.addEventListener('click', () => {
      state.bank.showAnswers = !state.bank.showAnswers;
      dom.bankToggleAnswersBtn.textContent = state.bank.showAnswers
        ? '🙈 Ẩn tất cả đáp án'
        : '👁️ Hiện tất cả đáp án';
      renderQuestionBank();
    });

    renderQuestionBank();
  }

  function renderQuestionBank() {
    const allQs = window.SEG_QUESTIONS || [];
    const filterCh = state.bank.filterChapter;
    const search = state.bank.searchQuery;

    const filtered = allQs.filter(q => {
      const matchCh = filterCh === 'all' || q.chapter.toString() === filterCh;
      const matchSearch = !search ||
        q.question.toLowerCase().includes(search) ||
        q.id.toLowerCase().includes(search) ||
        q.options.some(opt => opt.toLowerCase().includes(search));
      return matchCh && matchSearch;
    });

    dom.bankCountInfo.textContent = `Hiển thị ${filtered.length} / ${allQs.length} câu hỏi`;
    dom.bankQuestionsContainer.innerHTML = '';

    const letters = ['A', 'B', 'C', 'D', 'E'];
    const limit = Math.min(filtered.length, 100); // Render first 100 matches to keep DOM light

    for (let i = 0; i < limit; i++) {
      const q = filtered[i];
      const card = document.createElement('div');
      card.className = 'question-card reveal-on-scroll';

      let optionsHtml = '';
      q.options.forEach((optText, oIdx) => {
        const isCorrect = state.bank.showAnswers && oIdx === q.answer;
        optionsHtml += `
          <div class="option-btn ${isCorrect ? 'correct-choice' : ''}" style="cursor: default;">
            <span class="option-letter">${letters[oIdx] || (oIdx + 1)}</span>
            <span>${optText}</span>
          </div>
        `;
      });

      card.innerHTML = `
        <div class="q-meta-row">
          <span class="q-num-badge">${q.id}</span>
          <span class="badge-tag">${q.chapter === 'comp' ? 'Tổng Hợp' : 'Chương ' + q.chapter}</span>
        </div>
        <div class="q-text">${q.question}</div>
        <div class="options-list">${optionsHtml}</div>
        ${state.bank.showAnswers ? `
          <div class="explanation-box show">
            <div class="explanation-title">💡 Giải thích</div>
            <div class="explanation-text">${q.explanation || ''}</div>
          </div>
        ` : ''}
      `;

      dom.bankQuestionsContainer.appendChild(card);
    }

    if (filtered.length > 100) {
      const note = document.createElement('div');
      note.style.textAlign = 'center';
      note.style.padding = '1.5rem';
      note.style.color = 'var(--text-muted)';
      note.textContent = `(Đang hiển thị 100 câu đầu tiên trong tổng số ${filtered.length} câu phù hợp. Vui lòng lọc theo chương hoặc tìm kiếm để thu hẹp kết quả.)`;
      dom.bankQuestionsContainer.appendChild(note);
    }

    renderMath();
    if (window.SEG_ANIMATIONS) {
      window.SEG_ANIMATIONS.observeScrollReveals(dom.bankQuestionsContainer);
    }
  }

  // --- TAB 5: GLOSSARY CONTROLLER (83 Terms) ---
  function initGlossaryTab() {
    dom.glossarySearchInput.addEventListener('input', (e) => {
      state.glossary.searchQuery = e.target.value.toLowerCase().trim();
      renderGlossary();
    });

    renderGlossary();
  }

  function renderGlossary() {
    const list = window.SEG_GLOSSARY || [];
    const query = state.glossary.searchQuery;

    const filtered = list.filter(item => {
      return !query ||
        item.term.toLowerCase().includes(query) ||
        item.vietnamese.toLowerCase().includes(query) ||
        item.definition.toLowerCase().includes(query);
    });

    dom.glossaryCountInfo.textContent = `${filtered.length} / ${list.length} thuật ngữ`;
    dom.glossaryItemsGrid.innerHTML = '';

    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = 'glossary-card reveal-on-scroll';

      card.innerHTML = `
        <div class="glossary-term">${item.term}</div>
        <div class="glossary-vn">${item.vietnamese}</div>
        <div class="glossary-def">${item.definition}</div>
        <div class="glossary-chapter-tag">
          ${item.chapter === 'comp' ? 'Tổng Hợp' : 'Chương ' + item.chapter}
        </div>
      `;

      dom.glossaryItemsGrid.appendChild(card);
    });

    if (window.SEG_ANIMATIONS) {
      window.SEG_ANIMATIONS.observeScrollReveals(dom.glossaryItemsGrid);
    }
  }

  // --- GLOBAL SEARCH MODAL (Ctrl + K) ---
  function openSearchModal() {
    dom.searchModal.classList.add('show', 'active');
    dom.globalSearchInput.value = '';
    dom.globalSearchInput.focus();
    renderSearchResults('');
  }

  function closeSearchModal() {
    dom.searchModal.classList.remove('show', 'active');
  }

  function renderSearchResults(query) {
    dom.searchModalResults.innerHTML = '';
    if (!query) {
      dom.searchModalResults.innerHTML = `
        <div style="padding: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
          Gõ từ khóa để tìm nhanh 17 chương học, thuật ngữ hoặc câu hỏi thi...
        </div>
      `;
      return;
    }

    const q = query.toLowerCase().trim();
    const chapters = window.SEG_CHAPTERS || [];
    const glossary = window.SEG_GLOSSARY || [];
    const questions = window.SEG_QUESTIONS || [];

    const results = [];

    // Search Chapters
    chapters.forEach(ch => {
      const title = ch.title || ch.title_en || `Chapter ${ch.id}`;
      const titleVn = ch.title_vn || '';
      if (title.toLowerCase().includes(q) || titleVn.toLowerCase().includes(q) || ch.id.toString() === q) {
        results.push({
          type: 'chapter',
          title: `📖 Chương ${ch.id}: ${title}`,
          desc: titleVn,
          action: () => {
            selectChapter(ch.id);
            switchTab('knowledge');
            closeSearchModal();
          }
        });
      }
    });

    // Search Glossary
    glossary.forEach(g => {
      if (g.term.toLowerCase().includes(q) || g.vietnamese.toLowerCase().includes(q)) {
        results.push({
          type: 'glossary',
          title: `📚 ${g.term} (${g.vietnamese})`,
          desc: g.definition.slice(0, 100) + '...',
          action: () => {
            state.glossary.searchQuery = g.term.toLowerCase();
            dom.glossarySearchInput.value = g.term;
            renderGlossary();
            switchTab('glossary');
            closeSearchModal();
          }
        });
      }
    });

    // Search Questions
    questions.forEach(ques => {
      if (ques.question.toLowerCase().includes(q)) {
        results.push({
          type: 'question',
          title: `❓ [${ques.id}] ${ques.question.slice(0, 85)}...`,
          desc: `Chương ${ques.chapter}`,
          action: () => {
            state.bank.filterChapter = ques.chapter.toString();
            state.bank.searchQuery = ques.id.toLowerCase();
            state.bank.showAnswers = true;
            dom.bankChapterFilter.value = ques.chapter.toString();
            dom.bankSearchInput.value = ques.id;
            renderQuestionBank();
            switchTab('bank');
            closeSearchModal();
          }
        });
      }
    });

    if (results.length === 0) {
      dom.searchModalResults.innerHTML = `
        <div style="padding: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.85rem;">
          Không tìm thấy kết quả phù hợp cho "${query}".
        </div>
      `;
      return;
    }

    results.slice(0, 15).forEach(res => {
      const item = document.createElement('div');
      item.className = 'search-result-item';
      item.innerHTML = `
        <div class="search-result-title">${res.title}</div>
        <div class="search-result-desc">${res.desc}</div>
      `;
      item.addEventListener('click', res.action);
      dom.searchModalResults.appendChild(item);
    });
  }

  // --- EVENT BINDINGS ---
  function bindEvents() {
    // Nav tab clicks
    dom.navTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        switchTab(tab.dataset.tab);
      });
    });

    // Brand logo returns to knowledge
    dom.brandLogo.addEventListener('click', () => {
      switchTab('knowledge');
    });

    // Theme toggle
    dom.themeToggleBtn.addEventListener('click', toggleTheme);

    // Chapter filter search
    dom.chapterSearchInput.addEventListener('input', (e) => {
      renderChapterNav(e.target.value);
    });

    // Exam buttons
    dom.startExamBtn.addEventListener('click', startExam);
    dom.retakeExamBtn.addEventListener('click', startExam);
    dom.examFlagBtn.addEventListener('click', toggleExamFlag);

    dom.examPrevBtn.addEventListener('click', () => {
      if (state.exam.currentIndex > 0) {
        state.exam.currentIndex--;
        renderExamQuestion();
        renderExamPalette();
      }
    });

    dom.examNextBtn.addEventListener('click', () => {
      if (state.exam.currentIndex < state.exam.questions.length - 1) {
        state.exam.currentIndex++;
        renderExamQuestion();
        renderExamPalette();
      }
    });

    // Early submission modal
    dom.examSubmitEarlyBtn.addEventListener('click', () => {
      const answeredCount = Object.keys(state.exam.answers).length;
      const unanswered = state.exam.questions.length - answeredCount;

      if (unanswered > 0) {
        dom.confirmUnansweredCount.textContent = unanswered.toString();
        dom.confirmUnansweredAlert.style.display = 'block';
      } else {
        dom.confirmUnansweredAlert.style.display = 'none';
      }

      dom.submitConfirmModal.classList.add('show', 'active');
    });

    dom.closeConfirmModalBtn.addEventListener('click', () => {
      dom.submitConfirmModal.classList.remove('show', 'active');
    });

    dom.confirmCancelBtn.addEventListener('click', () => {
      dom.submitConfirmModal.classList.remove('show', 'active');
    });

    dom.confirmSubmitBtn.addEventListener('click', () => {
      dom.submitConfirmModal.classList.remove('show', 'active');
      submitExam(false);
    });

    // Review Filters in Exam Results
    dom.reviewFilterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        dom.reviewFilterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        state.exam.reviewFilter = chip.dataset.reviewFilter;
        renderExamReviewList();
      });
    });

    // Global Search Modal triggers
    dom.openSearchModalBtn.addEventListener('click', openSearchModal);

    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openSearchModal();
      }
      if (e.key === 'Escape') {
        closeSearchModal();
        dom.submitConfirmModal.classList.remove('show', 'active');
      }
    });

    dom.searchModal.addEventListener('click', (e) => {
      if (e.target === dom.searchModal) closeSearchModal();
    });

    dom.globalSearchInput.addEventListener('input', (e) => {
      renderSearchResults(e.target.value);
    });
  }

  // --- PUBLIC API EXPOSURE ---
  window.SEG_APP = {
    switchTab,
    selectChapter,
    openChapterTheory: (chKey) => {
      const id = chKey === 'comp' ? 1 : parseInt(chKey, 10);
      selectChapter(id);
      switchTab('knowledge');
    }
  };

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
