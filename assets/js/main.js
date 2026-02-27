// Sidebar toggle
function openSidebar(x) {
    x.classList.toggle('open');
    var sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open');
}

// Scroll progress bar
window.onscroll = function() {
    var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    var scrolled = (winScroll / height) * 100;
    document.getElementById("indicator").style.width = scrolled + "%";
};

// Sidebar sub-category expand/collapse
document.addEventListener('DOMContentLoaded', function() {
    var treeNodes = document.querySelectorAll('.expand-btn');
    treeNodes.forEach(function(t) {
        t.addEventListener('click', function(e) {
            var lv2 = e.currentTarget.parentElement.parentElement.nextElementSibling;
            lv2.classList.toggle('expand');
            e.currentTarget.classList.toggle('expand');
        });
    });
});

// Loading screen
window.addEventListener('load', function() {
    document.getElementById('load').style.display = 'none';
});
