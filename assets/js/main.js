(function () {
    'use strict';

    function setSidebar(open, restoreFocus) {
        var sidebar = document.getElementById('sidebar');
        var button = document.querySelector('.sidebar-btn');
        if (!sidebar) return;
        sidebar.classList.toggle('open', open);
        sidebar.setAttribute('aria-hidden', String(!open));
        sidebar.toggleAttribute('inert', !open);
        if (button) {
            button.classList.toggle('open', open);
            button.setAttribute('aria-expanded', String(open));
            button.setAttribute('aria-label', open ? '카테고리 메뉴 닫기' : '카테고리 메뉴 열기');
            if (restoreFocus) button.focus();
        }
    }

    // Keep the existing template's onclick contract without replacing global events.
    window.openSidebar = function () {
        var sidebar = document.getElementById('sidebar');
        if (sidebar) setSidebar(!sidebar.classList.contains('open'), false);
    };

    function setupSidebar() {
        var sidebar = document.getElementById('sidebar');
        var button = document.querySelector('.sidebar-btn');
        if (!sidebar) return;
        setSidebar(sidebar.classList.contains('open'), false);
        if (button && !button.hasAttribute('onclick')) {
            button.addEventListener('click', window.openSidebar);
        }
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && sidebar.classList.contains('open')) {
                setSidebar(false, true);
            }
        });
        document.addEventListener('click', function (event) {
            if (sidebar.classList.contains('open') && !sidebar.contains(event.target) &&
                !(button && button.contains(event.target))) {
                setSidebar(false, false);
            }
        });
        document.querySelectorAll('.expand-btn').forEach(function (toggle, index) {
            var controls = toggle.getAttribute('aria-controls');
            var group = toggle.closest('.lv1-category');
            var children = (controls && document.getElementById(controls)) ||
                (group && group.querySelector('.lv2-categories'));
            if (!children) return;
            if (!children.id) children.id = 'subcategories-' + (index + 1);
            toggle.setAttribute('aria-controls', children.id);
            toggle.setAttribute('aria-expanded', String(children.classList.contains('expand')));
            toggle.addEventListener('click', function () {
                var expanded = children.classList.toggle('expand');
                toggle.classList.toggle('expand', expanded);
                toggle.setAttribute('aria-expanded', String(expanded));
            });
        });
    }

    function setupProgress() {
        var indicator = document.getElementById('indicator');
        if (!indicator) return;
        var scheduled = false;
        function update() {
            scheduled = false;
            var root = document.documentElement;
            var height = root.scrollHeight - root.clientHeight;
            var progress = height > 0 ? (window.scrollY || root.scrollTop || 0) / height : 0;
            indicator.style.transform = 'scaleX(' + Math.max(0, Math.min(1, progress)) + ')';
        }
        function schedule() {
            if (!scheduled) {
                scheduled = true;
                window.requestAnimationFrame(update);
            }
        }
        window.addEventListener('scroll', schedule, { passive: true });
        window.addEventListener('resize', schedule, { passive: true });
        // Images, fonts, math and comments can change the page height after first paint.
        if ('ResizeObserver' in window) {
            new ResizeObserver(schedule).observe(document.body);
        } else {
            window.addEventListener('load', schedule, { once: true });
        }
        schedule();
    }

    function setupComments() {
        var button = document.getElementById('load-comments');
        var status = document.getElementById('comments-status');
        if (!button || !status) return;
        button.addEventListener('click', function () {
            if (button.disabled) return;
            var shortname = button.getAttribute('data-disqus-shortname');
            if (!shortname || !/^[a-z0-9-]+$/i.test(shortname)) return;
            button.disabled = true;
            status.textContent = '댓글을 불러오는 중입니다…';
            var url = button.getAttribute('data-page-url');
            // Keep URL-based discussion matching; old posts did not set an identifier.
            window.disqus_config = function () {
                if (url) this.page.url = url;
            };
            var script = document.createElement('script');
            script.src = 'https://' + shortname + '.disqus.com/embed.js';
            script.async = true;
            script.setAttribute('data-timestamp', String(Date.now()));
            script.onload = function () {
                button.hidden = true;
                status.textContent = '댓글 서비스가 열립니다. 표시되지 않으면 광고 차단 설정을 확인해 주세요.';
            };
            script.onerror = function () {
                script.remove();
                button.disabled = false;
                button.textContent = '댓글 다시 불러오기';
                status.textContent = '댓글을 불러오지 못했습니다. 연결 상태나 광고 차단 설정을 확인한 뒤 다시 시도해 주세요.';
            };
            document.head.appendChild(script);
        });
    }

    function initialize() {
        setupSidebar();
        setupProgress();
        setupComments();
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize, { once: true });
    } else {
        initialize();
    }
}());
