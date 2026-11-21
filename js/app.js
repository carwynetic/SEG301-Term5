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
      source: 'fe', // 'fe' (312 Slide bank - 293 questions) | 'bank' (694 questions)
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
    examHistory: [],

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
    examSourceRadios: document.querySelectorAll('input[name="exam-source-radio"]'),
    sourceCardFe: document.getElementById('source-card-fe'),
    sourceCardBank: document.getElementById('source-card-bank'),
    examHistoryContainer: document.getElementById('exam-history-container'),
    examViewImageBtn: document.getElementById('exam-view-image-btn'),
    backToIntroBtn: document.getElementById('back-to-intro-btn'),

    // Lightbox Modal
    imageViewerModal: document.getElementById('image-viewer-modal'),
    imageModalImg: document.getElementById('image-modal-img'),
    imageModalTitle: document.getElementById('image-modal-title'),
    btnCloseImageModal: document.getElementById('btn-close-image-modal'),
    examSourceRadios: document.querySelectorAll('input[name="exam-source-radio"]'),
    sourceCardFe: document.getElementById('source-card-fe'),
    sourceCardBank: document.getElementById('source-card-bank'),
    examHistoryContainer: document.getElementById('exam-history-container'),
    examViewImageBtn: document.getElementById('exam-view-image-btn'),
    backToIntroBtn: document.getElementById('back-to-intro-btn'),

    // Lightbox Modal
    imageViewerModal: document.getElementById('image-viewer-modal'),
    imageModalImg: document.getElementById('image-modal-img'),
    imageModalTitle: document.getElementById('image-modal-title'),
    btnCloseImageModal: document.getElementById('btn-close-image-modal'),
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
    const scoreDisplay = document.getElementById('result-score-display') || document.getElementById('results-score-display');

    // Refresh dynamic DOM bindings
    dom.imageViewerModal = document.getElementById('image-viewer-modal');
    dom.imageModalImg = document.getElementById('image-modal-img');
    dom.imageModalTitle = document.getElementById('image-modal-title');
    dom.btnCloseImageModal = document.getElementById('btn-close-image-modal');
    dom.examViewImageBtn = document.getElementById('exam-view-image-btn');
    dom.backToIntroBtn = document.getElementById('back-to-intro-btn');
    dom.examHistoryContainer = document.getElementById('exam-history-container');
    dom.sourceCardFe = document.getElementById('source-card-fe');
    dom.sourceCardBank = document.getElementById('source-card-bank');
    dom.examSourceRadios = document.querySelectorAll('input[name="exam-source-radio"]');
    initTheme();
    initMermaid();
    bindEvents();
    renderChapterNav();
    loadChapterKnowledge(state.activeChapterId);
    initPracticeTab();
    initBankTab();
    initGlossaryTab();
    state.examHistory = loadExamHistory();
    renderExamHistory();
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
        <span>${escapeHtmlText(optText)}</span>
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
  // Multi-choice & Single-choice Helper Utilities
  function getUserChoices(qId, answersObj) {
    if (!answersObj) return [];
    const ans = answersObj[qId];
    if (ans === undefined || ans === null) return [];
    return Array.isArray(ans) ? ans : [ans];
  }

  function isAnswerCorrect(q, userAns) {
    if (userAns === undefined || userAns === null) return false;
    const correctChoices = Array.isArray(q.correct_choices)
      ? q.correct_choices
      : (Array.isArray(q.correct) ? q.correct : [q.correct !== undefined ? q.correct : q.answer]);
    const userChoices = Array.isArray(userAns) ? userAns : [userAns];

    if (correctChoices.length !== userChoices.length) return false;
    const cSet = new Set(correctChoices);
    return userChoices.every(u => cSet.has(u));
  }


  // Lightbox Image Viewer
  function openImageModal(src, title) {
    if (!dom.imageViewerModal || !dom.imageModalImg) return;
    dom.imageModalImg.src = src;
    if (dom.imageModalTitle) {
      dom.imageModalTitle.innerHTML = `<i class="fas fa-image"></i> ${title || 'Chi tiết hình ảnh slide gốc'}`;
    }
    dom.imageViewerModal.classList.add('active');
  }

  function closeImageModal() {
    if (dom.imageViewerModal) {
      dom.imageViewerModal.classList.remove('active');
    }
  }

  // Escape HTML special characters so <...> tuples (e.g. Slide 68) and < math signs render visibly
  function escapeHtmlText(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // Question Normalization & Deduplication Helper
  function normalizeQuestionKey(txt) {
    if (!txt) return '';
    return txt.toLowerCase()
      .replace(/\(choose \d+ answers?\)/gi, '')
      .replace(/\(?\d+\s*options?\)?/gi, '')
      .replace(/check all correct answers\.?/gi, '')
      .replace(/[^a-z0-9]/g, '')
      .trim();
  }

  // Uniform Fisher-Yates shuffle
  function shuffleArray(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // Question Sampling Engine (100% Guaranteed ZERO Duplicate Questions per Exam)
  function sampleRandomExamQuestions(count = 50) {
    if (state.exam.source === 'fe') {
      const feQs = (window.SEG_FE_QUESTIONS || []).filter(q => !q.is_info && q.question && q.options && q.options.length >= 2);
      if (!feQs.length) {
        console.warn('SEG_FE_QUESTIONS not loaded, falling back to SEG_QUESTIONS');
        return sampleStratifiedBankQuestions(count);
      }
      
      // Group slides by normalized question text to eliminate all duplicate questions
      const uniqueMap = new Map();
      feQs.forEach(q => {
        const key = normalizeQuestionKey(q.question);
        if (!key) return;
        if (!uniqueMap.has(key)) {
          uniqueMap.set(key, []);
        }
        uniqueMap.get(key).push(q);
      });

      // From each duplicate group, select exactly 1 slide question at random
      const deduplicatedPool = [];
      uniqueMap.forEach((candidates) => {
        const picked = candidates[Math.floor(Math.random() * candidates.length)];
        deduplicatedPool.push(picked);
      });

      // True uniform Fisher-Yates shuffle
      const shuffled = shuffleArray(deduplicatedPool);
      return shuffled.slice(0, Math.min(count, shuffled.length));
    } else {
      return sampleStratifiedBankQuestions(count);
    }
  }

  function sampleStratifiedBankQuestions(count = 50) {
    const allQs = (window.SEG_QUESTIONS || []).filter(q => q.question && q.options && q.options.length >= 2);
    if (allQs.length <= count) return shuffleArray(allQs);

    // Deduplicate bank questions by normalized question key
    const uniqueMap = new Map();
    allQs.forEach(q => {
      const key = normalizeQuestionKey(q.question);
      if (!key) return;
      if (!uniqueMap.has(key)) {
        uniqueMap.set(key, q);
      }
    });
    const deduplicatedBank = Array.from(uniqueMap.values());

    const byChapter = {};
    deduplicatedBank.forEach(q => {
      const ch = q.chapter.toString();
      if (!byChapter[ch]) byChapter[ch] = [];
      byChapter[ch].push(q);
    });

    const selected = [];
    const usedKeys = new Set();

    // 3 questions from each of 12 chapters (36)
    for (let c = 1; c <= 12; c++) {
      const pool = byChapter[c.toString()] || [];
      const shuffled = shuffleArray(pool);
      const picks = shuffled.slice(0, 3);
      picks.forEach(p => {
        selected.push(p);
        usedKeys.add(normalizeQuestionKey(p.question));
      });
    }

    // Fill remaining up to count (50) from the remaining pool
    const remainingPool = shuffleArray(deduplicatedBank.filter(q => !usedKeys.has(normalizeQuestionKey(q.question))));
    while (selected.length < count && remainingPool.length > 0) {
      selected.push(remainingPool.pop());
    }

    return shuffleArray(selected);
  }

  // Exam History Management
  function loadExamHistory() {
    try {
      const saved = localStorage.getItem('seg301_exam_history');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      console.error('Failed to parse exam history:', e);
      return [];
    }
  }

  function saveExamHistory(record) {
    state.examHistory.unshift(record);
    if (state.examHistory.length > 50) {
      state.examHistory = state.examHistory.slice(0, 50);
    }
    try {
      localStorage.setItem('seg301_exam_history', JSON.stringify(state.examHistory));
    } catch (e) {
      console.warn('LocalStorage quota exceeded or blocked:', e);
    }
  }

  function clearExamHistory() {
    if (confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử các lần thi thử không? Dữ liệu đã xóa không thể khôi phục.')) {
      state.examHistory = [];
      localStorage.removeItem('seg301_exam_history');
      renderExamHistory();
    }
  }

  function renderExamHistory() {
    if (!dom.examHistoryContainer) return;
    const history = state.examHistory || [];
    if (history.length === 0) {
      dom.examHistoryContainer.innerHTML = `
        <div class="exam-history-header">
          <h3><i class="fas fa-history"></i> Lịch Sử Thi Thử & Đánh Giá Năng Lực</h3>
        </div>
        <div style="background: var(--bg-card); border: 1px dashed var(--border-color); border-radius: var(--radius-md); padding: 2rem; text-align: center; color: var(--text-secondary);">
          <i class="fas fa-clipboard-list" style="font-size: 2rem; margin-bottom: 0.75rem; color: var(--text-muted); display: block;"></i>
          <p style="margin: 0; font-weight: 500;">Chưa có lượt thi thử nào được ghi nhận.</p>
          <p style="margin-top: 0.4rem; font-size: 0.85rem; color: var(--text-muted);">Hãy chọn nguồn đề thi bên trên và bấm "Bắt đầu làm bài thi" để kiểm tra kiến thức và ghi log tiến độ ôn tập tranh Cóc Vàng!</p>
        </div>
      `;
      return;
    }

    const total = history.length;
    const scores = history.map(h => h.score || 0);
    const bestScore = Math.max(...scores);
    const avgScore = scores.reduce((a, b) => a + b, 0) / total;
    const goldCount = history.filter(h => (h.score || 0) >= 8.0).length;
    const goldRate = Math.round((goldCount / total) * 100);

    let rowsHtml = '';
    history.forEach((rec, idx) => {
      const isGold = (rec.score || 0) >= 8.0;
      const isPass = (rec.score || 0) >= 6.5;
      const pillClass = isGold ? 'badge-score-pass' : (isPass ? 'badge-score-pass' : 'badge-score-fail');
      const sourceBadgeClass = rec.source === 'fe' ? 'badge-source-fe' : 'badge-source-bank';
      const sourceText = rec.source === 'fe' ? 'FE 312 Slide' : 'Ngân hàng 12 Chương';

      rowsHtml += `
        <tr>
          <td style="font-weight: 700; color: var(--text-secondary); text-align: center;">#${total - idx}</td>
          <td><span style="font-family: var(--font-mono); font-size: 0.85rem;">${rec.formattedDate || rec.date?.slice(0, 16)}</span></td>
          <td><span class="badge-source ${sourceBadgeClass}">${sourceText}</span></td>
          <td><span class="badge-score-pill ${pillClass}">${rec.score.toFixed(1)} / 10.0</span></td>
          <td><strong>${rec.correctCount}</strong> / ${rec.totalQuestions} (${rec.accuracy}%)</td>
          <td><span style="font-family: var(--font-mono);">${rec.formattedTime || 'N/A'}</span></td>
          <td>
            <button class="btn-history-review" onclick="window.SEG_APP.viewExamRecord('${rec.id}')">
              <i class="fas fa-eye"></i> Xem lại
            </button>
          </td>
        </tr>
      `;
    });

    dom.examHistoryContainer.innerHTML = `
      <div class="exam-history-header">
        <h3><i class="fas fa-history"></i> Lịch Sử Thi Thử & Đánh Giá Năng Lực (${total} lần thi)</h3>
        <button class="btn-history-clear" onclick="window.SEG_APP.clearExamHistory()">
          <i class="fas fa-trash-alt"></i> Xóa lịch sử
        </button>
      </div>

      <div class="exam-history-summary">
        <div class="history-metric">
          <div class="history-metric-val" style="color: var(--primary);">${total}</div>
          <div class="history-metric-lbl">Tổng Lượt Thi</div>
        </div>
        <div class="history-metric">
          <div class="history-metric-val" style="color: var(--accent-emerald);">${bestScore.toFixed(1)}</div>
          <div class="history-metric-lbl">Điểm Cao Nhất (/10)</div>
        </div>
        <div class="history-metric">
          <div class="history-metric-val" style="color: var(--accent-cyan);">${avgScore.toFixed(1)}</div>
          <div class="history-metric-lbl">Điểm Trung Bình (/10)</div>
        </div>
        <div class="history-metric">
          <div class="history-metric-val" style="color: var(--accent-amber);">${goldRate}%</div>
          <div class="history-metric-lbl">Tỷ Lệ Đạt Cóc Vàng (≥8.0)</div>
        </div>
      </div>

      <div class="exam-history-table-wrap">
        <table class="exam-history-table">
          <thead>
            <tr>
              <th style="text-align: center; width: 50px;">#</th>
              <th>Ngày Giờ Thi</th>
              <th>Nguồn Đề</th>
              <th>Điểm Số</th>
              <th>Câu Đúng</th>
              <th>Thời Lượng</th>
              <th>Thao Tác</th>
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;
  }

  function viewExamRecord(recordId) {
    const rec = (state.examHistory || []).find(r => r.id === recordId);
    if (!rec) return;

    state.exam.questions = rec.questions;
    state.exam.answers = rec.answers || {};
    state.exam.flagged = new Set(rec.flagged || []);
    state.exam.source = rec.source || 'fe';
    state.exam.timeRemaining = 3000 - (rec.timeSpent || 0);

    dom.examIntroScreen.style.display = 'none';
    dom.examIntroScreen.classList.remove('active');
    dom.examActiveScreen.style.display = 'none';
    dom.examActiveScreen.classList.remove('active');
    dom.examResultsScreen.style.display = 'block';
    dom.examResultsScreen.classList.add('active');

    calculateAndRenderExamResults(false);
    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
  }

  function returnToExamIntro() {
    dom.examResultsScreen.style.display = 'none';
    dom.examResultsScreen.classList.remove('active');
    dom.examActiveScreen.style.display = 'none';
    dom.examActiveScreen.classList.remove('active');
    dom.examIntroScreen.style.display = 'block';
    dom.examIntroScreen.classList.add('active');

    renderExamHistory();
    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
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
      const uChoices = getUserChoices(q.id, state.exam.answers);
      if (uChoices.length > 0) {
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
    const isMulti = !!q.is_multi;
    const requiredChoices = q.required_choices || (isMulti ? 2 : 1);
    const userChoices = getUserChoices(q.id, state.exam.answers);

    dom.examQCounter.textContent = `Câu ${currentNum} / ${total}`;
    
    // Badge info (Chapter / Slide & Multi-choice indicator)
    const baseBadge = q.slide ? `Slide ${q.slide}` : (q.chapter === 'comp' ? 'Tổng Hợp' : `Chương ${q.chapter}`);
    if (isMulti) {
      const countText = `${userChoices.length}/${requiredChoices}`;
      const color = userChoices.length === requiredChoices ? 'var(--accent-emerald)' : '#f59e0b';
      dom.examCurrentChBadge.innerHTML = `${baseBadge} &bull; <span style="color: ${color}; font-weight: 700;"><i class="fas fa-check-double"></i> Chọn đúng ${requiredChoices} đáp án (${countText} đã chọn)</span>`;
    } else {
      dom.examCurrentChBadge.textContent = baseBadge;
    }

    // Flag button update
    const isFlagged = state.exam.flagged.has(q.id);
    dom.examFlagText.textContent = isFlagged ? 'Bỏ cắm cờ' : 'Cắm cờ';
    dom.examFlagBtn.style.color = isFlagged ? 'var(--accent-amber)' : 'inherit';

    dom.examQText.textContent = q.question;
    dom.examOptionsList.innerHTML = '';

    const letters = ['A', 'B', 'C', 'D', 'E'];

    q.options.forEach((optText, idx) => {
      const btn = document.createElement('button');
      btn.className = 'option-btn';
      const isSelected = userChoices.includes(idx);
      if (isSelected) {
        btn.classList.add('selected');
      }

      let checkIconHtml = '';
      if (isMulti) {
        checkIconHtml = `<span class="option-check-icon" style="margin-right: 0.5rem; color: ${isSelected ? 'var(--primary)' : 'var(--text-muted)'}; font-size: 1.05rem;"><i class="${isSelected ? 'fas fa-check-square' : 'far fa-square'}"></i></span>`;
      }

      btn.innerHTML = `
        <span class="option-letter">${letters[idx] || (idx + 1)}</span>
        ${checkIconHtml}
        <span>${escapeHtmlText(optText)}</span>
      `;

      btn.addEventListener('click', () => {
        if (isMulti) {
          let curr = [...getUserChoices(q.id, state.exam.answers)];
          if (curr.includes(idx)) {
            curr = curr.filter(x => x !== idx);
          } else {
            if (curr.length >= requiredChoices) {
              curr.shift(); // rotate selection
            }
            curr.push(idx);
          }
          if (curr.length === 0) {
            delete state.exam.answers[q.id];
          } else {
            state.exam.answers[q.id] = curr.sort((a, b) => a - b);
          }
        } else {
          state.exam.answers[q.id] = idx;
        }
        renderExamQuestion();
        renderExamPalette();
      });

      dom.examOptionsList.appendChild(btn);
    });

    dom.examPrevBtn.disabled = state.exam.currentIndex === 0;
    dom.examNextBtn.disabled = state.exam.currentIndex === total - 1;

    renderMath(examCard);
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

    calculateAndRenderExamResults(true); // save to history
    window.scrollTo({ top: 0, behavior: getScrollBehavior() });
  }

  function calculateAndRenderExamResults(saveHistory = true) {
    const questions = state.exam.questions;
    let correct = 0;
    let incorrect = 0;
    let unanswered = 0;

    const chapterStats = {}; // { ch: { total: 0, correct: 0 } }

    questions.forEach(q => {
      const ch = (q.chapter || 'comp').toString();
      if (!chapterStats[ch]) {
        chapterStats[ch] = { total: 0, correct: 0 };
      }
      chapterStats[ch].total++;

      const userAns = state.exam.answers[q.id];
      const isCorrect = isAnswerCorrect(q, userAns);

      if (userAns === undefined || (Array.isArray(userAns) && userAns.length === 0)) {
        unanswered++;
      } else if (isCorrect) {
        correct++;
        chapterStats[ch].correct++;
      } else {
        incorrect++;
      }
    });

    const total = questions.length;
    const accuracy = Math.round((correct / total) * 100);
    const scoreOutOf10 = (correct / total) * 10;

    // Score Banner
    dom.resultScoreDisplay.textContent = `${correct} / ${total} (${scoreOutOf10.toFixed(1)} / 10.0)`;
    dom.resMetricAccuracy.textContent = `${accuracy}%`;
    dom.resMetricCorrect.textContent = correct.toString();
    dom.resMetricIncorrect.textContent = (incorrect + unanswered).toString();

    // Time elapsed
    const elapsedSecs = Math.max(0, 3000 - state.exam.timeRemaining);
    const mins = Math.floor(elapsedSecs / 60);
    const secs = elapsedSecs % 60;
    dom.resMetricTime.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    // Pass / Fail Badge
    if (scoreOutOf10 >= 8.0) {
      dom.resultStatusBadge.className = 'results-status-badge status-passed';
      dom.resultStatusBadge.textContent = '🎉 ĐẠT XUẤT SẮC - SẴN SÀNG TRANH CÓC VÀNG (GPA ≥ 9.5)';
    } else if (scoreOutOf10 >= 6.5) {
      dom.resultStatusBadge.className = 'results-status-badge status-passed';
      dom.resultStatusBadge.textContent = '✅ ĐẠT YÊU CẦU (PASS)';
    } else {
      dom.resultStatusBadge.className = 'results-status-badge status-failed';
      dom.resultStatusBadge.textContent = '⚠️ CHƯA ĐẠT (CẦN TIẾP TỤC ÔN TẬP THÊM)';
    }

    if (saveHistory) {
      const logRecord = {
        id: 'exam_' + Date.now(),
        date: new Date().toISOString(),
        formattedDate: new Date().toLocaleString('vi-VN', {
          year: 'numeric', month: '2-digit', day: '2-digit',
          hour: '2-digit', minute: '2-digit'
        }),
        source: state.exam.source,
        sourceTitle: state.exam.source === 'fe' ? 'Đề thi FE 312 Slide (Leaked)' : 'Ngân hàng 12 Chương',
        score: scoreOutOf10,
        accuracy: accuracy,
        correctCount: correct,
        incorrectCount: incorrect,
        unansweredCount: unanswered,
        totalQuestions: total,
        timeSpent: elapsedSecs,
        formattedTime: `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`,
        answers: { ...state.exam.answers },
        flagged: Array.from(state.exam.flagged),
        questions: state.exam.questions
      };
      saveExamHistory(logRecord);
      renderExamHistory();
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
      const userChoices = getUserChoices(q.id, state.exam.answers);
      const isMulti = !!q.is_multi;
      const correctChoices = Array.isArray(q.correct_choices)
        ? q.correct_choices
        : (Array.isArray(q.correct) ? q.correct : [q.correct !== undefined ? q.correct : q.answer]);
      const isCorrect = isAnswerCorrect(q, userAns);
      const isFlagged = state.exam.flagged.has(q.id);

      if (filter === 'wrong' && isCorrect) return;
      if (filter === 'correct' && !isCorrect) return;
      if (filter === 'flagged' && !isFlagged) return;

      const card = document.createElement('div');
      card.className = 'question-card';
      card.style.borderLeft = isCorrect ? '4px solid var(--accent-emerald)' : '4px solid var(--accent-rose)';

      let statusBadge = isCorrect
        ? `<span class="badge-tag" style="background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); border-color: var(--accent-emerald);">✓ Đúng</span>`
        : `<span class="badge-tag" style="background: rgba(239, 68, 68, 0.2); color: var(--accent-rose); border-color: var(--accent-rose);">✗ Sai</span>`;

      if (userChoices.length === 0) {
        statusBadge = `<span class="badge-tag" style="background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); border-color: var(--accent-amber);">⚪ Bỏ trống</span>`;
      }

      let multiTagHtml = '';
      if (isMulti) {
        multiTagHtml = `<span class="badge-tag" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b; border-color: rgba(245, 158, 11, 0.35); font-weight: 700;"><i class="fas fa-check-double"></i> Chọn ${q.required_choices || 2} đáp án</span>`;
      }

      let imageBtnHtml = '';

      let optionsHtml = '';
      q.options.forEach((optText, oIdx) => {
        let optClass = 'option-btn';
        let suffixIcon = '';
        const isThisCorrect = correctChoices.includes(oIdx);
        const isThisUser = userChoices.includes(oIdx);

        if (isThisCorrect && isThisUser) {
          optClass += ' correct-choice';
          suffixIcon = '<span style="margin-left: auto; color: var(--accent-emerald); font-weight: 700;"><i class="fas fa-check-circle"></i> Bạn chọn đúng</span>';
        } else if (isThisCorrect && !isThisUser) {
          optClass += ' correct-choice';
          suffixIcon = '<span style="margin-left: auto; color: var(--accent-emerald); font-weight: 700;"><i class="fas fa-check"></i> Đáp án đúng</span>';
        } else if (!isThisCorrect && isThisUser) {
          optClass += ' incorrect-choice';
          suffixIcon = '<span style="margin-left: auto; color: var(--accent-rose); font-weight: 700;"><i class="fas fa-times-circle"></i> Bạn chọn sai</span>';
        }

        let checkIconHtml = '';
        if (isMulti) {
          checkIconHtml = `<span class="option-check-icon" style="margin-right: 0.5rem;"><i class="${isThisUser ? 'fas fa-check-square' : 'far fa-square'}"></i></span>`;
        }

        optionsHtml += `
          <div class="${optClass}" style="cursor: default;">
            <span class="option-letter">${letters[oIdx] || (oIdx + 1)}</span>
            ${checkIconHtml}
            <span>${escapeHtmlText(optText)}</span>
            ${suffixIcon}
          </div>
        `;
      });

      card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
          <div style="display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;">
            <span style="font-weight: 800; color: var(--text-primary); font-size: 1.05rem;">Câu ${idx + 1}</span>
            <span class="badge-tag">${q.slide ? `Slide ${q.slide}` : (q.chapter === 'comp' ? 'Tổng Hợp' : `Chương ${q.chapter}`)}</span>
            ${multiTagHtml}
            ${statusBadge}
            ${isFlagged ? '<span class="badge-tag" style="background: rgba(245, 158, 11, 0.2); color: var(--accent-amber);">🔖 Đã cắm cờ</span>' : ''}
          </div>
          ${imageBtnHtml}
        </div>

        <div class="q-text">${escapeHtmlText(q.question)}</div>
        <div class="options-list">${optionsHtml}</div>

        <div class="explanation-box show">
          <div class="explanation-title">
            <span>💡</span> Giải thích học thuật (Academic Explanation & Croft Reference)
          </div>
          <div class="explanation-text" style="white-space: pre-line;">${q.explanation || 'Không có giải thích chi tiết.'}</div>
        </div>
      `;

      dom.examReviewQuestionsList.appendChild(card);
    });

    renderMath(dom.examReviewQuestionsList);
  }

  // --- TAB 4: QUESTION BANK EXPLORER (694 Qs) ---
  function initBankTab() {
    const chapters = window.SEG_CHAPTERS || [];
    const totalQs = (window.SEG_QUESTIONS || []).length;
    dom.bankChapterFilter.innerHTML = `<option value="all">Tất cả các chương (${totalQs} câu)</option>`;

    chapters.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch.id.toString();
      const title = ch.title || ch.title_en || `Chapter ${ch.id}`;
      opt.textContent = `Chương ${ch.id}: ${title}`;
      dom.bankChapterFilter.appendChild(opt);
    });

    const compQs = (window.SEG_QUESTIONS || []).filter(q => q.chapter === 'comp');
    const compOpt = document.createElement('option');
    compOpt.value = 'comp';
    compOpt.textContent = `Tổng hợp liên chương (${compQs.length} câu)`;
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
            <span>${escapeHtmlText(optText)}</span>
          </div>
        `;
      });

      card.innerHTML = `
        <div class="q-meta-row">
          <span class="q-num-badge">${q.id}</span>
          <span class="badge-tag">${q.chapter === 'comp' ? 'Tổng Hợp' : 'Chương ' + q.chapter}</span>
        </div>
        <div class="q-text">${escapeHtmlText(q.question)}</div>
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

  // --- TAB 5: GLOSSARY CONTROLLER (66 Terms) ---
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
          Gõ từ khóa để tìm nhanh 12 chương học, thuật ngữ hoặc câu hỏi thi...
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

    // Exam Source Radio Selector
    if (dom.examSourceRadios) {
      dom.examSourceRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
          state.exam.source = e.target.value;
          if (dom.sourceCardFe && dom.sourceCardBank) {
            dom.sourceCardFe.classList.toggle('selected', state.exam.source === 'fe');
            dom.sourceCardBank.classList.toggle('selected', state.exam.source === 'bank');
          }
        });
      });
    }

    // Modal Image Viewer
    if (dom.btnCloseImageModal) {
      dom.btnCloseImageModal.addEventListener('click', closeImageModal);
    }
    if (dom.imageViewerModal) {
      dom.imageViewerModal.addEventListener('click', (e) => {
        if (e.target === dom.imageViewerModal) closeImageModal();
      });
    }

    // Back to Exam Intro button
    if (dom.backToIntroBtn) {
      dom.backToIntroBtn.addEventListener('click', returnToExamIntro);
    }

    // Exam Source Radio Selector
    if (dom.examSourceRadios) {
      dom.examSourceRadios.forEach(radio => {
        radio.addEventListener('change', (e) => {
          state.exam.source = e.target.value;
          if (dom.sourceCardFe && dom.sourceCardBank) {
            dom.sourceCardFe.classList.toggle('selected', state.exam.source === 'fe');
            dom.sourceCardBank.classList.toggle('selected', state.exam.source === 'bank');
          }
        });
      });
    }

    // Modal Image Viewer
    if (dom.btnCloseImageModal) {
      dom.btnCloseImageModal.addEventListener('click', closeImageModal);
    }
    if (dom.imageViewerModal) {
      dom.imageViewerModal.addEventListener('click', (e) => {
        if (e.target === dom.imageViewerModal) closeImageModal();
      });
    }

    // Back to Exam Intro button
    if (dom.backToIntroBtn) {
      dom.backToIntroBtn.addEventListener('click', returnToExamIntro);
    }

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
        closeImageModal();
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
    },
    openImageModal,
    closeImageModal,
    viewExamRecord,
    clearExamHistory,
    state,
    sampleRandomExamQuestions
  };

  // Run on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
