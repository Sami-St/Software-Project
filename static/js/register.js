const lehrerAnsichtDiv = document.getElementById("lehrerAnsichtDiv");
const dropdownMenu = document.getElementById("fachDropdownMenu");
const fachHinzufügenBtn = document.getElementById("fachHinzufügenBtn");
const listeFächer = document.getElementById("hinzugefügteFächer");
const submitBtnEl = document.querySelector(".submitBtn");
const radioBtns = document.querySelectorAll('input[name="user-type"]');
const showPasswordBtn = document.querySelector(".registerEyeIcon");
const passwordField = document.getElementById("passwordInput");
const messageEl = document.querySelector(".messageEl");
const schülerAnsichtDiv = document.getElementById("schülerAnsichtDiv");

dropdownMenu.addEventListener("change", () => checkSelection(dropdownMenu));
// überprüfe welcher Radio Btn derzeit selected ist.
radioBtns.forEach((btn) => {
    btn.addEventListener("change", () =>{
        if (btn.value === "Lehrer"){
            lehrerAnsichtDiv.style.display = "block";
            schülerAnsichtDiv.style.display = "none";
        } else {
            schülerAnsichtDiv.style.display = "block";
            lehrerAnsichtDiv.style.display = "none";
        }
    })
});

showPasswordBtn.addEventListener("click", () => toggleShowPassword(passwordField, showPasswordBtn))

function toggleShowPassword(targetField, toggleBtn){
    if (targetField.type === "password"){
        targetField.type = "text";
        toggleBtn.setAttribute("src", "/static/icons/eye2.png")
    } else{
        targetField.type = "password";
        toggleBtn.setAttribute("src", "/static/icons/eye1.png")
    }
}

function checkSelection(element){

    if (element === dropdownMenu){
        if (element.value !== "bitte auswählen..."){
            fachHinzufügenBtn.removeAttribute("disabled");
        } else {
            fachHinzufügenBtn.setAttribute("disabled", "");
        }
    };
};

fachHinzufügenBtn.addEventListener("click", updateFächerListe)

let fächerArray = [];

function updateFächerListe() {

    const selectedFach = dropdownMenu.value;
    const options = dropdownMenu.children;
    let fächerStr = "";

    if (fächerArray.length < 3){
        fächerArray.push(selectedFach)

        for (let i = 0; i < fächerArray.length; i++){
            fächerStr += fächerArray[i];
            // Komma nach jedem Element im Array hinzufügen außer dem letzten 
            i !== fächerArray.length - 1 ? fächerStr += ", " : "";
        }

    } else {
        updateMessageBlock("Sie dürfen maximal 3 Fächer auswählen.", "#FC4343", "white");

        // MessageBlock nach 3 sec wieder verstecken
        setTimeout(() => {
            messageEl.style.display = "none";
        }, 3000);
        return;
    }

    listeFächer.innerHTML = "Zugewiesene Fächer: " + fächerStr

    // entferne bereits ausgewählte Options
    for (let optionToRemove of options) {
        
        if (optionToRemove.value === selectedFach){
            optionToRemove.remove()
        }
    }
    checkSelection(dropdownMenu)
}

function updateMessageBlock(messageText, backgroundColor, fontColor){

    messageEl.innerHTML = messageText;
    messageEl.style.backgroundColor = backgroundColor;
    messageEl.style.color = fontColor;
    messageEl.style.display = "block";
}

document.getElementById('registerForm').addEventListener('submit', async function(event){
    event.preventDefault();
    try {
        const username = document.getElementById("usernameInput").value;
        const email = document.getElementById("emailInput").value;
        const password = document.getElementById("passwordInput").value;
        const userType = document.querySelector('input[name="user-type"]:checked').value;
        const schülerKlasse = document.getElementById("assignedClass").value;
        let fächer = listeFächer.innerHTML;
        let fächerArray = [];

        // überprüfe, ob Fächer ausgewählt wurden
        if(fächer.length > 20 && userType !== "Schüler"){

            // den String "fächer" in ein Array umwandeln; entferne unnötiger Text und White Spaces
            fächer = fächer.replace("Zugewiesene Fächer: ", "")
            fächerArray = fächer.split(", ").filter(fach => fach !== "")
        } else {
            fächerArray = null
        }

        const data = {
            "username": username,
            "email": email,
            "password": password,
            "user-type": userType,
            "fächer": fächerArray,
            "klasse": schülerKlasse
            } 

        try {
            updateMessageBlock("Registrierung läuft...", "yellow", "black")

            const response = await fetch("/verwalter/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            let result = await response.json()
            let responseMessage = JSON.stringify(result.message)

            if (!response.ok) {

                updateMessageBlock(responseMessage, "#FC4343", "white")

            } else{
                
                updateMessageBlock(responseMessage, "green", "white")

                setTimeout(() => {
                    window.location.href="/klassen";
                }, 1000);
            }  
            
            } catch (error){
                updateMessageBlock(`An error occurred: ${error}`, "#FC4343", "white")
                console.log("Inner try block error: ", error);
            }     
        } catch (error){
            updateMessageBlock(`An error occurred: ${error}`, "#FC4343", "white")
            console.log("Outter try block error occurred: ", error);
            }
});