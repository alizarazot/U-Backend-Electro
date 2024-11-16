let camera = document.querySelector("#camera");

setInterval((_) => {
  if (!camera.complete) {
    return;
  }

  camera.src = "http://192.168.0.110/capture?t=" + new Date().getTime();
}, 250);

let button = document.querySelector("#button");
let plate = document.querySelector("#plate");

button.addEventListener("click", async (_) => {
  plate.innerText = "Leyendo...";
  let response = await fetch("/plate");
  plate.innerText = "Placa: " + (await response.text());
});
