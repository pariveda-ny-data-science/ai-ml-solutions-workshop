var scaled = 10;

function rescaleTo(multiplier, ratio) {
  scaled = 12 + (10 * ratio / multiplier);
}

function getPathData(radius, startX, startY) {
  radius = 1.05 * radius;
  return `m${startX-radius},${startY} a${radius},${radius} 0 0 1 ${2*radius}, 0`;
}

function drawToSVG(root) {
  // Prepare the svg element dimensions
  d3.selectAll("svg > *").remove();
  var svg = d3.select("svg"),
    diameter = +svg.attr("width"),
    margin = 25,
    g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

  // Structure the data for circle pack layout
  var pack = d3.pack()
    .size([diameter - margin, diameter - margin])
    .padding(function (d, i) {
      return d.r || 0;
    });

  // Fetch the top most element
  root = d3.hierarchy(root)
    .sum(function (d) {
      return d.value;
    })
    .sort(function (a, b) {
      return b.value - a.value;
    });

  // Prep variables for the active element & root's children
  var focus = root,
    nodes = pack(root).descendants(),
    view;

  // Draw the circles! Nested and all
  var circle = g.selectAll("circle")
    .data(nodes)
    .enter().append("circle")
    .attr("class", function (d) {
      return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root";
    })
    .style("fill", function (d) {
      return d3.interpolateBrBG(d.data.sentiment);
    })
    .attr("test", function (d) {
      return d.data.sentiment;
    })
    .on("click", function (d) {
      if (focus !== d) {
        zoom(d);
        displayActiveData(d.data);
      }
      d3.event.stopPropagation();
    })
    .on("mouseover", function (d) {
      displayHoverData(d.data);
    });

  // Define the arc paths for each data element
  var paths = g.selectAll("defs")
    .data(nodes)
    .enter().append('path')
    .attr("d", function (d) {
      return getPathData(d.r, d.x - root.x, d.y - root.y);
    })
    .attr("id", function (d, i) {
      return `curvedPath${i}`;
    });


  // Write out the text for each of the data elements
  var text = g.selectAll("text")
    .data(nodes)
    .enter().append("text")
    .attr("class", "label")
    .style("fill-opacity", function (d) {
      return (d === root || d.parent === root) ? 1 : 0;
    })
    .style("display", function (d) {
      return (d === root || d.parent === root) ? "inline" : "none";
    })
    .append('textPath')
    .attr("startOffset", "25%")
    .attr("xlink:xlink:href", function (d, i) {
      return `#curvedPath${i}`;
    })
    .text(function (d) {
      return d.data.name.length > 20 ? `${d.data.name.substr(0,20)}...` : d.data.name;
    });

  // Prep variables for group modifications on circles + text
  var node = g.selectAll("circle");
  var textNode = g.selectAll("text");
  var pathNode = g.selectAll("path");

  // "Reset" the zoom if you click outside of a circle
  svg
    .on("click", function () {
      zoom(root);
    });

  // Start with us zoomed into the root
  zoomTo([root.x, root.y, root.r * 2 + margin]);

  // Function to do a sick zoom
  function zoom(d) {
    var focus0 = focus;
    focus = d;

    // Ease into the zoom
    var transition = d3.transition()
      .duration(d3.event.altKey ? 7500 : 750)
      .tween("zoom", function (d) {
        var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
        return function (t) {
          zoomTo(i(t));
        };
      });

    // Have text fade out / in based on whether you or your parent is the one in focus
    transition.selectAll("text")
      .filter(function (d) {
        return d === focus || d.parent === focus || this.style.display === "inline";
      })
      .style("fill-opacity", function (d) {
        return (d === focus || d.parent === focus) ? 1 : 0;
      })
      .on("start", function (d) {
        if (d === focus || d.parent === focus) this.style.display = "inline";
      })
      .on("end", function (d) {
        if (d.parent !== focus && d !== focus) this.style.display = "none";
      });
  }

  function zoomTo(v) {
    rescaleTo(v[2], diameter);
    var k = diameter / v[2];
    view = v;
    var rScale = (r) => (r * k);
    var xScale = (x) => (x - v[0]) * k;
    var yScale = (y) => (y - v[1]) * k;
    node.attr("transform", function (d) {
      return "translate(" + xScale(d.x) + "," + yScale(d.y) + ")";
    });
    pathNode.attr("d", function (d) {
      return getPathData(rScale(d.r), xScale(d.x), yScale(d.y));
    })
    textNode.attr("font-size", function (d) {
      return `${Math.min(20, (scaled * d.r) * 0.05)}`;
    });
    circle.attr("r", function (d) {
      return rScale(d.r);
    });
  }
}