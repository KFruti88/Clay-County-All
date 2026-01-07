// MASTER HUB CONTROL SCRIPT
document.addEventListener('DOMContentLoaded', function() {
    loadHubData();
});

async function loadHubData() {
    try {
        // Fetching the Master Data (Town colors, News, etc.)
        const response = await fetch('data.json');
        const data = await response.json();

        // 1. Apply Town Color Locks
        applyTownStyles(data.towns);

        // 2. Load the Calendar Module
        // We call the specific calendar fetcher here
        loadCalendarEvents();

    } catch (error) {
        console.error("Master Hub Load Error:", error);
    }
}

// Handles the Visual Effect for the different town sections
function applyTownStyles(towns) {
    if (towns.Louisville) {
        const louSection = document.getElementById('louisville-section');
        if (louSection) {
            louSection.style.backgroundColor = towns.Louisville.bg;
            louSection.style.color = towns.Louisville.text;
        }
    }
    // Add other towns (Flora, Xenia, etc.) here as needed
}

// CALENDAR MODULE LOGIC
async function loadCalendarEvents() {
    const calendarContainer = document.getElementById('calendar-container');
    
    try {
        // Fetching from your specific Calendar JSON
        const response = await fetch('https://kfruti88.github.io/Clay-County-All/Calendar/calendar_data.json');
        
        if (!response.ok) throw new Error('Calendar data not found');

        const events = await response.json();
        renderCalendar(events);

    } catch (error) {
        console.error('Calendar Sync Error:', error);
        if (calendarContainer) {
            calendarContainer.innerHTML = `<p style="color:red; text-align:center;">Sync Error: Checking for updates...</p>`;
        }
    }
}

function renderCalendar(events) {
    const container = document.getElementById('calendar-container');
    if (!container) return;

    container.innerHTML = ''; // Clear loading state

    // Sort: Closest date first
    events.sort((a, b) => new Date(a.date) - new Date(b.date));

    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'calendar-card';
        
        // This keeps your specific "Portal" visual effect
        eventCard.innerHTML = `
            <div class="event-header">
                <div class="event-info">
                    <h3 class="event-title">${event.title}</h3>
                    <p class="event-meta">
                        <strong>Date:</strong> ${event.date} | <strong>Time:</strong> ${event.time || 'TBA'}
                    </p>
                </div>
                <span class="event-location">${event.location || 'Clay County'}</span>
            </div>
            <div class="event-desc">${event.description || 'No description provided.'}</div>
        `;
        
        container.appendChild(eventCard);
    });
}
