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

  for (plate of JSON.parse(plates)) {
    mainContainer.innerHTML += generateCard(plate, "12:45", "$5000");
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
