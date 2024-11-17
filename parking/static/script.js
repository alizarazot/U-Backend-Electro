// Script principal.

// Selectores.
let imgCamera = document.querySelector("#camera");
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

function generateCard(plate, time, money) {
  return `
    <div class="Card">
      <h3 class="plate">${plate}</h3>
      <span class="time">${time}</span>
      <span class="money">${money}</span>
    </div>
    `;
}
