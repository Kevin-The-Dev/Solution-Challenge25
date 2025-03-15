document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('nav ul li');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Remove active class from all links
            navLinks.forEach(item => item.classList.remove('active'));
            // Add active class to clicked link
            link.classList.add('active');

            // Simulate notification toggle for Staff Room
            if (link.classList.contains('notification')) {
                link.classList.toggle('notified');
            }
        });
    });
});