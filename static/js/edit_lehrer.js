window.addEventListener("DOMContentLoaded", () => {
    const klassenListe = document.getElementById("klassenListe");
    const editBtn = document.querySelector(".editIcon");
    const lehrerID = document.getElementById("lehrerID").innerHTML;
    editBtn.addEventListener("click", () => {
        editBtn.remove()
        const inputField = document.createElement("input");
        const saveBtn = document.createElement("button");
        saveBtn.innerHTML = "speichern";
        inputField.setAttribute("maxlength", 2)
        klassenListe.appendChild(inputField);
        klassenListe.appendChild(saveBtn);
        saveBtn.addEventListener("click", () => sendData(inputField.value, lehrerID))

    })

    async function sendData(data, user_id) {

        const options = {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)}
        
        const response = await fetch(`/verwalter/edit_lehrer/${user_id}`, options);
        const result = await response.json();
        const responseMessage = JSON.stringify(result.message);

        if (!response.ok) {
            const errorMsg = document.createElement("h1");
            klassenListe.appendChild(errorMsg);
            errorMsg.innerHTML = responseMessage;
            errorMsg.style.backgroundColor = "#FC4343";
            errorMsg.style.color = "white";
            errorMsg.style.fontSize = "20px";

            setTimeout(() => {
                errorMsg.remove()
            }, 5000);
        } else {
            location.reload()
        }
    }
})