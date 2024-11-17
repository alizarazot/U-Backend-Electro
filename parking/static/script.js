let camera = document.querySelector("#camera");
setInterval((_) => {
  if (!camera.complete) {
    return;
  }

  camera.src = camera.dataset.src + "?t=" + new Date().getTime();
}, 512);

function generateCard(plate, time, money) {
  return `
    <div class="Card">
      <h3>${plate}</h3>
      <span class="time">${time}</span>
      <span class="money">${money}</span>
    </div>
    `;
}

async function getPlate() {
  return await (await fetch("/plate")).text();
}

let btnIn = document.querySelector("#btn-in");
let btnOut = document.querySelector("#btn-out");
let mainContainer = document.querySelector("main");

btnIn.addEventListener("click", async (_) => {
  mainContainer.innerHTML += generateCard(await getPlate(), "12:15", "$24500");
});
