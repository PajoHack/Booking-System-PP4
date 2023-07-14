window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const navbarNav = document.body.querySelector('#navbarNav');
    if (navbarNav) {
        navbarNav.addEventListener('click', event => {
            event.preventDefault();
            if(navbarNav.classList.contains('show')){
                navbarNav.classList.remove('show');
            } else {
                navbarNav.classList.add('show');
            }
        });
    }

});
