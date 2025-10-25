// Configuration
// Auto-detect backend port for local development
let API_BASE_URL = 'http://localhost:5000/api';

// State
let currentItineraryId = null;

// DOM Elements
const tripInput = document.getElementById('trip-input');
const planButton = document.getElementById('plan-button');
const buttonText = document.getElementById('button-text');
const buttonLoading = document.getElementById('button-loading');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');
const errorText = document.getElementById('error-text');
const intentDisplay = document.getElementById('intent-display');
const itineraryDisplay = document.getElementById('itinerary-display');
const downloadButton = document.getElementById('download-button');
const examplesGrid = document.getElementById('examples-grid');
const citiesList = document.getElementById('cities-list');

// Detect backend port on startup
async function detectBackendPort() {
    const ports = [5000, 5001, 5002];
    for (const port of ports) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 1000);

            const response = await fetch(`http://localhost:${port}/api/health`, {
                method: 'GET',
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (response.ok) {
                API_BASE_URL = `http://localhost:${port}/api`;
                console.log(`✅ Backend detected on port ${port}`);
                return;
            }
        } catch (e) {
            // Port not available, try next
        }
    }
    console.warn('⚠️ Backend not detected on ports 5000, 5001, or 5002');
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await detectBackendPort();
    loadExamples();
    loadCities();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    planButton.addEventListener('click', handlePlanTrip);
    tripInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            handlePlanTrip();
        }
    });
    downloadButton.addEventListener('click', handleDownload);
}

// Load Examples
async function loadExamples() {
    try {
        const response = await fetch(`${API_BASE_URL}/examples`);
        const data = await response.json();

        examplesGrid.innerHTML = data.examples.map(example => `
            <div class="example-card" onclick="useExample('${escapeHtml(example.prompt)}')">
                <h4>${example.title}</h4>
                <p>${example.description}</p>
                <p class="example-prompt">"${example.prompt}"</p>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading examples:', error);
        examplesGrid.innerHTML = '<p>Could not load examples</p>';
    }
}

// Load Cities
async function loadCities() {
    try {
        const response = await fetch(`${API_BASE_URL}/cities`);
        const data = await response.json();

        citiesList.innerHTML = data.cities.map(city =>
            `<span class="city-tag">${city}</span>`
        ).join('');
    } catch (error) {
        console.error('Error loading cities:', error);
        citiesList.innerHTML = 'Error loading cities';
    }
}

// Use Example
function useExample(prompt) {
    tripInput.value = prompt;
    tripInput.focus();
    // Scroll to input
    tripInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Handle Plan Trip
async function handlePlanTrip() {
    const message = tripInput.value.trim();

    if (!message) {
        showError('Please enter a trip request');
        return;
    }

    // Show loading state
    setLoading(true);
    hideError();
    hideResults();

    try {
        const response = await fetch(`${API_BASE_URL}/plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to plan trip');
        }

        if (data.success) {
            currentItineraryId = data.itinerary_id;
            displayResults(data);
        } else {
            throw new Error(data.error || 'Unknown error');
        }
    } catch (error) {
        console.error('Error planning trip:', error);
        showError(error.message || 'Failed to plan trip. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Display Results
function displayResults(data) {
    // Display intent
    displayIntent(data.intent);

    // Display itinerary
    displayItinerary(data.itinerary);

    // Show results section
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display Intent
function displayIntent(intent) {
    const preferences = intent.preferences && intent.preferences.length > 0
        ? `<div class="preferences-list">
            ${intent.preferences.map(pref => `<span class="preference-tag">${pref}</span>`).join('')}
           </div>`
        : '<span class="intent-value">General exploration</span>';

    intentDisplay.innerHTML = `
        <h3>📋 Trip Details</h3>
        <div class="intent-items">
            <div class="intent-item">
                <span class="intent-label">Destination</span>
                <span class="intent-value">${escapeHtml(intent.destination)}</span>
            </div>
            <div class="intent-item">
                <span class="intent-label">Duration</span>
                <span class="intent-value">${intent.days} ${intent.days === 1 ? 'day' : 'days'}</span>
            </div>
            <div class="intent-item">
                <span class="intent-label">Interests</span>
                ${preferences}
            </div>
        </div>
    `;
}

// Display Itinerary
function displayItinerary(itinerary) {
    // Group items by day
    const dayGroups = {};
    itinerary.items.forEach(item => {
        if (!dayGroups[item.day]) {
            dayGroups[item.day] = [];
        }
        dayGroups[item.day].push(item);
    });

    // Sort days
    const sortedDays = Object.keys(dayGroups).sort((a, b) => a - b);

    // Generate HTML
    itineraryDisplay.innerHTML = sortedDays.map(day => {
        const activities = dayGroups[day];
        const dayName = getDayName(parseInt(day), activities[0].area);

        return `
            <div class="day-section">
                <div class="day-header">
                    <span class="day-number">${day}</span>
                    <span>${dayName}</span>
                </div>
                <div class="activity-list">
                    ${activities.map(activity => `
                        <div class="activity-item">
                            <div class="activity-time">${activity.time}</div>
                            <div class="activity-details">
                                <div class="activity-name">
                                    <a href="${activity.url}" target="_blank" rel="noopener">
                                        ${escapeHtml(activity.name)}
                                    </a>
                                </div>
                                <div class="activity-meta">
                                    <span class="activity-area">📍 ${escapeHtml(activity.area)}</span>
                                    <div class="activity-tags">
                                        ${activity.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');
}

// Get Day Name
function getDayName(dayNumber, area) {
    const dayNames = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'];
    const name = dayNames[dayNumber - 1] || `Day ${dayNumber}`;
    return area ? `${name} - ${area}` : name;
}

// Handle Download
async function handleDownload() {
    if (!currentItineraryId) {
        showError('No itinerary to download');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/download/${currentItineraryId}`);

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to download calendar');
        }

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'trip_itinerary.ics';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // Show success message
        showTemporaryMessage('Calendar file downloaded! Import it to your calendar app.');
    } catch (error) {
        console.error('Error downloading calendar:', error);
        showError(error.message || 'Failed to download calendar');
    }
}

// Show Temporary Message
function showTemporaryMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'success-message';
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 300);
    }, 3000);
}

// UI Helper Functions
function setLoading(isLoading) {
    planButton.disabled = isLoading;
    buttonText.style.display = isLoading ? 'none' : 'inline';
    buttonLoading.style.display = isLoading ? 'inline' : 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideError() {
    errorSection.style.display = 'none';
}

function hideResults() {
    resultsSection.style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(style);
