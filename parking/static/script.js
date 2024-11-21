// Script principal.

// Selectores.
let imgCamera = document.querySelector("#camera");
let spanPlateStatus = document.querySelector("#plate-status");
let divActivePlates = document.querySelector("#active-plates");
let divInactivePlates = document.querySelector("#inactive-plates");

// Configurar WebSockets.
let socket = io();

socket.on("connect", (_) => {
  socket.emit("connected", navigator.userAgent);
});

socket.on("plates", (plates) => {
  plates = JSON.parse(plates);

  divActivePlates.innerHTML = "";
  for (let plate of plates.active) {
    divActivePlates.innerHTML += generateActiveCard(
      plate.plate,
      formatTime(new Date(plate.time_in * 1000)),
      `$${plate.price}`,
    );
  }

  divInactivePlates.innerHTML = "";
  for (let plate of plates.inactive) {
    divInactivePlates.innerHTML += generateInactiveCard(
      plate.plate,
      formatTime(new Date(plate.time_in * 1000)),
      `$${plate.price}`,
      plate.pdf,
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
  if (plate == undefined) {
    spanPlateStatus.innerText = "Placa no detectada";
  } else {
    spanPlateStatus.innerText = "Placa añadida: " + plate;
  }
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

function generateActiveCard(plate, time, money) {
  return `
    <div class="Card">
      <h3 class="plate">${plate}</h3>
      <span class="time">${time}</span>
      <span class="money">${money}</span>
    </div>
    `;
}

function generateInactiveCard(plate, time, money, pdf) {
  return `
    <div class="Card">
      <h3 class="plate">${plate}</h3>
      <span class="money">${money}</span>
      <a class="pdf" href="pdf/${pdf}" target="_blank"> PDF </a>
    </div>
    `;
}

function formatTime(date) {
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

  return `${hours}:${minutes} ${meridian}`;
}
