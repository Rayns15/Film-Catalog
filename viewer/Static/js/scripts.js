document.addEventListener('DOMContentLoaded', function () {
    // Highlight active navigation link based on current URL
    const navLinks = document.querySelectorAll('.actions a.btn-login, .actions a.btn-signup');
    navLinks.forEach(link => {
        if (window.location.pathname === link.getAttribute('href')) {
            link.classList.add('active');
        }
    });

    // Example: Add smooth scroll to Contact link
    const contactLink = document.querySelector('.actions a[href="/contact/"]');
    if (contactLink) {
        contactLink.addEventListener('click', function (e) {
            if (window.location.pathname === '/contact/') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    }
});