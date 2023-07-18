# DeAngelo's Restaurant Booking System

DeAngelo's Restaurant Booking System is a comprehensive digital solution developed to streamline and enhance the dining experience for both customers and administrators of DeAngelo's, a popular local fictitious eatery. The application integrates a range of user-friendly functionalities, offering a seamless interface between customers and staff.

The platform has been primarily developed to cater to the needs of restaurant-goers and the restaurant's administrative personnel. It provides an efficient online booking system for customers seeking to reserve tables at their convenience, while also allowing them to view the restaurant's extensive menu. This interactive, easy-to-navigate system greatly simplifies the booking process and ensures customers can plan their visit to DeAngelo's without any hassle.

For the administrative personnel of DeAngelo's, this system provides a robust back-end solution that offers an overview of the bookings, enables menu management, and handles table arrangements. This ensures smooth operations and improved organization within the restaurant, leading to better service quality and enhanced customer satisfaction.

The DeAngelo's Restaurant Booking System aims to bridge the gap between conventional restaurant management and the growing need for digital interaction in the hospitality industry. With its simple, intuitive design, and effective functionality, it offers a unique, improved dining experience for customers while ensuring efficient, organized operations for the restaurant's staff and administration.

## Existing features 

- Navigation Bar for customers 
   - When visitors first land on the home page they will see a top nav bar with links to four pages, Home, Menu, Gallery and login. The DeAngelo's branding is also displayed on the left hand side. Clicking the logo returns the user back to the home page.
   - On larger screens a more traditional navigation is displayed, on smaller screens the navigation reverts to a hamburger menu.

![Screenshot of logo & navigation](documentation/front-facing-navigation.png)

  - Registered users will have extra links to their profile page and to the reservations page. The login link changes to logout.

![Screenshot of logged in registered user links](documentation/logged-in-customer.png)
  
  - Signed in Admins will have an extra link to the Admin App

![Screenshot of logged in admin links](documentation/logged-in-admin.png)

### Site Home Page

The site home page contains a hero image of the Italian countryside. It gives the visitor a sense of the rich, serene, and rustic ambiance associated with traditional Italian dining, setting the stage for a culinary journey through the delights of Italian cuisine.

There is also a section containing a brief synopsis of the restaurant's history.

![Screenshot of the top half of the home page](documentation/front-page-top.png)

Scrolling to the lower segment of the home page, the viewer is greeted with a warmly inviting image of the restaurant's interior. The restaurant address and phone number are also displayed.

![Screenshot of the bottom half of the home page](documentation/front-page-bottom.png)

### Site Footer

the site footer is displayed on all front facing pages. It contains the copyright symbol. Here, visitors can explore a wider array of content concerning the restaurant, with every link thoughtfully designed to open in a separate tab, ensuring undisturbed navigation."

![Screenshot of the footer](documentation/footer.png)

### Menu Page

The menu page contains vibrant imagery of our delectable dishes. Accompanied by both detailed descriptions and transparent pricing, it offers an enticing preview of the culinary delights that await our guests.

![Screenshot of the footer](documentation/menu.png)

### Gallery Page

The gallery page showcases an array of captivating images which we feel captures the essence of our restaurant. To elevate user experience, a simple click on an image triggers a seamless on-page enlargement, offering an up-close view of the image. Additionally, users can effortlessly navigate through these magnified images - right and left - without the need to close each picture first, thereby ensuring a smooth, uninterrupted exploration."

![Screenshot of the footer](documentation/gallery.png)

### Reservation Page

The reservation page is only available to registered users and displays the booking form. At the top of the form there is a paragraph explaining how to complete the form. Once the user enters details, script runs in the background to check to see if the table(s) is available. There is validation built into the form to ensure a date in the past cannot be selected. A table becomes available again two hours after being selcted. Also there is a check to make sure that the number of guests is not greater than the capacity of the tables selected. The submit button is disabled until all checks have been passed.

The reservation page, accessible only to registered users, elegantly presents a booking form with an accompanying guide on how to fill it out. As the user inputs their details, a script diligently checks the availability of the requested tables. The form incorporates an intelligent validation system, eliminating the possibility of selecting past dates and ensuring that the number of guests does not surpass the capacity of the chosen tables. Furthermore, each table becomes available for new reservations two hours after the start of the previous booking. Only when all these checks are satisfied does the form's submission button become enabled, ensuring a smooth and error-free reservation experience.

![Screenshot of the booking form](documentation/booking-form.png)

This message is displayed when the table is available and all necessary information is provided.

![Screenshot of table is available message](documentation/table-available.png)

This message is displayed when the table is not available.

![Screenshot of table is not available message](documentation/table-not-available.png)

These errors are displayed if a date in the past is selected or when a time slot selected is too close to closing time.

![Screenshot of errors for past dates and late bookings](documentation/past-booking-and-too-close-to-closing-time.png)

### Profile Page