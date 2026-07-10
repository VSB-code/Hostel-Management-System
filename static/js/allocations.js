/**
 * NIT Hostel Allocation - Allocations History JavaScript
 * Handles:
 * - Display all allocations (active + history)
 * - Filter by status
 * - Export to CSV (optional)
 */

document.addEventListener('DOMContentLoaded', function() {
    // Filter by status
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            const selected = this.value;
            const rows = document.querySelectorAll('.allocations-table tbody tr');
            
            rows.forEach(row => {
                const statusSpan = row.querySelector('.status-badge');
                if (!statusSpan) return;
                const status = statusSpan.textContent.trim();
                
                if (selected === '' || status === selected) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Search by student name or ID
    const searchInput = document.getElementById('allocationSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const query = this.value.toLowerCase().trim();
            const rows = document.querySelectorAll('.allocations-table tbody tr');
            
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

    // Export to CSV button
    const exportBtn = document.getElementById('exportCSV');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            const table = document.querySelector('.allocations-table');
            if (!table) return;
            
            let csv = [];
            const rows = table.querySelectorAll('tr');
            rows.forEach(row => {
                const cols = row.querySelectorAll('td, th');
                const rowData = [];
                cols.forEach(col => {
                    rowData.push(col.textContent.trim());
                });
                csv.push(rowData.join(','));
            });
            
            const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'allocations_export.csv';
            a.click();
            window.URL.revokeObjectURL(url);
        });
    }

    console.log('Allocations page JS loaded.');
});