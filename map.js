const width = 800, height = 500;
const svg = d3.select("#map");

const projection = d3.geoMercator()
    .scale(500)  // Adjust scale to zoom into Asia
    .translate([width * -.2 , height * 1.3])  // Center the projection

const path = d3.geoPath().projection(projection);


const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("visibility", "hidden")
    .style("background-color", "rgba(0, 0, 0, 0.6)")
    .style("color", "white")
    .style("padding", "5px")
    .style("border-radius", "4px")
    .style("font-size", "14px");

// Set up zoom behavior
const zoom = d3.zoom()
    .scaleExtent([1, 8]) 
    .translateExtent([[0, 0], [width *1.5, height *1.5]])
    .on("zoom", zoomed);


svg.call(zoom);

// Function to handle zoom and pan
function zoomed(event) {
    const transform = event.transform;

    // Apply the transformation (zoom and pan) to the map paths and circles
    svg.selectAll("path")
        .attr("transform", transform);

    svg.selectAll("circle")
        .attr("transform", transform); 

    // Apply the transformation to the route lines
    svg.selectAll(".route-line")
        .attr("transform", transform); 
}

d3.json("https://d3js.org/world-110m.v1.json").then(worldData => {
    const countries = topojson.feature(worldData, worldData.objects.countries);

    svg.selectAll("path")
        .data(countries.features)
        .enter().append("path")
        .attr("d", path)
        .attr("fill", "white")
        .attr("stroke", "black");

    d3.csv("large_airport_coordinates.csv").then(data => {
        svg.selectAll("circle")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", d => projection([+d.longitude, +d.latitude])[0])
            .attr("cy", d => projection([+d.longitude, +d.latitude])[1])
            .attr("r", 4)
            .attr("fill", "red")
            .attr("stroke", "black")
            .attr("opacity", .9)
            .on("mouseover", function(event, d) {
                tooltip.style("visibility", "visible")
                    .text(d.iata + "\n" + d.city_name);
            })
            .on("mousemove", function(event) {
                // Update tooltip position to follow the mouse
                tooltip.style("top", (event.pageY + 5) + "px")
                    .style("left", (event.pageX + 5) + "px");
            })
            .on("mouseout", function() {
                tooltip.style("visibility", "hidden");
            })
            .on("click", function(event, d) {
                const selectedIATA = d.iata;
                const originCoords = projection([+d.longitude, +d.latitude]);

                // Remove previous lines before drawing new ones
                svg.selectAll(".route-line").remove();

                // Get the current zoom transform
                const transform = event.transform;

                // Load connections data
                d3.csv("large_connections.csv").then(connections => {

                    const destinations = connections.filter(conn => conn.Origin === selectedIATA);

                    svg.selectAll("circle").attr("fill", "gray");

                    d3.select(this).attr("fill", "red");

                    svg.selectAll("circle")
                        .filter(d => destinations.some(conn => conn.Destination === d.iata))
                        .attr("fill", "blue");

                    // Draw lines to destinations
                    destinations.forEach(conn => {
                        const destCoords = projection([+conn.Destination_Longitude, +conn.Destination_Latitude]);

                        // Append lines
                        svg.append("line")
                            .attr("class", "route-line")
                            .attr("x1", originCoords[0])
                            .attr("y1", originCoords[1])
                            .attr("x2", destCoords[0])
                            .attr("y2", destCoords[1])
                            .attr("stroke", "black")
                            .attr("stroke-width", 1)
                            .attr("opacity", 0.8)
                            .attr("transform", transform); 
                    });
                });
            });
    });
});
