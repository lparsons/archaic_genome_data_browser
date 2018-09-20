var mymap = L.map('mapid').setView([10, 0], 2);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.outdoors',
    accessToken: 'pk.eyJ1IjoibHBhcnNvbnMiLCJhIjoiY2ptYXJtaWlmMW92YzNwcXFjdW5uZ2d4cCJ9.C_9_7EWGRR5zKOQfzSpx9g'
}).addTo(mymap);