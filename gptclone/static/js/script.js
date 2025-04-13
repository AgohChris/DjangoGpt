function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    
    
    
    
    const form = document.getElementById("prompt-form");
    const chatBox = document.getElementById("chat-box");
    const template = document.getElementById("message-template");

    // form.addEventListener("submit", async (e) => {
    //     e.preventDefault();
    //     const input = document.getElementById("prompt");
    //     const message = input.value.trim();
    //     if (!message) return;

    //     addMessageToChat(message, "user");
    //     input.value = "";

    //     // Simuler la réponse GPT (tu remplaces ça avec ton backend Django)
    //     setTimeout(() => {
    //         addMessageToChat("Rps de chatgpt...", "bot");
    //     }, 1000);
        
    // });



    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const input = document.getElementById("prompt");
        const message = input.value.trim();
        if (!message) return;
    
        addMessageToChat(message, "user");
        input.value = "";
    

        try {
            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"), // CSRF Token utile avec Django
                },
                body: JSON.stringify({ message: message }),
            });
    
            const data = await response.json();
            if (data.response) {
                setTimeout( () =>{
                    addMessageToChat(data.response, "bot");
                },1000)

            } else {
                addMessageToChat("Erreur lors de la réponse du bot.", "bot");
            }
        } catch (err) {
            console.error(err);
           setTimeout(() =>{
            addMessageToChat("Erreur côté client", "bot");
           }, 1000)
        }
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


    