const log = document.getElementById("log");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("chat-send");

function addBubble(text, who) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
  return div;
}

function addEvent(text, kind) {
  const div = document.createElement("div");
  div.className = "event " + kind;
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

async function sendMessage(message) {
  addBubble(message, "user");
  const botBubble = addBubble("", "bot");

  // UI always gets one plain response, no live tool-call updates.
  // (Streaming is still available for curl/Postman at POST /chat/stream.)
  const res = await fetch("http://127.0.0.1:8080/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!res.ok) {
    botBubble.textContent = "Error: " + res.status;
    return;
  }

  const event = await res.json();

  if (event.type === "done") {
    botBubble.textContent = event.full_text;
  } else {
    botBubble.textContent = "Error: " + (event.message || "unknown error");
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  sendBtn.disabled = true;

  try {
    await sendMessage(message);
  } catch (err) {
    addEvent("stream failed: " + err, "error");
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});
