// Set up width, height, and projection
const width = 800, height = 500;
const svg = d3.select("#map");

// Define projection (focus on Asia)
const projection = d3.geoMercator()
    .scale(450)  // Adjust scale to zoom into Asia
    .translate([width - 1000, height])  // Center the projection
    
const path = d3.geoPath().projection(projection);

// Create a tooltip div (invisible by default)
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
    .scaleExtent([1, 8]) // Set zoom limits (1x to 8x zoom)
    .translateExtent([[0, 0], [width+200, height]]) // Limit panning within the SVG bounds
    .on("zoom", zoomed);

// Apply zoom behavior to SVG
svg.call(zoom);

// Function to handle zoom and pan
function zoomed(event) {
    const transform = event.transform;
    
    // Apply the transformation (zoom and pan) to the map and the circles
    svg.selectAll("path")
        .attr("transform", transform); // Zoom/pan map paths
    
    svg.selectAll("circle")
        .attr("transform", transform); // Zoom/pan airport circles
}

// Load world map (GeoJSON)
d3.json("https://d3js.org/world-110m.v1.json").then(worldData => {
    const countries = topojson.feature(worldData, worldData.objects.countries);

    // Draw countries
    svg.selectAll("path")
        .data(countries.features)
        .enter().append("path")
        .attr("d", path)
        .attr("fill", "white")
        .attr("stroke", "black");

    // Load CSV data
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
            .attr("opacity", 0.7)
            .on("mouseover", function(event, d) {
                // Show tooltip on mouseover
                tooltip.style("visibility", "visible")
                    .text(d.iata); // Show IATA code
            })
            .on("mousemove", function(event) {
                // Update tooltip position to follow the mouse
                tooltip.style("top", (event.pageY + 5) + "px")
                    .style("left", (event.pageX + 5) + "px");
            })
            .on("mouseout", function() {
                // Hide tooltip on mouseout
                tooltip.style("visibility", "hidden");
            });
    });
});
