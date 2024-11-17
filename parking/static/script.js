// || Live camera polling.
let camera = document.querySelector("#camera");
setInterval((_) => {
  if (!camera.complete) {
    return;
  }

  camera.src = camera.dataset.src + "?t=" + new Date().getTime();
}, 512);

let mainContainer = document.querySelector("main");
let socket = io();
socket.on("connect", (_) => {
  socket.emit("connected", navigator.userAgent);
});
socket.on("plates", (plates) => {
  console.log("Plates updated.");
  mainContainer.innerHTML = "";

  for (plate of JSON.parse(plates)) {
    mainContainer.innerHTML += generateCard(plate, "12:45", "$5000");
  }
});

function generateCard(plate, time, money) {
  return `
    <div class="Card">
      <h3>${plate}</h3>
      <span class="time">${time}</span>
      <span class="money">${money}</span>
    </div>
    `;
}

let btnIn = document.querySelector("#btn-in");
let btnOut = document.querySelector("#btn-out");

btnIn.addEventListener("click", (_) => {
  fetch("/plate");
});
