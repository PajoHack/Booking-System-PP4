// // Wait for all elements of the DOM to be fully loaded before running the script
// window.addEventListener('DOMContentLoaded', event => {

//     // Find the navigation bar element in the body of the document
//     const navbarNav = document.body.querySelector('#navbarNav');
//     // Check if the navigation bar element exists
//     if (navbarNav) {
//         // Add a click event listener to the navigation bar
//         navbarNav.addEventListener('click', event => {
//             // Prevent the default action of the click event (useful if the element is a link or a button)
//             event.preventDefault();
//              // If the navigation bar currently has the 'show' class, remove it
//             if(navbarNav.classList.contains('show')){
//                 navbarNav.classList.remove('show');
//             } 
//             // If the navigation bar does not have the 'show' class, add it
//             else {
//                 navbarNav.classList.add('show');
//             }
//         });
//     }

// });
