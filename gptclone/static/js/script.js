    const form = document.getElementById("prompt-form");
    const chatBox = document.getElementById("chat-box");
    const template = document.getElementById("message-template");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const input = document.getElementById("prompt");
        const message = input.value.trim();
        if (!message) return;

        addMessageToChat(message, "user");
        input.value = "";

        // Simuler la réponse GPT (tu remplaces ça avec ton backend Django)
        setTimeout(() => {
            addMessageToChat("Rps de chatgpt...", "bot");
        }, 100);
    });

    function addMessageToChat(text, role = "user") {
        const clone = template.cloneNode(true);
        clone.classList.remove("hidden");
        clone.querySelector(".message-text").innerText = text;

        if (role === "user") {
            clone.classList.add("bg-blue-100", "self-end");
        } else {
            clone.classList.add("bg-green-100", "self-start");
        }

        chatBox.appendChild(clone);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Option de fichier
    const fileInput = document.getElementById("file-upload");
    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (file) {
            addMessageToChat(`📎 Fichier ajouté : ${file.name}`, "user");
            // Tu peux gérer l'envoi de fichier vers Django ici
        }
    });