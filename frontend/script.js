// frontend/script.js
const API_BASE = "http://localhost:5000";

const resultsEl = document.getElementById("results");
const processTextBtn = document.getElementById("processTextBtn");
const textInput = document.getElementById("textInput");

const audioFileEl = document.getElementById("audioFile");
const processAudioBtn = document.getElementById("processAudioBtn");

function renderResults(data) {
  resultsEl.innerHTML = "";

  const metaDiv = document.createElement("div");
  metaDiv.className = "result-block";
  metaDiv.innerHTML = `
    <h3>Meta</h3>
    <div class="meta">${JSON.stringify(data.meta || {}, null, 2)}</div>
  `;
  resultsEl.appendChild(metaDiv);

  const transcriptDiv = document.createElement("div");
  transcriptDiv.className = "result-block";
  transcriptDiv.innerHTML = `
    <h3>Transcript</h3>
    <div>${escapeHtml(data.transcript || "")}</div>
  `;
  resultsEl.appendChild(transcriptDiv);

  const summaryDiv = document.createElement("div");
  summaryDiv.className = "result-block";
  summaryDiv.innerHTML = `
    <h3>Summary</h3>
    <div>${escapeHtml(data.summary || "")}</div>
  `;
  resultsEl.appendChild(summaryDiv);

  const tasksDiv = document.createElement("div");
  tasksDiv.className = "result-block";
  tasksDiv.innerHTML = `<h3>Tasks</h3>`;
  const tasks = data.tasks || [];
  if (tasks.length === 0) {
    tasksDiv.innerHTML += `<div class="meta">No tasks detected.</div>`;
  } else {
    tasks.forEach(t => {
      const item = document.createElement("div");
      item.className = "item";
      item.innerHTML = `
        <strong>Title:</strong> ${escapeHtml(t.title || "")}<br/>
        <strong>Owner:</strong> ${escapeHtml(t.owner || "-")}<br/>
        <strong>Due:</strong> ${escapeHtml(t.due || "-")}<br/>
        <strong>Source:</strong> ${escapeHtml(t.source || "")}
      `;
      tasksDiv.appendChild(item);
    });
  }
  resultsEl.appendChild(tasksDiv);

  const followDiv = document.createElement("div");
  followDiv.className = "result-block";
  followDiv.innerHTML = `<h3>Follow-ups</h3>`;
  const followups = data.followups || [];
  if (followups.length === 0) {
    followDiv.innerHTML += `<div class="meta">No follow-ups detected.</div>`;
  } else {
    followups.forEach(f => {
      const item = document.createElement("div");
      item.className = "item";
      item.innerHTML = `${escapeHtml(f)}`;
      followDiv.appendChild(item);
    });
  }
  resultsEl.appendChild(followDiv);

  const hlDiv = document.createElement("div");
  hlDiv.className = "result-block";
  hlDiv.innerHTML = `<h3>Highlights</h3>`;
  const highlights = data.highlights || [];
  if (highlights.length === 0) {
    hlDiv.innerHTML += `<div class="meta">No highlights detected.</div>`;
  } else {
    highlights.forEach(h => {
      const item = document.createElement("div");
      item.className = "item";
      item.innerHTML = `${escapeHtml(h)}`;
      hlDiv.appendChild(item);
    });
  }
  resultsEl.appendChild(hlDiv);
}

function escapeHtml(str) {
  return (str || "").toString()
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

processTextBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  if (!text) {
    alert("Please paste some text to process.");
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/process/text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.error(err);
    alert("Error processing text.");
  }
});

processAudioBtn.addEventListener("click", async () => {
  const file = audioFileEl.files[0];
  if (!file) {
    alert("Please select an audio file.");
    return;
  }
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/process/audio`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.error(err);
    alert("Error processing audio.");
  }
});
