
// document.addEventListener("DOMContentLoaded", () => {
//     const popup = document.getElementById("popup");
//     const closePopupButton = document.getElementById("closePopup");
//     const navLinks = document.querySelectorAll('.navbar ul li a');
//     const menuIcon = document.getElementById("menuIcon");
//     const unorderedList = document.getElementById("unorderedList");

//     window.addEventListener("scroll", () => {
//         console.log(`Current scroll position: ${window.scrollY}`);
//         if (window.scrollY >= 610) {
//             console.log("Showing popup...");
//             if (popup) {
//                 popup.classList.add("visible");
//                 popup.classList.remove("hidden");
//             }
//         } else {
//             console.log("Hiding popup...");
//             if (popup) {
//                 popup.classList.remove("visible");
//                 popup.classList.add("hidden");
//             }
//         }
//     });

//     // Close the popup when the close button is clicked
//     if (closePopupButton) {
//         closePopupButton.addEventListener("click", () => {
//             if (popup) {
//                 popup.classList.remove("visible");
//                 popup.classList.add("hidden");
//             }
//         });
//     }

//     // Active class and underline toggle for navigation links
//     navLinks.forEach(link => {
//         link.addEventListener('click', function () {
//             // Remove active class from previously active link
//             const currentActive = document.querySelector('.navbar ul li a.active');
//             if (currentActive) {
//                 currentActive.classList.remove('active');
//             }

//             // Add active class to the clicked link and underline it
//             this.classList.add('active');
//         });
//     });
    
//     if (menuIcon && unorderedList) {
//         menuIcon.addEventListener("click", () => {
//             unorderedList.classList.toggle("shown");
//             menuIcon.classList.toggle("open");
//             console.log("Menu toggle activated.");
//         });
//     } else {
//         console.error("Menu icon or unordered list not found.");
//     }
// });


document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popup");
    const closePopupButton = document.getElementById("closePopup");
    const navLinks = document.querySelectorAll(".navbar ul li a");
    const menuIcon = document.getElementById("menuIcon");
    const unorderedList = document.getElementById("unorderedList");

    // Function to toggle the menu
    const toggleMenu = () => {
        if (unorderedList && menuIcon) {
            unorderedList.classList.toggle("shown");
            menuIcon.classList.toggle("open");
            console.log("Menu toggled.");
        } else {
            console.error("Menu icon or unordered list not found.");
        }
    };

    // Function to handle the popup visibility based on scroll
    const handleScroll = () => {
        if (window.scrollY >= 436) {
            console.log("Showing popup...");
            if (popup) {
                popup.classList.add("visible");
                popup.classList.remove("hidden");
            }
        } else {
            console.log("Hiding popup...");
            if (popup) {
                popup.classList.remove("visible");
                popup.classList.add("hidden");
            }
        }
    };

    window.addEventListener("scroll", handleScroll);

    if (menuIcon) {
        menuIcon.addEventListener("click", toggleMenu);
    } else {
        console.error("Menu icon not found.");
    }

    // Close the popup when the close button is clicked
    if (closePopupButton) {
        closePopupButton.addEventListener("click", () => {
            if (popup) {
                popup.classList.remove("visible");
                popup.classList.add("hidden");
            }
        });
    }

    // Active class and underline toggle for navigation links
    navLinks.forEach((link) => {
        link.addEventListener("click", function () {
            // Remove active class from previously active link
            const currentActive = document.querySelector(".navbar ul li a.active");
            if (currentActive) {
                currentActive.classList.remove("active");
            }

            // Add active class to the clicked link and underline it
            this.classList.add("active");
        });
    });

    // Ensure the menu toggle works when the popup becomes visible
    const observePopupVisibility = () => {
        if (popup) {
            const observer = new MutationObserver(() => {
                if (popup.classList.contains("visible")) {
                    console.log("Popup became visible. Reattaching menu icon listener.");
                    // Re-attach the menu icon click listener when popup becomes visible
                    if (menuIcon) {
                        menuIcon.removeEventListener("click", toggleMenu); // Remove previous listeners
                        menuIcon.addEventListener("click", toggleMenu); // Re-add listener
                    }
                }
            });

            observer.observe(popup, { attributes: true, attributeFilter: ["class"] });
        }
    };

    observePopupVisibility();
});


document.addEventListener("DOMContentLoaded", function () {
    // Select auth-text and side-menu
    const authText = document.querySelector(".auth-text");
    const sideMenu = document.querySelector(".side-menu");

    // Toggle side-menu visibility on click
    authText.addEventListener("click", function () {
        sideMenu.classList.toggle("visible");
    });

    // Optional: Close the menu when clicking outside of it
    document.addEventListener("click", function (event) {
    if (!authText.contains(event.target) && !sideMenu.contains(event.target)) {
        sideMenu.classList.remove("visible");
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Main navbar
    const originalNavbar = document.querySelector("nav.navbar");

    // Placeholder for the cloned navbar in the popup
    const popupNavbarPlaceholder = document.getElementById("popup-navbar-placeholder");

    // Clone the original navbar and append it to the popup
    if (originalNavbar && popupNavbarPlaceholder) {
        const clonedNavbar = originalNavbar.cloneNode(true); // Deep clone the navbar
        clonedNavbar.id = "popup-navbar"; // Assign a unique ID to the cloned navbar
        popupNavbarPlaceholder.appendChild(clonedNavbar);

        // Add event listeners specifically for the cloned navbar
        const menuIconPopup = clonedNavbar.querySelector("#menuIcon"); // Adjust if IDs are reused
        const unorderedListPopup = clonedNavbar.querySelector("#unorderedList");
        const authTextPopup = clonedNavbar.querySelector("#authText");
        const sideMenuPopup = clonedNavbar.querySelector("#sideMenu");

        if(authTextPopup && sideMenuPopup) {
            authTextPopup.addEventListener("click", function () {
                sideMenuPopup.classList.toggle("visible");
            });
        }
        // Optional: Close the menu when clicking outside of it
        document.addEventListener("click", function (event) {
        if (!authTextPopup.contains(event.target) && !sideMenuPopup.contains(event.target)) {
            sideMenuPopup.classList.remove("visible");
            }
        });

        if (menuIconPopup && unorderedListPopup) {
            menuIconPopup.addEventListener("click", () => {
                unorderedListPopup.classList.toggle("shown");
            });
        }
        // Optional: Close the menu when clicking outside of it
        // document.addEventListener("click", function (event) {
        // if (!menuIconPopup.contains(event.target) && !unorderedListPopup.contains(event.target)) {
        //     unorderedListPopup.classList.remove("visible");
        //     }
        // });
    }
});

