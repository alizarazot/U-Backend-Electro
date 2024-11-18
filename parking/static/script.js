// Script principal.

// Selectores.
let imgCamera = document.querySelector("#camera");
let spanPlateStatus = document.querySelector("#plate-status");
let mainContainer = document.querySelector("main");

// Configurar WebSockets.
let socket = io();

socket.on("connect", (_) => {
  socket.emit("connected", navigator.userAgent);
});

socket.on("plates", (plates) => {
  mainContainer.innerHTML = "";

  for (let plate of JSON.parse(plates)) {
    let date = new Date(plate.time_in * 1000);
    let meridian = "A.M.";
    let hours = date.getHours();
    if (hours > 12) {
      hours -= 12;
      meridian = "P.M.";
    }
    if (hours < 10) {
      hours = "0" + hours.toString();
    }
    let minutes = date.getMinutes();
    if (minutes < 10) {
      minutes = "0" + minutes.toString();
    }

    mainContainer.innerHTML += generateCard(
      plate.plate,
      `${hours}:${minutes} ${meridian}`,
      `$${plate.price}`,
    );
  }
});

socket.on("live", (b64) => {
  imgCamera.src = "data:image/png;base64," + b64;
});

socket.on("car-in-start", (_) => {
  spanPlateStatus.innerText = "Carro detectado en la entrada, leyendo placa...";
  spanPlateStatus.classList.toggle("hidden", false);
});

socket.on("car-in-end", (plate) => {
  spanPlateStatus.innerText = "Placa añadida: " + plate;
  spanPlateStatus.classList.toggle("hidden", false);
  setTimeout((_) => spanPlateStatus.classList.toggle("hidden", true), 5000);
});

socket.on("car-out-start", (_) => {
  spanPlateStatus.innerText = "Carro detectado en la salida, leyendo placa...";
  spanPlateStatus.classList.toggle("hidden", false);
});

socket.on("car-out-end", (plate) => {
  spanPlateStatus.innerText = "Placa eliminada: " + plate;
  spanPlateStatus.classList.toggle("hidden", false);
  setTimeout((_) => spanPlateStatus.classList.toggle("hidden", true), 5000);
});

function generateCard(plate, time, money) {
  return `
    <div class="Card">
      <h3 class="plate">${plate}</h3>
      <span class="time">${time}</span>
      <span class="money">${money}</span>
    </div>
    `;
}
