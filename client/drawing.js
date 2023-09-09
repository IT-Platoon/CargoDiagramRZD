function getDrawing() {
    const L = 13400;
    const W = 2870;
    const wugr = 1310;
    const vct = 800;
    const dp = 9720;
    const cargo = [
        {'length': 1080, 'width': 1580, 'height': 390, 'weight': 395 / 1000},
        {'length': 3650, 'width': 3320, 'height': 1500, 'weight': 6670 / 1000},
        {'length': 4100, 'width': 1720, 'height': 1150, 'weight': 1865 / 1000},
        {'length': 3870, 'width': 2890, 'height': 1020, 'weight': 4085 / 1000},
    ];

    const width = 800;
    const unit = width / L;
    const maxHeight = Math.max(...cargo.map(v => v.height));
    const height = (wugr + maxHeight) * unit * 1.5;
    const maxWidth = Math.max(...cargo.map(v => v.width));
    const height2 = Math.max(W, maxWidth) * unit * 1.5;

    const svgWrapper = d3.create("svg")
        .attr("width", Math.max(width, height2) + 20)
        .attr("height", 2 * height + height2 + 60)
        .attr("version", 1.1)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .style('background', '#EEEEEE');

    const svg = svgWrapper.append("svg")
        .attr("width", width + 20)
        .attr("height", height + 20)
        .attr("x", 10)
        .attr("y", 0);

    svg.append("circle") // центр тяжести платформы
        .style("stroke", "orange")
        .style("fill", "orange")
        .style("stroke-width", "2")
        .attr("cx", L / 2 * unit)
        .attr("cy", height - vct * unit)
        .attr('r', 5);

    const wheelMargin = unit * (L - dp) / 2;
    const radius = (vct / 2 - 50) * unit;

    [
        wheelMargin + radius * 1.5,
        wheelMargin - radius * 1.5,
        width - wheelMargin + radius * 1.5,
        width - wheelMargin - radius * 1.5,
    ].forEach(x =>
        svg.append("circle") // колёса
            .attr("stroke", "gray")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr("cx", x)
            .attr("cy", height - radius)
            .attr('r', radius)
    );

    svg.append("polyline") // Платформа
        .attr("stroke", "gray")
        .attr("fill", "none")
        .attr("stroke-width", "2")
        .attr("points", [
            0, height - wugr*unit,
            0, height - radius * 2,
            unit*L, height - radius * 2,
            unit*L, height - wugr*unit,
            0, height - wugr*unit,
        ]);


    svg.append("circle") // центр тяжести платформы
        .attr("fill", "orange")
        .attr("cx", L / 2 * unit)
        .attr("cy", height - vct * unit)
        .attr('r', 5);

    const delta = 50;

    let fromStart = 150*unit
    for (item of cargo) {
        svg.append("rect") // грузы
            .attr("stroke", "blue")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr('x', fromStart + delta*unit)
            .attr('y', height - (wugr + 50 + item.height) * unit)
            .attr('width', item.length*unit)
            .attr('height', item.height*unit);

        svg.append("circle") // центры тяжести грузов
            .attr("fill", "orange")
            .attr("cx", fromStart + (delta + item.length/2)*unit)
            .attr("cy", height - (wugr + 50 + item.height / 2) * unit)
            .attr("r", 3);

        svg.append("text") // длина
            .attr("color", "gray")
            .attr("text-anchor", "middle")
            .attr("dy", '-0.2em')
            .attr("x", fromStart + (delta + item.length/2)*unit)
            .attr("y", height - (wugr + 50 + item.height) * unit)
            .text(item.length);

        svg.append("text") // высота
            .attr("color", "gray")
            .attr("alignment-baseline", "middle")
            .attr("text-anchor", "middle")
            .attr("writing-mode", "tb")
            .attr("dx", '0.6em')
            .attr("x", fromStart)
            .attr("y", height - (wugr + 50 + item.height / 2) * unit)
            .text(item.height);

        fromStart += (item.length + delta) * unit;
    }

    svg.append("circle") // общий центр тяжести
        .attr("fill", "red")
        .attr("cx", L / 2 * unit)
        .attr("cy", height - wugr * 1.5 * unit)
        .attr('r', 5);

    const svg2 = svgWrapper.append("svg")
        .attr("width", width + 20)
        .attr("height", height2 + 20)
        .attr("x", 10)
        .attr("y", height + 20);


    svg2.append("rect") // платформа
        .attr("stroke", "gray")
        .attr("fill", "none")
        .attr("stroke-width", "2")
        .attr('x', 0)
        .attr('y', (height2 - W*unit) * 0.5)
        .attr('width', L*unit)
        .attr('height', W*unit);

    svg2.append("circle") // центр тяжести платформы
        .attr("fill", "orange")
        .attr("cx", width / 2)
        .attr("cy", height2 / 2)
        .attr('r', 5);


    fromStart = 150*unit;
    for (item of cargo) {
        svg2.append("rect") // грузы
            .attr("stroke", "blue")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr('x', fromStart + delta*unit)
            .attr('y', (height2 - item.width*unit) / 2)
            .attr('width', item.length*unit)
            .attr('height', item.width*unit);

        svg2.append("circle") // центры тяжести грузов
            .attr("fill", "orange")
            .attr("cx", fromStart + (delta + item.length/2)*unit)
            .attr("cy", height2 / 2)
            .attr("r", 3);

        svg2.append("text") // длина
            .attr("color", "gray")
            .attr("text-anchor", "middle")
            .attr("dy", '-0.2em')
            .attr("x", fromStart + (delta + item.length/2)*unit)
            .attr("y", (height2 - item.width*unit) / 2)
            .text(item.length);

        svg2.append("text") // ширина
            .attr("color", "gray")
            .attr("alignment-baseline", "middle")
            .attr("text-anchor", "middle")
            .attr("writing-mode", "tb")
            .attr("dx", '0.6em')
            .attr("x", fromStart)
            .attr("y", height2 / 2)
            .text(item.width);

        fromStart += (item.length + delta) * unit;
    }

    svg2.append("circle") // общий центр тяжести
        .attr("fill", "red")
        .attr("cx", L / 2 * unit)
        .attr("cy", height2 / 2)
        .attr('r', 5);

    const svg3 = svgWrapper.append("svg")
        .attr("width", height2 + 20)
        .attr("height", height + 20)
        .attr("x", 10)
        .attr("y", height2 + height + 40);

    svg3.append("polyline") // Платформа
        .attr("stroke", "gray")
        .attr("fill", "none")
        .attr("stroke-width", "2")
        .attr("points", [
            (height2 - W*unit) / 2, height - wugr*unit,
            (height2 - W*unit) / 2, height - radius * 2,
            (height2 + W*unit) / 2, height - radius * 2,
            (height2 + W*unit) / 2, height - wugr*unit,
            (height2 - W*unit) / 2, height - wugr*unit,
        ]);

    [
        height2/2 + 50 - 150*unit,
        height2/2 - 50,
    ].forEach(x =>
        svg3.append("rect") // грузы
            .attr("stroke", "gray")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr('x', x)
            .attr('y', height - 2*radius)
            .attr('width', 150*unit)
            .attr('height', 2*radius)
    );

    for (item of cargo) {
        svg3.append("rect") // грузы
            .attr("stroke", "blue")
            .attr("fill", "none")
            .attr("stroke-width", "1")
            .attr("stroke-dasharray", "8")
            .attr('x', (height2 - item.width*unit) / 2)
            .attr('y', height - (wugr + item.height + 50)*unit)
            .attr('width', item.width*unit)
            .attr('height', item.height*unit);
    }

    svg3.append("text") // ширина
        .attr("color", "gray")
        .attr("text-anchor", "middle")
        .attr("font-weight", "bold")
        .attr("dy", '-0.2em')
        .attr("x", height2/2)
        .attr("y", height - (wugr + maxHeight + 50)*unit)
        .text(maxWidth);

    svg3.append("text") // высота
        .attr("color", "gray")
        .attr("alignment-baseline", "middle")
        .attr("text-anchor", "middle")
        .attr("writing-mode", "tb")
        .attr("font-weight", "bold")
        .attr("dx", '-0.8em')
        .attr("x", (height2 - maxWidth*unit)/2)
        .attr("y", height/2)
        .text(maxHeight);


    drawing.append(svgWrapper.node());

// const svgBlob = new Blob(
//     [svgWrapper.node().outerHTML],
//     {type: "image/svg+xml;charset=utf-8"}
// );
// const svgUrl = URL.createObjectURL(svgBlob);
// const downloadLink = document.getElementById("link");
// downloadLink.href = svgUrl;
// downloadLink.download = 'Схема';
}
