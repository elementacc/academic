// Selected page hover functionality
document.addEventListener('DOMContentLoaded', function() {
    const projectRows = document.querySelectorAll('.project-row');
    
    projectRows.forEach(row => {
        const hoverImages = row.querySelector('.hover-images');
        
        if (hoverImages) {
            // Show images on hover
            row.addEventListener('mouseenter', function() {
                hoverImages.style.opacity = '1';
                hoverImages.style.visibility = 'visible';
            });
            
            // Hide images when not hovering
            row.addEventListener('mouseleave', function() {
                hoverImages.style.opacity = '0';
                hoverImages.style.visibility = 'hidden';
            });
            
            // Prevent images from disappearing when hovering over them
            hoverImages.addEventListener('mouseenter', function() {
                hoverImages.style.opacity = '1';
                hoverImages.style.visibility = 'visible';
            });
        }
    });
    
    // Add click functionality to individual images for modal viewing
    const gridImages = document.querySelectorAll('.grid-image img');
    
    gridImages.forEach(img => {
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            // You can add modal functionality here if needed
            console.log('Image clicked:', this.src);
        });
    });
});