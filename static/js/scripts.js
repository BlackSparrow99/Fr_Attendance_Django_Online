document.addEventListener("DOMContentLoaded", () => {
    const popup = document.getElementById("popup");
    const closePopupButton = document.getElementById("closePopup");
    const navLinks = document.querySelectorAll("#unorderedList li a");
    const menuIcon = document.getElementById("menuIcon");
    const unorderedList = document.getElementById("unorderedList");
    const authText = document.querySelector(".auth-text");
    const sideMenu = document.querySelector(".side-menu");

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

    // Function to handle popup visibility based on scroll
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

    // Function to handle the active class toggling and storing the active link
    const setActiveClass = (clickedLink) => {
        // Remove active class from all links
        navLinks.forEach((link) => link.classList.remove("active"));

        // Add active class to the clicked link
        clickedLink.classList.add("active");

        // Store the active link in localStorage
        localStorage.setItem("activeLink", clickedLink.href);
    };

    // Function to handle link click event
    const handleLinkClick = (event) => {
        const clickedLink = event.target;

        // Only toggle active if it's a valid link (not a "#" or "void" link)
        if (clickedLink.tagName === "A" && clickedLink.href !== "#") {
            setActiveClass(clickedLink);
        }
    };

    // Add event listeners for all links to manage active class
    navLinks.forEach((link) => {
        link.addEventListener("click", handleLinkClick);
    });

    // Ensure the active class is correctly set on page load
    window.addEventListener("load", () => {
        const activeLinkHref = localStorage.getItem("activeLink");

        // If we have a stored active link, set it to active
        if (activeLinkHref) {
            const activeLink = Array.from(navLinks).find((link) => link.href === activeLinkHref);
            if (activeLink) {
                setActiveClass(activeLink);
            }
        }
    });

    // Function to toggle the side menu
    const toggleSideMenu = () => {
        if (authText && sideMenu) {
            authText.addEventListener("click", () => {
                sideMenu.classList.toggle("visible");
            });

            // Close side menu when clicking outside of it
            document.addEventListener("click", (event) => {
                if (!authText.contains(event.target) && !sideMenu.contains(event.target)) {
                    sideMenu.classList.remove("visible");
                }
            });
        }
    };

    // Clone navbar for popup
    const cloneNavbarForPopup = () => {
        const originalNavbar = document.querySelector("nav.navbar");
        const popupNavbarPlaceholder = document.getElementById("popup-navbar-placeholder");

        if (originalNavbar && popupNavbarPlaceholder) {
            const clonedNavbar = originalNavbar.cloneNode(true);
            clonedNavbar.id = "popup-navbar";
            popupNavbarPlaceholder.appendChild(clonedNavbar);

            const clonedNavLinks = clonedNavbar.querySelectorAll("#unorderedList li a");

            // Re-attach click listeners to cloned navbar
            clonedNavLinks.forEach((link) => {
                link.addEventListener("click", handleLinkClick);
            });
        }
    };

    // Initialize all functionality
    const initialize = () => {
        // Scroll-based popup visibility
        window.addEventListener("scroll", handleScroll);

        // Menu toggle logic
        if (menuIcon) {
            menuIcon.addEventListener("click", toggleMenu);
        }

        // Close popup when close button is clicked
        if (closePopupButton) {
            closePopupButton.addEventListener("click", () => {
                if (popup) {
                    popup.classList.remove("visible");
                    popup.classList.add("hidden");
                }
            });
        }

        // Side menu toggle logic
        toggleSideMenu();

        // Clone navbar for popup functionality
        cloneNavbarForPopup();
    };

    // Run initialize
    initialize();
});
