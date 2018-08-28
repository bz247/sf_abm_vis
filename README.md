# sf_abm_vis
* Visualisation of the shortest path between origin-destination (OD) pairs
* Modification of the road network through screen clicking and visualising the new path based on the modified network

### Preparation
* Install python3 and required packages through, e.g., `pip3 install flask`
* Install `python-igraph`. If you are using Mac, you can follow this [SO link](https://stackoverflow.com/a/46335152)
* Get an access token from [Mapbox](https://www.mapbox.com/help/how-access-tokens-work/) and set environment variable in the terminal with `export MapboxAccessToken=[your access token]`

### Running
* Start with the server `python3 server.py`
* Open a browser window and navigate to `127.0.0.1:5000`. It may take 1-2 seconds for the shortest paths in undisturbed network to show
* Click on any point on the map (preferrably near an exisiting path) to simulate a local disruption. New paths will be calculated in the server and visualised in the browser

