// This script dynamically updates the SVG filter based on CSS variables
// Define the update function in the global scope so it can be called from other scripts
function updateSVGFilter() {
    const root = document.documentElement;
    const cornerRadius = getComputedStyle(root).getPropertyValue('--hex-corner-radius').trim();
    
    // Update the stdDeviation attribute of the feGaussianBlur filter
    const filterBlur = document.querySelector('#goo feGaussianBlur');
    if (filterBlur) {
        filterBlur.setAttribute('stdDeviation', cornerRadius);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Run once on load
    updateSVGFilter();
    
    // Optional: Watch for resize events if you have responsive styles that change variables
    window.addEventListener('resize', updateSVGFilter);
});
