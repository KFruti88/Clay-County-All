// MASTER HUB CONTROL SCRIPT
document.addEventListener('DOMContentLoaded', function() {
    loadHubData();
});

async function loadHubData() {
    try {
        const response = await fetch('data.json');
        const data = await response.json();

        // 1. Apply Town Color Locks
        applyTownStyles(data.towns);

        // 2. Load the Calendar Module
        loadCalendarEvents();

    } catch (error) {
        console.error("Master Hub Load Error:", error);
    }
}

function applyTownStyles(towns) {
    if (towns.Louisville) {
        const louSection = document.getElementById('louisville-section');
        if (louSection) {
            louSection.style.backgroundColor = towns.Louisville.bg;
            louSection.style.color = towns.Louisville.text;
        }
    }
}

// CALENDAR MODULE LOGIC
async function loadCalendarEvents() {
    const calendarContainer = document.getElementById('calendar-container');
    
    try {
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

    container.innerHTML = ''; 

    // Sort: Closest date first
    events.sort((a, b) => new Date(a.date) - new Date(b.date));

    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'event-card-row'; // Using your sideways template class
        
        // Find image in description or use fallback
        const imgMatch = (event.description || "").match(/\bhttps?:\/\/\S+\.(?:png|jpg|jpeg|gif)\b/i);
        const imgUrl = imgMatch ? imgMatch[0] : 'https://via.placeholder.com/180?text=Event';
        const cleanDesc = (event.description || "No details provided.").replace(imgUrl, '').trim();

        // Template logic: Adding onclick to open the Single Event View
        eventCard.onclick = () => openEventDetails(event.title, event.date, imgUrl, cleanDesc);

        eventCard.innerHTML = `
            <img src="${imgUrl}" class="event-image-slot">
            <div class="event-details-slot">
                <h2 class="event-title">${event.title}</h2>
                <p class="event-desc-snippet">${cleanDesc.substring(0, 150)}...</p>
                <div class="event-time-tag">
                    📅 ${event.date} | ⌚ ${event.time || 'TBA'}
                </div>
            </div>
        `;
        
        container.appendChild(eventCard);
    });
}

/* This function opens the "Single Event" view (The Modal) */
function openEventDetails(title, date, img, description) {
    document.getElementById('modal-title').innerText = title;
    document.getElementById('modal-date').innerText = date;
    document.getElementById('modal-detail-date').innerText = date;
    document.getElementById('modal-img').src = img;
    document.getElementById('modal-desc').innerText = description;

    // Show the pop-up
    document.getElementById('event-modal').style.display = 'flex';
}

/* This function closes the view */
function closeEvent() {
    document.getElementById('event-modal').style.display = 'none';
}
