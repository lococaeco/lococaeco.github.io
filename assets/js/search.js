(function () {
    'use strict';

    const input = document.getElementById('search-input');
    const results = document.getElementById('results-container');
    const status = document.getElementById('search-status');
    if (!input || !results || !status) return;

    const maximumResults = 100;
    let indexPromise;
    let searchTimer;
    let sequence = 0;
    let composing = false;

    function element(tag, className, text) {
        const node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function safeURL(value, image) {
        if (typeof value !== 'string' || !value.trim()) return '';
        try {
            const url = new URL(value, window.location.href);
            if (!['http:', 'https:'].includes(url.protocol)) return '';
            if (!image && url.origin !== window.location.origin) return '';
            return url.href;
        } catch (_) {
            return '';
        }
    }

    function loadIndex() {
        if (!indexPromise) {
            indexPromise = fetch(input.dataset.searchIndex, { credentials: 'same-origin' })
                .then(response => {
                    if (!response.ok) throw new Error('Search index unavailable');
                    return response.json();
                })
                .then(posts => {
                    if (!Array.isArray(posts)) throw new Error('Invalid search index');
                    return posts.filter(post => post && typeof post === 'object' && safeURL(post.url, false)).map(post => ({
                        ...post,
                        searchText: [post.title, post.excerpt, post.tags, post.categories].filter(Boolean).join(' ').normalize('NFKC').toLocaleLowerCase('ko-KR'),
                    }));
                })
                .catch(error => { indexPromise = null; throw error; });
        }
        return indexPromise;
    }

    function resultCard(post) {
        const href = safeURL(post.url, false);
        if (!href) return null;
        const item = element('li', 'search-result');
        const link = element('a', 'post-link default-single-default');
        link.href = href;
        const teaser = element('div', 'list-element-teaser');
        const imageURL = safeURL(post.teaser, true);
        if (imageURL) {
            const image = element('img');
            image.src = imageURL;
            image.alt = '';
            image.loading = 'lazy';
            image.decoding = 'async';
            image.width = 128;
            image.height = 128;
            image.addEventListener('error', () => {
                image.remove();
                teaser.append(element('div', 'empty-teaser'));
            }, { once: true });
            teaser.append(image);
        } else {
            teaser.append(element('div', 'empty-teaser'));
        }
        const text = element('div', 'list-element-text');
        text.append(element('div', 'list-element-category', post.categories || ''));
        text.append(element('h2', 'list-element-title', post.title || '제목 없는 글'));
        const date = element('time', 'list-element-date', post.date || '');
        if (/^\d{4}[.-]\d{2}[.-]\d{2}$/.test(post.date || '')) date.dateTime = post.date.replace(/\./g, '-');
        text.append(date, element('div', 'list-element-excerpt', post.excerpt || ''));
        link.append(teaser, text);
        item.append(link);
        return item;
    }

    async function search() {
        const currentSequence = ++sequence;
        const query = input.value.normalize('NFKC').trim().toLocaleLowerCase('ko-KR');
        if (!query) {
            results.replaceChildren();
            results.removeAttribute('aria-busy');
            status.textContent = '제목, 태그, 카테고리로 글을 찾아보세요.';
            return;
        }
        results.setAttribute('aria-busy', 'true');
        status.textContent = '글을 찾고 있어요…';
        try {
            const posts = await loadIndex();
            if (currentSequence !== sequence) return;
            const words = query.split(/\s+/);
            const matches = posts.filter(post => words.every(word => post.searchText.includes(word)));
            const fragment = document.createDocumentFragment();
            for (const post of matches.slice(0, maximumResults)) {
                const card = resultCard(post);
                if (card) fragment.append(card);
            }
            results.replaceChildren(fragment);
            status.textContent = matches.length ? matches.length > maximumResults
                ? `${matches.length}개의 글 중 처음 ${maximumResults}개를 표시합니다. 검색어를 더 입력해 범위를 좁혀보세요.`
                : `${matches.length}개의 글을 찾았어요.`
                : '검색 결과가 없어요. 다른 검색어로 찾아보세요.';
        } catch (_) {
            if (currentSequence !== sequence) return;
            results.replaceChildren();
            status.textContent = '검색 목록을 불러오지 못했어요. 연결을 확인하고 Enter 키로 다시 시도해 주세요.';
        } finally {
            if (currentSequence === sequence) results.removeAttribute('aria-busy');
        }
    }

    function scheduleSearch() {
        clearTimeout(searchTimer);
        // Invalidate an earlier request as soon as the query changes.
        sequence += 1;
        if (!composing) searchTimer = setTimeout(search, 160);
    }
    input.addEventListener('input', scheduleSearch);
    input.addEventListener('compositionstart', () => { composing = true; clearTimeout(searchTimer); sequence += 1; });
    input.addEventListener('compositionend', () => { composing = false; scheduleSearch(); });
    input.addEventListener('focus', () => { loadIndex().catch(() => {}); }, { once: true });
    input.form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(searchTimer); search(); });

    const initialQuery = new URLSearchParams(window.location.search).get('q');
    if (initialQuery) { input.value = initialQuery; search(); }
})();
