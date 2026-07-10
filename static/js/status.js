/**
 * NIT Hostel Allocation - Status Page JavaScript
 * Handles:
 * - Fetch and display detailed occupancy stats
 * - Auto-refresh every 30 seconds
 */

async function loadFullStats() {
    try {
        const res = await fetch('/api/occupancy');
        const data = await res.json();
        
        if (!data.success) {
            document.getElementById('statsTable').innerHTML = 
                '<p style="color:red;">Failed to load stats</p>';
            return;
        }
        
        let html = `
            <table>
                <thead>
                    <tr>
                        <th>Hostel</th>
                        <th>Total Rooms</th>
                        <th>Total Beds</th>
                        <th>Occupied</th>
                        <th>Available</th>
                        <th>Occupancy Rate</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        data.stats.forEach(h => {
            const rate = ((h.occupied_beds / h.total_beds) * 100).toFixed(1);
            const badge = h.available_beds === 0 
                ? '<span class="badge-full">FULL</span>' 
                : '<span class="badge-avail">AVAILABLE</span>';
            
            html += `
                <tr>
                    <td><strong>${h.hostel_name}</strong> ${badge}</td>
                    <td>${h.total_rooms}</td>
                    <td>${h.total_beds}</td>
                    <td>${h.occupied_beds}</td>
                    <td>${h.available_beds}</td>
                    <td>
                        <div class="progress">
                            <div class="progress-fill" style="width: ${rate}%;"></div>
                        </div>
                        ${rate}%
                    </td>
                </tr>
            `;
        });
        
        html += `</tbody></table>`;
        document.getElementById('statsTable').innerHTML = html;
        
    } catch (err) {
        document.getElementById('statsTable').innerHTML = 
            '<p style="color:red;">Network error loading stats</p>';
    }
}

// Load on page load
document.addEventListener('DOMContentLoaded', function() {
    loadFullStats();
    // Auto-refresh every 30 seconds
    setInterval(loadFullStats, 30000);
});