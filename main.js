// Simple Gallery Script - No redirects, no automatic navigation
document.addEventListener('DOMContentLoaded', function() {
    let currentImageIndex = 0;
    let allImages = [];
    let modal = null;

    // Create modal on page load
    createModal();
    
    // Add click listeners to all images
    initializeImageClicks();

    function createModal() {
        modal = document.createElement('div');
        modal.className = 'simple-modal';
        modal.innerHTML = `
            <div class="simple-modal-overlay">
                <button class="simple-modal-close">&times;</button>
                <button class="simple-modal-prev">‹</button>
                <button class="simple-modal-next">›</button>
                <img class="simple-modal-image" src="" alt="">
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Close modal events
        modal.querySelector('.simple-modal-close').addEventListener('click', closeModal);
        modal.querySelector('.simple-modal-overlay').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });
        
        // Navigation events
        modal.querySelector('.simple-modal-prev').addEventListener('click', function(e) {
            e.stopPropagation();
            showPrevImage();
        });
        
        modal.querySelector('.simple-modal-next').addEventListener('click', function(e) {
            e.stopPropagation();
            showNextImage();
        });
        
        // Keyboard events
        document.addEventListener('keydown', function(e) {
            if (!modal.classList.contains('active')) return;
            
            if (e.key === 'Escape') closeModal();
            if (e.key === 'ArrowLeft') showPrevImage();
            if (e.key === 'ArrowRight') showNextImage();
        });
    }

    function initializeImageClicks() {
        // Get all images from archive and lectures
        const archiveImages = document.querySelectorAll('.image-container img');
        const lectureImages = document.querySelectorAll('.lecture-image img, .lecture-image-container img, .teaching-image-container img');
        
        // Combine all images
        allImages = [];
        
        archiveImages.forEach(img => {
            allImages.push(img.src);
            img.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                openModal(img.src);
            });
        });
        
        lectureImages.forEach(img => {
            allImages.push(img.src);
            img.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                openModal(img.src);
            });
        });
    }

    function openModal(imageSrc) {
        currentImageIndex = allImages.indexOf(imageSrc);
        modal.querySelector('.simple-modal-image').src = imageSrc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        
        // Clear image src to stop loading
        setTimeout(() => {
            if (!modal.classList.contains('active')) {
                modal.querySelector('.simple-modal-image').src = '';
            }
        }, 300);
    }

    function showPrevImage() {
        if (allImages.length === 0) return;
        currentImageIndex = (currentImageIndex - 1 + allImages.length) % allImages.length;
        modal.querySelector('.simple-modal-image').src = allImages[currentImageIndex];
    }

    function showNextImage() {
        if (allImages.length === 0) return;
        currentImageIndex = (currentImageIndex + 1) % allImages.length;
        modal.querySelector('.simple-modal-image').src = allImages[currentImageIndex];
    }
});