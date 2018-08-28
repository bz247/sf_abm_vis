mapboxgl.accessToken = process.env.MapboxAccessToken;
var map = new mapboxgl.Map({
    container: 'map', // container id
    style: 'mapbox://styles/mapbox/dark-v9', // stylesheet location: streets-v9
    center: [-122.45, 37.75],//[-71.97722138410576, -13.517379300798098], // starting position [lng, lat]
    zoom: 11 // starting zoom
});

map.on('load', function () {
    get_route();
    get_closure();

});

function get_closure() {
    map.on('click', function(e) {
        var click_coord = [e.lngLat.lng, e.lngLat.lat];
        console.log(click_coord);
        $.ajax({
            'method': 'POST',
            'url': '/get_closure',
            'data': JSON.stringify(click_coord),
            'contentType': 'application/json;charset=UTF-8',
            success: function(response) {
                console.log('successfully posted click coordinate');
            },
            error: function(error) {
                console.log(error);
            }
        }).done(function(data) {
            var paths = data['paths'];
            if (map.getLayer('updated_shortest_paths')){map.removeLayer('updated_shortest_paths')}
            if (map.getSource('updated_shortest_paths')){map.removeSource('updated_shortest_paths')}
            map.addLayer({
                'id': 'updated_shortest_paths',
                'type': 'line',
                'source': {'type': 'geojson','data': paths},
                'paint': {'line-width': 1, 'line-color': 'rgba(255,0,255,1)'}
            })
        });
    })
}

function get_route() {
    $.ajax({
        'method': 'GET',
        'url': '/get_route',
    }).done(function(data) {
        var paths = data['paths'];
        map.addLayer({
            'id': 'shortest_paths',
            'type': 'line',
            'source': {
                'type': 'geojson',
                'data': paths
            },
            'paint': {
                'line-width': 1,
                'line-color': 'rgba(255,0,0,1)'
            }
        })

        var origins = data['origins'];
        map.addLayer({
            'id': 'shortest_path_origins',
            'type': 'circle',
            'source': {
                'type': 'geojson',
                'data': origins
            },
            'paint': {
                'circle-radius': 5,
                'circle-color': 'rgba(0,255,0,1)'
            }
        })

        var destinations = data['destinations'];
        map.addLayer({
            'id': 'shortest_path_destinations',
            'type': 'circle',
            'source': {
                'type': 'geojson',
                'data': destinations
            },
            'paint': {
                'circle-radius': 5,
                'circle-color': 'rgba(0,0,255,1)'
            }
        })

    })
}