function getDrawing(
    floorLengthValue,
    floorHeightFromLevelRailHeadsTitleValue,
    heightCenterGravityFromLevelRailHeadsTitleValue,
    platformBaseValue,
    platformWidthValue,
    result,
) {
    const {
        cargo,
        longitudinal_displacement_in_car,
        longitudinal_displacement_with_car,
        general_height_center_gravity,
    } = result;

    const width = 800;
    const unit = width / floorLengthValue;
    const maxHeight = Math.max(...cargo.map(v => v.height));
    const height = (floorHeightFromLevelRailHeadsTitleValue + maxHeight) * unit * 1.5;
    const maxWidth = Math.max(...cargo.map(v => v.width));
    const height2 = Math.max(platformWidthValue, maxWidth) * unit * 1.5;

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

    const wheelMargin = unit * (floorLengthValue - platformBaseValue) / 2;
    const radius = (heightCenterGravityFromLevelRailHeadsTitleValue / 2 - 50) * unit;

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
            0, height - floorHeightFromLevelRailHeadsTitleValue*unit,
            0, height - radius * 2,
            unit*floorLengthValue, height - radius * 2,
            unit*floorLengthValue, height - floorHeightFromLevelRailHeadsTitleValue*unit,
            0, height - floorHeightFromLevelRailHeadsTitleValue*unit,
        ]);

    svg.append("circle") // центр тяжести платформы
        .attr("fill", "orange")
        .attr("cx", floorLengthValue / 2 * unit)
        .attr("cy", height - heightCenterGravityFromLevelRailHeadsTitleValue * unit)
        .attr('r', 5);

    svg.append("circle") // центр тяжести груза
        .attr("fill", "red")
        .attr("cx", (floorLengthValue / 2 - longitudinal_displacement_in_car) * unit)
        .attr("cy", height - general_height_center_gravity * unit)
        .attr('r', 5);
    svg.append("circle") //  центр тяжести груза с вагоном
        .attr("fill", "red")
        .attr("cx", (floorLengthValue / 2 - longitudinal_displacement_with_car) * unit)
        .attr("cy", height - general_height_center_gravity * unit)
        .attr('r', 5);


    for (item of cargo) {
        svg.append("rect") // грузы
            .attr("stroke", "blue")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr('x', (item.delta - item.length/2)*unit)
            .attr('y', height - (floorHeightFromLevelRailHeadsTitleValue + 50 + item.height) * unit)
            .attr('width', item.length*unit)
            .attr('height', item.height*unit);

        svg.append("circle") // центры тяжести грузов
            .attr("fill", "orange")
            .attr("cx", item.delta*unit)
            .attr("cy", height - (floorHeightFromLevelRailHeadsTitleValue + 50 + item.height / 2) * unit)
            .attr("r", 3);

        svg.append("text") // длина
            .attr("color", "gray")
            .attr("text-anchor", "middle")
            .attr("dy", '-0.2em')
            .attr("x", item.delta*unit)
            .attr("y", height - (floorHeightFromLevelRailHeadsTitleValue + 50 + item.height) * unit)
            .text(item.length);

        svg.append("text") // высота
            .attr("color", "gray")
            .attr("alignment-baseline", "middle")
            .attr("text-anchor", "middle")
            .attr("writing-mode", "tb")
            .attr("dx", '0.4em')
            .attr("x", (item.delta - item.length/2)*unit)
            .attr("y", height - (floorHeightFromLevelRailHeadsTitleValue + 50 + item.height / 2) * unit)
            .text(item.height);
    }


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
        .attr('y', (height2 - platformWidthValue*unit) * 0.5)
        .attr('width', floorLengthValue*unit)
        .attr('height', platformWidthValue*unit);

    svg2.append("circle") // центр тяжести платформы
        .attr("fill", "orange")
        .attr("cx", width / 2)
        .attr("cy", height2 / 2)
        .attr('r', 5);

    svg2.append("circle") // центр тяжести груза
        .attr("fill", "red")
        .attr("cx", width / 2 - longitudinal_displacement_in_car * unit)
        .attr("cy", height2 / 2)
        .attr('r', 5);
    svg2.append("circle") // центр тяжести груза с вагоном
        .attr("fill", "red")
        .attr("cx", width / 2 - longitudinal_displacement_with_car * unit)
        .attr("cy", height2 / 2)
        .attr('r', 5);


    for (item of cargo) {
        svg2.append("rect") // грузы
            .attr("stroke", "blue")
            .attr("fill", "none")
            .attr("stroke-width", "2")
            .attr('x', (item.delta - item.length/2)*unit)
            .attr('y', (height2 - item.width*unit) / 2)
            .attr('width', item.length*unit)
            .attr('height', item.width*unit);

        svg2.append("circle") // центры тяжести грузов
            .attr("fill", "orange")
            .attr("cx", item.delta*unit)
            .attr("cy", height2 / 2)
            .attr("r", 3);

        svg2.append("text") // длина
            .attr("color", "gray")
            .attr("text-anchor", "middle")
            .attr("dy", '-0.2em')
            .attr("x", item.delta*unit)
            .attr("y", (height2 - item.width*unit) / 2)
            .text(item.length);

        svg2.append("text") // ширина
            .attr("color", "gray")
            .attr("alignment-baseline", "middle")
            .attr("text-anchor", "middle")
            .attr("writing-mode", "tb")
            .attr("dx", '0.4em')
            .attr("x", (item.delta - item.length/2)*unit)
            .attr("y", height2 / 2)
            .text(item.width);
    }

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
            (height2 - platformWidthValue*unit) / 2, height - floorHeightFromLevelRailHeadsTitleValue*unit,
            (height2 - platformWidthValue*unit) / 2, height - radius * 2,
            (height2 + platformWidthValue*unit) / 2, height - radius * 2,
            (height2 + platformWidthValue*unit) / 2, height - floorHeightFromLevelRailHeadsTitleValue*unit,
            (height2 - platformWidthValue*unit) / 2, height - floorHeightFromLevelRailHeadsTitleValue*unit,
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
            .attr('y', height - (floorHeightFromLevelRailHeadsTitleValue + item.height + 50)*unit)
            .attr('width', item.width*unit)
            .attr('height', item.height*unit);
    }

    svg3.append("text") // ширина
        .attr("color", "gray")
        .attr("text-anchor", "middle")
        .attr("font-weight", "bold")
        .attr("dy", '-0.2em')
        .attr("x", height2/2)
        .attr("y", height - (floorHeightFromLevelRailHeadsTitleValue + maxHeight + 50)*unit)
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


    const {outerHTML} = svgWrapper.node()
    drawing.innerHTML = outerHTML;
    drawing.href = URL.createObjectURL(new Blob(
        [outerHTML],
        {type: "image/svg+xml;charset=utf-8"}
    ));
}
