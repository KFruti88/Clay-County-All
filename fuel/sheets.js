fetch('https://docs.google.com/spreadsheets/d/e/2PACX-1vR_qODviVvfoveVKlgrOmJkCxIqLw1gfvftvlDGnZMDALQxcvph8o0MgVK11mhIeETQnagbNbqf2aER/pub?gid=1150011142&single=true&output=csv')
  .then(response => response.text())
  .then(data => {
    // Code to convert CSV text into an HTML table
  });
