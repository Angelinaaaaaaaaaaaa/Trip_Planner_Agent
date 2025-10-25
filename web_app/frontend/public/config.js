// Configuration for API endpoint
// Change this when deploying to production
const API_BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:5002/api'  // Local development
  : 'https://your-backend-url.com/api';  // Production - UPDATE THIS!
