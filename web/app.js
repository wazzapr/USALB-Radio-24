const STREAM_URL = ""; // Set this after the radio server is deployed.

const audio = document.querySelector("#audio");
const play = document.querySelector("#play");
const status = document.querySelector("#status");
const dot = document.querySelector("#dot");
const message = document.querySelector("#message");

function setState(text, live = false) {
  status.textContent = text;
  dot.classList.toggle("live", live);
}

play.addEventListener("click", async () => {
  if (!STREAM_URL) {
    setState("Stream not connected");
    message.textContent = "Radio server is not connected yet. Add the live stream URL to web/app.js after deployment.";
    return;
  }

  if (audio.paused) {
    audio.src = STREAM_URL;
    try {
      await audio.play();
      play.textContent = "⏸ Pause";
      setState("Live", true);
      message.textContent = "You are listening to USALB Radio 24.";
    } catch (error) {
      setState("Playback blocked");
      message.textContent = "Press play again or check the stream URL.";
    }
  } else {
    audio.pause();
    play.textContent = "▶ Play USALB Radio 24";
    setState("Paused");
  }
});

audio.addEventListener("playing", () => setState("Live", true));
audio.addEventListener("waiting", () => setState("Buffering…"));
audio.addEventListener("ended", () => setState("Stream ended"));
