/**
 * NIT Hostel Allocation - Student Dashboard JavaScript
 * Handles:
 * - Live occupancy stats (fetch + render)
 * - AJAX form submission for room allocation
 * - Auto-refresh stats every 15 seconds
 */

// Fetch occupancy stats from API
async function fetchOccupancy() {
    try {
        const response = await fetch('/api/occupancy');
        const data = await response.json();
        if (data.success) {
            renderStats(data.stats);
        } else {
            document.getElementById('statsContainer').innerHTML = 
                '<div style="color:#ffaaaa;">Failed to load stats</div>';
        }
    } catch (err) {
        document.getElementById('statsContainer').innerHTML = 
            '<div style="color:#ffaaaa;">Network error</div>';
    }
}

// Render occupancy stats in the UI
function renderStats(stats) {
    const container = document.getElementById('statsContainer');
    container.innerHTML = '';
    let totalBeds = 0, totalOccupied = 0;
    
    stats.forEach(hostel => {
        totalBeds += hostel.total_beds;
        totalOccupied += hostel.occupied_beds;
        const percent = (hostel.occupied_beds / hostel.total_beds) * 100;
        
        const hostelDiv = document.createElement('div');
        hostelDiv.className = 'hostel-item';
        hostelDiv.innerHTML = `
            <div class="hostel-name">
                <span>🏛️ ${hostel.hostel_name}</span>
                <span>${hostel.occupied_beds}/${hostel.total_beds}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${percent}%;"></div>
            </div>
            <div class="stats-numbers">
                <span>✅ Available: ${hostel.available_beds}</span>
                <span>🧑‍🎓 Occupied: ${hostel.occupied_beds}</span>
            </div>
        `;
        container.appendChild(hostelDiv);
    });
    
    const totalPercent = (totalOccupied / totalBeds) * 100;
    document.getElementById('totalSummary').innerHTML = `
        📊 Overall: ${totalOccupied} / ${totalBeds} beds filled (${totalPercent.toFixed(1)}%)
    `;
}

// Show flash message
function showMessage(msg, type) {
    const messageDiv = document.getElementById('messageArea');
    messageDiv.innerHTML = `<div class="flash-message ${type}">${msg}</div>`;
    setTimeout(() => {
        if (messageDiv.firstChild) messageDiv.firstChild.remove();
    }, 5000);
}

// Handle form submission via AJAX
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('allocationForm');
    const submitBtn = document.getElementById('submitBtn');
    
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const student_id = document.getElementById('student_id').value.trim();
            const student_name = document.getElementById('student_name').value.trim();

            if (!student_id || !student_name) {
                showMessage('❌ Please fill all fields', 'error');
                return;
            }

            // Show loading state
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loader"></span> Processing...';
            submitBtn.disabled = true;

            try {
                const response = await fetch('/book', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams({ student_id, student_name })
                });
                const text = await response.text();
                
                if (text.includes('✅') || text.includes('Success')) {
                    showMessage(text, 'success');
                    document.getElementById('student_id').value = '';
                    document.getElementById('student_name').value = '';
                    fetchOccupancy(); // refresh stats
                } else if (text.includes('❌') || text.includes('Error') || text.includes('full')) {
                    showMessage(text, 'error');
                } else {
                    showMessage(text, 'info');
                }
            } catch (err) {
                showMessage('Network error. Please try again.', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    // Refresh button
    const refreshBtn = document.getElementById('refreshStats');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', fetchOccupancy);
    }

    // Initial load + auto-refresh
    fetchOccupancy();
    setInterval(fetchOccupancy, 15000);
});