"use strict";

const calcButton = document.getElementById('calc-button');
const cargoAdd = document.getElementById('cargo-add');

let cargoArray = []
const cargoList = document.getElementById('cargo-list');

const resultWrapper = document.getElementById('result');
const resultList = document.getElementById('result-list');

let resultController;

async function sendRequest(body) {
  const response = await fetch(
    '/api/v1/calculate',
    {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  return response.json();
}

calcButton.addEventListener('click', async () => {
  const floorLength = document.getElementById('floor-length');
  const floorWidth = document.getElementById('floor-width');
  const tareWeight = document.getElementById('tare-weight');
  const floorHeightFromLevelRailHeadsTitle = document.getElementById('floor-height-from-level-rail-heads');
  const heightCenterGravityFromLevelRailHeadsTitle = document.getElementById('height-center-gravity-from-level-rail-heads');
  const platformBase = document.getElementById('platform-base');

  const floorLengthValue = Number(floorLength?.value) > 0 ? Number(floorLength?.value) : 0
  const floorWidthValue = Number(floorWidth?.value) > 0 ? Number(floorWidth?.value) : 0
  const tareWeightValue = Number(tareWeight?.value) > 0 ? Number(tareWeight?.value) : 0
  const floorHeightFromLevelRailHeadsTitleValue = Number(floorHeightFromLevelRailHeadsTitle?.value) > 0 ? Number(floorHeightFromLevelRailHeadsTitle?.value) : 0
  const heightCenterGravityFromLevelRailHeadsTitleValue = Number(heightCenterGravityFromLevelRailHeadsTitle?.value) > 0 ? Number(heightCenterGravityFromLevelRailHeadsTitle?.value) : 0
  const platformBaseValue = Number(platformBase?.value) > 0 ? Number(platformBase?.value) : 0

  let values = (
    floorLengthValue &&
    floorWidthValue &&
    tareWeightValue &&
    floorHeightFromLevelRailHeadsTitleValue &&
    heightCenterGravityFromLevelRailHeadsTitleValue &&
    platformBaseValue
  )
  
  if(values && cargoArray.length) {
    const request = {
      floor_length: floorLengthValue,
      floor_width: floorWidthValue,
      tare_weight: tareWeightValue,
      floor_height_from_level_rail_heads: floorHeightFromLevelRailHeadsTitleValue,
      height_center_gravity_from_level_rail_heads: heightCenterGravityFromLevelRailHeadsTitleValue,
      platform_base: platformBaseValue,
      cargo: cargoArray,
    }

    console.log(request)

    resultList.innerHTML = '';

    let result;
    try {
      result = await sendRequest(request);
    } catch (e) {
      console.error(e);
    }

    if (result?.result == undefined || result?.result?.error != undefined) {
      console.error(result)
      return;
    }

    console.log(result)
    floorLength.value = 13400
    floorWidth.value = 2870
    tareWeight.value = 21
    floorHeightFromLevelRailHeadsTitle.value = 1310
    heightCenterGravityFromLevelRailHeadsTitle.value = 800
    platformBase.value = 9720
    cargoArray = []
    while (cargoList.firstChild) {
      cargoList.removeChild(cargoList.firstChild);
    }
  }
});

cargoAdd.addEventListener('click', async () => {
  const cargoLength = document.getElementById('cargo-length');
  const cargoWidth = document.getElementById('cargo-width');
  const cargoHeight = document.getElementById('cargo-height');
  const cargoWeight = document.getElementById('cargo-weight');
  const cargoQuantity = document.getElementById('cargo-quantity');

  const cargoLengthValue = Number(cargoLength?.value) > 0 ? Number(cargoLength?.value) : 0
  const cargoWidthValue = Number(cargoWidth?.value) > 0 ? Number(cargoWidth?.value) : 0
  const cargoHeightValue = Number(cargoHeight?.value) > 0 ? Number(cargoHeight?.value) : 0
  const cargoWeightValue = Number(cargoWeight?.value) > 0 ? Number(cargoWeight?.value) : 0
  const cargoQuantityValue = Number(cargoQuantity?.value) > 0 ? Number(cargoQuantity?.value) : 0

  let values = (
    cargoLengthValue &&
    cargoWidthValue &&
    cargoHeightValue &&
    cargoWeightValue &&
    cargoQuantityValue
  )

  if (values) {
    const obj = {
      length: cargoLengthValue,
      width: cargoWidthValue,
      height: cargoHeightValue,
      weight: cargoWeightValue,
      quantity: cargoQuantityValue,
    }
    cargoArray.push(obj)
    const item = document.createElement("li")
    const info = `Длина ${obj.length} мм; Ширина ${obj.width} мм; Высота ${obj.height} мм; Вес одного ${obj.weight} т; Количество ${obj.quantity} шт;`
    item.appendChild(document.createTextNode(info))
    cargoList.appendChild(item)

    cargoLength.value = 0
    cargoWidth.value = 0
    cargoHeight.value = 0
    cargoWeight.value = 0
    cargoQuantity.value = 0
  }
});
