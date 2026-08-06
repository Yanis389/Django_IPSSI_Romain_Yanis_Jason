function buildRadarSvg(data) {
    const svgNS = "http://www.w3.org/2000/svg";
    const size = 480;
    const center = size / 2;
    const radius = 90;
    const n = data.length;
    const maxCount = Math.max(...data.map((d) => d.count));

    const svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", `0 0 ${size} ${size}`);
    svg.setAttribute("width", size);
    svg.setAttribute("height", size);

    const points = [];

    data.forEach((d, i) => {
        const angle = (Math.PI * 2 * i) / n - Math.PI / 2;
        const axisX = center + Math.cos(angle) * radius;
        const axisY = center + Math.sin(angle) * radius;

        const axis = document.createElementNS(svgNS, "line");
        axis.setAttribute("x1", center);
        axis.setAttribute("y1", center);
        axis.setAttribute("x2", axisX);
        axis.setAttribute("y2", axisY);
        axis.setAttribute("stroke", "#2a2a3a");
        svg.appendChild(axis);

        const labelX = center + Math.cos(angle) * (radius + 30);
        const labelY = center + Math.sin(angle) * (radius + 30);
        const cosAngle = Math.cos(angle);
        const anchor = cosAngle > 0.2 ? "start" : cosAngle < -0.2 ? "end" : "middle";
        const label = document.createElementNS(svgNS, "text");
        label.setAttribute("x", labelX);
        label.setAttribute("y", labelY);
        label.setAttribute("text-anchor", anchor);
        label.setAttribute("font-size", "11");
        label.setAttribute("fill", "#b0b0c0");
        label.textContent = d.genre;
        svg.appendChild(label);

        const value = maxCount ? d.count / maxCount : 0;
        const px = center + Math.cos(angle) * radius * value;
        const py = center + Math.sin(angle) * radius * value;
        points.push(`${px},${py}`);
    });

    const polygon = document.createElementNS(svgNS, "polygon");
    polygon.setAttribute("points", points.join(" "));
    polygon.setAttribute("fill", "rgba(108, 92, 231, 0.35)");
    polygon.setAttribute("stroke", "#6c5ce7");
    polygon.setAttribute("stroke-width", "2");
    svg.appendChild(polygon);

    return svg;
}

function loadRadar() {
    const section = document.getElementById("radar-section");
    const container = document.getElementById("genre-radar");
    if (!section || !container) return;

    fetch("/api/profile/genres/")
        .then((r) => (r.ok ? r.json() : []))
        .then((data) => {
            if (data.length < 3) return;
            container.innerHTML = "";
            container.appendChild(buildRadarSvg(data));
            section.hidden = false;
        })
        .catch(() => {});
}

loadRadar();
