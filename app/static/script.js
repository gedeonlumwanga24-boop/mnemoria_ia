const API = {
  memory: "/memory/",
  projects: "/projects/",
  notes: "/notes/",
  tasks: "/tasks/",
};

const toast = document.getElementById("toast");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 2200);
}

async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  const text = await response.text();
  const result = text ? JSON.parse(text) : {};

  if (!response.ok) {
    throw new Error(result.detail || "Erreur API");
  }

  return result;
}

function renderList(containerId, items, type) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  if (!items || items.length === 0) {
    container.innerHTML =
      '<div class="entity-item"><p>Aucune donnée.</p></div>';
    return;
  }

  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "entity-item";

    if (type === "memory") {
      card.innerHTML = `
        <h4>${item.title}</h4>
        <p>${item.content}</p>
        <p><strong>Type:</strong> ${item.memory_type}</p>
      `;
    }

    if (type === "project") {
      card.innerHTML = `
        <h4>${item.name}</h4>
        <p>${item.description}</p>
        <p><strong>Status:</strong> ${item.status}</p>
      `;
    }

    if (type === "note") {
      card.innerHTML = `
        <h4>${item.title}</h4>
        <p>${item.content}</p>
        <p><strong>Course:</strong> ${item.course_id ?? "Aucune"}</p>
      `;
    }

    if (type === "task") {
      card.innerHTML = `
        <h4>${item.title}</h4>
        <p>${item.description}</p>
        <p><strong>Status:</strong> ${item.status}</p>
      `;
    }

    container.appendChild(card);
  });
}

async function loadMemories() {
  try {
    const data = await apiRequest(API.memory);
    renderList("memory-list", data, "memory");
    document.getElementById("stat-memories").textContent = data.length;
  } catch (error) {
    showToast(error.message);
  }
}

async function loadProjects() {
  try {
    const data = await apiRequest(API.projects);
    renderList("project-list", data, "project");
    document.getElementById("stat-projects").textContent = data.length;
  } catch (error) {
    showToast(error.message);
  }
}

async function loadNotes() {
  try {
    const data = await apiRequest(API.notes);
    renderList("note-list", data, "note");
    document.getElementById("stat-notes").textContent = data.length;
  } catch (error) {
    showToast(error.message);
  }
}

async function loadTasks() {
  try {
    const data = await apiRequest(API.tasks);
    renderList("task-list", data, "task");
    document.getElementById("stat-tasks").textContent = data.length;
  } catch (error) {
    showToast(error.message);
  }
}

async function refreshAll() {
  await Promise.all([loadMemories(), loadProjects(), loadNotes(), loadTasks()]);
}

document.getElementById("refresh-all").addEventListener("click", refreshAll);

document
  .getElementById("memory-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      title: document.getElementById("memory-title").value,
      content: document.getElementById("memory-content").value,
      memory_type: document.getElementById("memory-type").value,
      source: document.getElementById("memory-source").value || "user",
    };

    try {
      await apiRequest(API.memory, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast("Mémoire ajoutée");
      event.target.reset();
      document.getElementById("memory-source").value = "user";
      await loadMemories();
    } catch (error) {
      showToast(error.message);
    }
  });

document
  .getElementById("project-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = {
      name: document.getElementById("project-name").value,
      description: document.getElementById("project-description").value,
      status: document.getElementById("project-status").value,
    };

    try {
      await apiRequest(API.projects, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast("Projet ajouté");
      event.target.reset();
      await loadProjects();
    } catch (error) {
      showToast(error.message);
    }
  });

document
  .getElementById("note-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const courseIdValue = document.getElementById("note-course-id").value;
    const payload = {
      title: document.getElementById("note-title").value,
      content: document.getElementById("note-content").value,
      course_id: courseIdValue ? Number(courseIdValue) : null,
    };

    try {
      await apiRequest(API.notes, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast("Note ajoutée");
      event.target.reset();
      await loadNotes();
    } catch (error) {
      showToast(error.message);
    }
  });

document
  .getElementById("task-form")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const projectIdValue = document.getElementById("task-project-id").value;
    const payload = {
      title: document.getElementById("task-title").value,
      description: document.getElementById("task-description").value,
      status: document.getElementById("task-status").value,
      project_id: projectIdValue ? Number(projectIdValue) : null,
      due_date: null,
    };

    try {
      await apiRequest(API.tasks, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      showToast("Tâche ajoutée");
      event.target.reset();
      await loadTasks();
    } catch (error) {
      showToast(error.message);
    }
  });

refreshAll();
