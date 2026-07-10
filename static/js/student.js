/**
 * NIT Hostel Allocation - Students Management JavaScript
 * Handles:
 * - Display all students
 * - Search/filter students
 * - View student allocation history
 */

document.addEventListener('DOMContentLoaded', function() {
    // Search students by name or roll number
    const searchInput = document.getElementById('studentSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const query = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll('.students-table tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Filter by allocation status
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            const selected = this.value;
            const rows = document.querySelectorAll('.students-table tbody tr');
            
            rows.forEach(row => {
                const statusBadge = row.querySelector('.status-badge');
                if (!statusBadge) return;
                const status = statusBadge.textContent.trim();
                
                if (selected === '' || status === selected) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    console.log('Students page JS loaded.');
});