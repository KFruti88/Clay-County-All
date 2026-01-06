// #keep full story logic - Clay County Calendar Module
document.addEventListener('DOMContentLoaded', function() {
    loadCalendarData();
});

async function loadCalendarData() {
    const calendarContainer = document.getElementById('calendar-container'); // Ensure this ID exists in your Index.html
    
    try {
        // FIXED URL: Fetching directly from your GitHub Pages to avoid "Unexpected Token" errors
        const response = await fetch('https://kfruti88.github.io/Clay-County-All/Calendar/calendar_data.json');
        
        if (!response.ok) {
            throw new Error('Calendar data not found');
        }

        const events = await response.json();
        renderCalendar(events);

    } catch (error) {
        console.error('Error loading calendar:', error);
        if (calendarContainer) {
            calendarContainer.innerHTML = `<p style="color:red; text-align:center;">Calendar Sync Error: Updating events...</p>`;
        }
    }
}

function renderCalendar(events) {
    const container = document.getElementById('calendar-container');
    if (!container) return;

    container.innerHTML = ''; // Clear loading message

    if (events.length === 0) {
        container.innerHTML = '<p style="text-align:center; color:#888;">No upcoming events scheduled.</p>';
        return;
    }

    // Sort events by date (closest first)
    events.sort((a, b) => new Date(a.date) - new Date(b.date));

    events.forEach(event => {
        const eventCard = document.createElement('div');
        eventCard.className = 'calendar-card';
        
        // Styling matches your Portal theme
        eventCard.style.background = '#1f1f1f';
        eventCard.style.padding = '15px';
        eventCard.style.marginBottom = '15px';
        eventCard.style.borderRadius = '8px';
        eventCard.style.borderLeft = '4px solid #00ff00';

        eventCard.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h3 style="color: #00ff00; margin: 0 0 5px 0;">${event.title}</h3>
                    <p style="color: #888; font-size: 0.9rem; margin: 0;">
                        <strong>Date:</strong> ${event.date} | <strong>Time:</strong> ${event.time || 'TBA'}
                    </p>
                </div>
                <span style="background: #333; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; color: #fff;">
                    ${event.location || 'Clay County'}
                </span>
            </div>
            <div style="margin-top: 10px; color: #ddd; white-space: pre-wrap;">
                ${event.description || 'No description provided.'}
            </div>
        `;
        
        container.appendChild(eventCard);
    });
}
