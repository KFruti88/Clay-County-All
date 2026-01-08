// CALENDAR MODULE LOGIC
async function loadCalendarEvents() {
    const calendarContainer = document.getElementById('calendar-container');
    
    try {
        // Attempting to fetch real data
        const response = await fetch('https://kfruti88.github.io/Clay-County-All/Calendar/calendar_data.json');
        let events = [];
        
        if (response.ok) {
            events = await response.json();
        }

        // --- TEST EVENTS START ---
        // These ensure you have exactly 3 cards to look at for the test
        const testEvents = [
            {
                title: "🐺 Pack Community Meetup",
                date: "2026-01-15",
                time: "6:00 PM",
                description: "Testing the sideways layout. This text should be on the left and the image on the right! https://werewolf.ourflora.com/wp-content/uploads/2025/12/WolfPack-Friends.png"
            },
            {
                title: "🏫 School Returns",
                date: "2026-01-06",
                time: "8:00 AM",
                description: "Back to school test event. Checking the detailed modal view. https://werewolf.ourflora.com/wp-content/uploads/2025/12/image_2025-12-22_222907634.png"
            },
            {
                title: "🚜 Farm Consignment Sale",
                date: "2026-01-19",
                time: "9:00 AM",
                description: "Mt. Erie Ruritan Farm Consignment Sale test. No used tires! https://raw.githubusercontent.com/KFruti88/Clay-County-Fuel/main/images/mach1.png"
            }
        ];
        // Combine real events with test events
        events = [...events, ...testEvents];
        // --- TEST EVENTS END ---

        renderCalendar(events);

    } catch (error) {
        console.error('Calendar Sync Error:', error);
        // Fallback to test events only if fetch fails completely
        renderCalendar(testEvents); 
    }
}

function renderCalendar(events) {
    const container = document.getElementById('calendar-container');
    if (!container) return;

    container.innerHTML = ''; 

    // 1. Sort by date (Closest first)
    events.sort((a, b) => new Date(a.date) - new Date(b.date));

    // 2. LIMIT TO TOP 3 for the Main Page view
    const upcoming = events.slice(0, 3);

    upcoming.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'event-card-row'; // Sideways layout
        
        const imgMatch = (event.description || "").match(/\bhttps?:\/\/\S+\.(?:png|jpg|jpeg|gif)\b/i);
        const imgUrl = imgMatch ? imgMatch[0] : '';
        const cleanDesc = (event.description || "No details provided.").replace(imgUrl, '').trim();

        // Template: TEXT on LEFT, IMAGE on RIGHT
        eventCard.innerHTML = `
            <div class="event-details-slot">
                <div class="event-time-tag">📅 ${event.date} | ⌚ ${event.time || 'TBA'}</div>
                <h2 class="event-title">${event.title}</h2>
                <p class="event-desc-snippet">${cleanDesc.substring(0, 120)}...</p>
            </div>
            ${imgUrl ? `<img src="${imgUrl}" class="event-image-slot">` : ''}
        `;
        
        // Link to the "School Returns" Pop-up logic
        eventCard.onclick = () => openEventDetails(event.title, event.date, imgUrl, cleanDesc);
        
        container.appendChild(eventCard);
    });
}
