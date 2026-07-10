/**
 * NIT Hostel Allocation - Rooms Explorer JavaScript
 * Handles:
 * - Search/filter rooms
 * - Toggle room details
 * - Auto-refresh room status (optional)
 */

document.addEventListener('DOMContentLoaded', function() {
    // Search functionality: filter rooms by number
    const searchInput = document.getElementById('roomSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const query = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll('.rooms-table tbody tr');
            
            rows.forEach(row => {
                const roomNumber = row.querySelector('.room-pill')?.textContent || '';
                if (roomNumber.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Filter by status
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            const selected = this.value.toLowerCase();
            const rows = document.querySelectorAll('.rooms-table tbody tr');
            
            rows.forEach(row => {
                const statusSpan = row.querySelector('.status-label');
                if (!statusSpan) return;
                const status = statusSpan.textContent.toLowerCase();
                
                if (selected === '' || status === selected) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Filter by hostel (if hostel dropdown exists)
    const hostelFilter = document.getElementById('hostelFilter');
    if (hostelFilter) {
        hostelFilter.addEventListener('change', function() {
            const selected = this.value;
            const hostelCards = document.querySelectorAll('.hostel-card');
            
            hostelCards.forEach(card => {
                const hostelName = card.dataset.hostel || '';
                if (selected === '' || hostelName === selected) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Toggle room details (expand/collapse)
    const toggleButtons = document.querySelectorAll('.toggle-details');
    toggleButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const details = this.closest('tr').querySelector('.room-details');
            if (details) {
                details.style.display = details.style.display === 'none' ? '' : 'none';
                this.textContent = details.style.display === 'none' ? '▶' : '▼';
            }
        });
    });

    console.log('Rooms page JS loaded successfully.');
});