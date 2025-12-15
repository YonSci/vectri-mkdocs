// Collapse all navigation sections by default (except the one containing current page)
// This script works with Material for MkDocs navigation system
(function() {
  'use strict';
  
  function collapseNavSections() {
    // Find all top-level navigation sections (Day 1, Day 2, etc.)
    const navItems = document.querySelectorAll('.md-nav__item--nested');
    
    navItems.forEach(function(item) {
      // Check if this section contains the currently active page
      const hasActiveLink = item.querySelector('.md-nav__link--active');
      
      // Only collapse sections that don't contain the active page
      if (!hasActiveLink) {
        // Remove the active class to collapse the section
        item.classList.remove('md-nav__item--active');
      }
    });
  }
  
  // Wait for navigation to be fully rendered
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      // Try multiple times to ensure navigation is ready
      setTimeout(collapseNavSections, 300);
      setTimeout(collapseNavSections, 600);
      setTimeout(collapseNavSections, 1000);
    });
  } else {
    setTimeout(collapseNavSections, 300);
    setTimeout(collapseNavSections, 600);
    setTimeout(collapseNavSections, 1000);
  }
})();

