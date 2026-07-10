/**
 * NIT Hostel Allocation - Admin Dashboard JavaScript
 * Handles:
 * - Vacate confirmation
 * - System reset confirmation
 * - Auto-refresh dashboard (optional)
 */

document.addEventListener('DOMContentLoaded', function() {
    // Confirm before vacating a room
    const vacateForms = document.querySelectorAll('.vacate-form');
    vacateForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('⚠️ Are you sure you want to vacate this room?\n\nThis action will:\n- Mark allocation as VACATED\n- Free up the room for others\n- Can be reverted by re-allocating')) {
                e.preventDefault();
            }
        });
    });

    // Confirm before resetting entire system
    const resetForm = document.getElementById('resetForm');
    if (resetForm) {
        resetForm.addEventListener('submit', function(e) {
            const confirmInput = document.getElementById('resetConfirm');
            if (!confirmInput || confirmInput.value !== 'YES') {
                e.preventDefault();
                alert('⚠️ Please type "YES" to confirm the system reset.');
                return;
            }
            
            if (!confirm('🚨 DANGER: This will:\n- Delete ALL allocations\n- Reset ALL rooms to AVAILABLE\n- Remove ALL student data\n\nAre you absolutely sure?')) {
                e.preventDefault();
            }
        });
    }

    // Auto-refresh dashboard every 60 seconds (optional)
    // Uncomment if you want auto-refresh
    /*
    setInterval(() => {
        location.reload();
    }, 60000);
    */

    console.log('Admin JS loaded successfully.');
});