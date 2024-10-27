# Midterm_Project


## **Names of group members**
- Naim Baziz (2406394881)
- Andhika Nayaka Arya Wibowo (2306174135)
- Syifa Ananda Widyati (2306173656)
- Keira Diaz Nabhani (2306256394)
- Adyo Arkan Prawira (2306173750)
- Ameera Khaira Tawfiqa (2306256223)


## **Application description**
A Thousand Flavours is a platform designed for exploring restaurants in Pulau Seribu. This website allows users to easily find restaurants across the islands, with easy options to save favorites and make a wish list. Users also can leave ratings and reviews to the restaurant they have visited. Each month, a featured "Restaurant of the Month" highlight which is a standout spot giving the opportunity for local restaurants to stand out. This website also provides images of some restaurants as well as direct Google Maps links for each restaurant, making it easy to navigate straight to users' chosen restaurant.


## **List of modules to be implemented**
**Main Page**
- Home (```show_main```)
In the main page users can explore featured restaurants in the gallery, check out restaurant categories to get an overview of what is available. The main page also displays images of restaurants and the restaurant of the month and possibly advertisements.


**Navigation Bar**
- Navbar (```navbar```)
The navigation bar will display the following: the title of the website A Thousand Flavors and text that shows Welcome, {name} in which the user name changes depending on the name of the logged in user. The welcome text does not show if the user is not logged in. In addition, there are buttons for the interactive features, Explore, Wishlist and Favorites.
Logged in users can choose to log out by clicking on their username in the navigation bar and a pop out will appear to log out.

**User Authentication Modules**
- Sign Up (```register```)
Provides a page for new users to register their account
- Login (```login_user```)
Allows returning users to log in and access their saved preferences
- Logout (```logout_user```)
Log out the current user

**Interactive Features**
- Add to Favorites (```add_to_favorites```)
Allows users to mark a restaurant as a favorite
- View Favorites (```show_favorites```)
Shows a list of restaurants marked as favorite by the user
- Add to Wishlist and Remove from Wishlist
Users can add restaurant to a wishlist using ```add_to_wishlist``` and remove them if needed with ```remove_from_wishlist```
- Wishlist (```show_wishlist```)
Shows all restaurants in the users wishlist
- Add a Review (```add_review```)
Allows users to add a review on restaurants they have visited. Could include ratings, comments, and other feedback
- Restaurant of the Month (```restaurant_of_the_month```)
Highlights a special restaurant each month on the main page
- Search Restaurants (```search_restaurant```)
Allows users to find restaurants by typing in the restaurants name
- Google Maps location redirect (```redirect_to_google_maps```)
Open Google Maps with directions to a specific restaurant directly from the site

## **Source of initial dataset for main product category**
https://docs.google.com/spreadsheets/d/15E1xJK2QDuCy3dWdd7jCqVFBHhm_CS1D6vKP3dhr_dg/edit?gid=0#gid=0


## **User roles and their descriptions**


**Admin**
Below are the admin privileges;


1. Edit, Delete, and Add New Data
Admins have full control over the platform's data. They can add new content such as restaurants and photos, keeping the platform updated. In addition, they can edit or remove outdated or incorrect data, ensuring the information on the platform is always accurate and relevant.


2. View All User Data
Admins have access to the complete set of user data, including profiles, activity logs, and reviews. This allows them to monitor user interactions, track engagement, and ensure compliance with the platforms guidelines. We can use this data for future modeling implementation.


3. Modify Customer Reviews
Admins can edit and remove customer reviews. By managing customer reviews, admins help maintain a constructive and informative environment for all users.

4. Access and Modify Internal Data Formats
Admins can work directly with the platforms underlying data structures, such as JSON and XML files. This ability allows them to modify how data is stored, transferred, and displayed, ensuring smooth functionality and integration with backend systems. This technical capability is essential for optimizing performance and implementing new features.


**Users**
Registered users have access to personalized features, allowing them to save their favorite restaurants, create a wishlist of places, and leave reviews to share their thoughts with others. They can see a customized navigation bar that includes these interactive options.


**Non Users**
Non registered users, or guest users, have limited access. They can look up restaurants by name and view general information, but personalization options are unavailable. 


## **Application deployment link**
https://andhika-nayaka-athousandflavourmidterm.pbp.cs.ui.ac.id/
