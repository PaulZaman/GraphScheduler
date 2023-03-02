import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

function Graph({ edges, startnode, endnode }) {
  const svgRef = useRef();
  const key = JSON.stringify(edges);

  useEffect(() => {
    // Convert edges to nodes
    const nodes = Array.from(new Set(edges.flatMap((e) => [e.from, e.to]))).map(
      (id, index) => ({ id })
    );

    // Create links from edges
    const links = edges.map((e) => ({
      source: nodes.find((n) => n.id === e.from),
      target: nodes.find((n) => n.id === e.to),
      weight: e.weight,
    }));

    // Define the dimensions of the container element
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    // Set the initial positions of the nodes randomly within the dimensions of the SVG canvas
    nodes.forEach((node) => {
      // only set initial position for non-fixed nodes
      node.x = Math.random() * width;
      node.y = Math.random() * height;
    });

    // Define the simulation with force-directed layout
    const simulation = d3
      .forceSimulation(nodes)
      .force(
        "link",
        d3
          .forceLink(links)
          .id((d) => d.id)
          .distance(200)
      )
      .force("charge", d3.forceManyBody().strength(-50))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(70));

    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", `0 0 ${width} ${height}`);

    svg
      .append("defs")
      .append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "-0 -5 10 10")
      .attr("refX", 20)
      .attr("refY", 0)
      .attr("orient", "auto")
      .attr("markerWidth", 5)
      .attr("markerHeight", 5)
      .attr("xoverflow", "visible")
      .append("svg:path")
      .attr("d", "M 0,-5 L 10 ,0 L 0,5")
      .attr("fill", "#f00")
      .style("stroke", "none");

    // Create the links between nodes
    const link = svg
      .selectAll(".link")
      .data(links)
      .enter()
      .append("line")
      .attr("class", "link")
      .attr("stroke-width", 3)
      .attr("stroke", "red")
      .attr("marker-end", "url(#arrowhead)");

    // Create the nodes
    const node = svg
      .selectAll(".node")
      .data(nodes)
      .enter()
      .append("circle")
      .attr("class", "node")
      .attr("r", 20)
      .attr("fill", "steelblue");

    // Add labels to the nodes
    const label = svg
      .selectAll(".label")
      .data(nodes)
      .enter()
      .append("text")
      .attr("class", "label")
      .attr("text-anchor", "middle")
      .attr("fill", "white")
      .text((d) => d.id);

    // Update the position of the nodes and links on each tick of the simulation
    simulation.on("tick", () => {
      nodes.forEach((node) => {
        // constrain nodes to be within the SVG canvas
        // bottom of frame
        node.x = Math.max(0, Math.min(node.x, width - 50));
        node.y = Math.max(0, Math.min(node.y, height - 50));
        // top of frame
        node.x = Math.max(50, Math.min(node.x, width));
        node.y = Math.max(50, Math.min(node.y, height));

        // fix position of last node
        if (node.id === endnode) {
          node.x = width - (width * 1) / 20;
          node.y = height / 2;
        }
      });
      // fix position of first node:
      nodes[0].fx = width / 20;
      nodes[0].fy = height / 2;

      link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

      label.attr("x", (d) => d.x).attr("y", (d) => d.y);
    });
  }, [edges]);

  return (
    <svg
      ref={svgRef}
      className="w-full h-96"
      style={{ maxHeight: "400px" }}
      viewBox="0 0 600 400"
      key={key}
    />
  );
}

export default Graph;
