import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { drag } from "d3-drag";

function Graph({ edges, endnode, criticalPath = null }) {
  const svgRef = useRef();
  const key = JSON.stringify(edges);
  const criticalPathEdges = [];

  if (criticalPath) {
    for (let i = 0; i < criticalPath.length - 1; i++) {
      criticalPathEdges.push({
        from: criticalPath[i],
        to: criticalPath[i + 1],
      });
    }
  }

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
          .distance(100)
      )
      .force("charge", d3.forceManyBody().strength(-100))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(75))
      .alphaDecay(0);

    const svg = d3
      .select(svgRef.current)
      .attr("viewBox", `0 0 ${width} ${height}`);

    // Create the links between nodes
    const link = createLinks(svg, links, criticalPathEdges);

    // Create the labels for the links
    const linkLabel = createLinkLabels(svg, links);

    // Create the nodes
    const node = createNodes(svg, nodes);

    // Add labels to the nodes
    const label = createLabels(svg, nodes, simulation);

    // Update the position of the nodes and links on each tick of the simulation
    simulation.on("tick", () => {
      updateNodes(nodes, node, width, height, endnode);
      updateLinks(link, linkLabel);
      label.attr("x", (d) => d.x).attr("y", (d) => d.y + 5);
    });
  }, [edges]);

  return (
    <svg
      ref={svgRef}
      className="w-full h-full"
      style={{ maxHeight: "400px" }}
      viewBox="0 0 600 400"
      key={key}
    />
  );
}

function createLinks(svg, links, criticalPathEdges) {
  // create arrowhead marker
  svg
    .append("defs")
    .append("marker")
    .attr("id", "arrowhead-red")
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

  svg
    .append("defs")
    .append("marker")
    .attr("id", "arrowhead-green")
    .attr("viewBox", "-0 -5 10 10")
    .attr("refX", 20)
    .attr("refY", 0)
    .attr("orient", "auto")
    .attr("markerWidth", 5)
    .attr("markerHeight", 5)
    .attr("xoverflow", "visible")
    .append("svg:path")
    .attr("d", "M 0,-5 L 10 ,0 L 0,5")
    .attr("fill", "green")
    .style("stroke", "none");

  return svg
    .selectAll(".link")
    .data(links)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke-width", 3)
    .attr("marker-end", (d) => {
      for (let i = 0; i < criticalPathEdges.length; i++) {
        if (
          d.source.id.toString() === criticalPathEdges[i].from.toString() &&
          d.target.id.toString() === criticalPathEdges[i].to.toString()
        ) {
          return "url(#arrowhead-green)";
        }
      }
      return "url(#arrowhead-red)";
    })
    .attr("stroke", (d) => {
      for (let i = 0; i < criticalPathEdges.length; i++) {
        if (
          d.source.id.toString() === criticalPathEdges[i].from.toString() &&
          d.target.id.toString() === criticalPathEdges[i].to.toString()
        ) {
          return "green";
        }
      }
      return "red";
    });
}

function createArrowHead(svg) {}

function createLinkLabels(svg, links) {
  return svg
    .selectAll(".link-label")
    .data(links)
    .enter()
    .append("text")
    .attr("class", "link-label")
    .attr("font-size", "12px")
    .attr("fill", "white")
    .attr("text-anchor", "middle")
    .text((d) => d.weight);
}

function createNodes(svg, nodes) {
  const dragging = drag()
    .on("start", (event, d) => dragStart(event, d, simulation))
    .on("drag", (event, d) => dragging(event, d, simulation))
    .on("end", (event, d) => dragEnd(event, d, simulation));
  return svg
    .selectAll(".node")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("class", "node cursor-pointer")
    .attr("r", 20)
    .attr("fill", "steelblue")
    .call(dragging);
}

function createLabels(svg, nodes, simulation) {
  const dragLabel = drag()
    .on("start", (event, d) => dragStart(event, d, simulation))
    .on("drag", (event, d) => dragging(event, d, simulation))
    .on("end", (event, d) => dragEnd(event, d, simulation));

  return svg
    .selectAll(".label")
    .data(nodes)
    .enter()
    .append("text")
    .attr("class", "label cursor-pointer")
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .text((d) => d.id)
    .call(dragLabel);
}

function updateNodes(nodes, node, width, height, endnode) {
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
  node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
}

function updateLinks(link, linkLabel) {
  link
    .attr("x1", (d) => d.source.x)
    .attr("y1", (d) => d.source.y)
    .attr("x2", (d) => d.target.x)
    .attr("y2", (d) => d.target.y);

  linkLabel
    .attr("x", (d) => (d.source.x + d.target.x) / 2)
    .attr("y", (d) => (d.source.y + d.target.y) / 2);
}

function dragStart(event, d, simulation) {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragging(event, d, simulation) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragEnd(event, d, simulation) {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

export default Graph;
