document.addEventListener("DOMContentLoaded", () => getDatenSchüler());
const notenListe = document.getElementById("noten");
const anwesenheitListe = document.getElementById("anwesenheiten");
const messageEl = document.querySelector(".messageEl");
const tempMsg = document.querySelectorAll(".tempMsg");

async function getDatenSchüler(){

    const options = {method: 'POST', headers: {"Content-Type": "application/json"}};

    try{
        response = await fetch("/noten_anwesenheit_einsehen", options);
        const result = await response.json();
        const responseMessage = JSON.stringify(result.message);

        if (!response.ok){

            updateMessageBlock(responseMessage, "#FC4343", "white");

        } else if (response.ok) {
            
            tempMsg.forEach(msg => {
                msg.style.display = "none"
            });

            noten = result.noten;
            anwesenheit = result.anwesenheit;

            for (const [fach, note] of Object.entries(noten)){
                console.log("values of fach and notte are: ", fach, note);
                const li = document.createElement("li");
                li.innerHTML = `${fach}: ${note}`;
                notenListe.appendChild(li);
            }

            maximale_anzahl_präsenz = [15, 14, 7, 8, 13, 8, 7, 13, 10];
            let i = 0;

            for (const [fach, frequenz] of Object.entries(anwesenheit)){
                const li = document.createElement("li");
                li.innerHTML = `${fach}: ${frequenz}/${maximale_anzahl_präsenz[i]}`;
                i++;
                anwesenheitListe.appendChild(li);
            }
        }
    } catch(error){
        updateMessageBlock(`An error occurred: ${error}`, "#FC4343", "white");
        console.log("Try block error occurred: ", error);
    }
}

function updateMessageBlock(messageText, backgroundColor, fontColor){

    messageEl.innerHTML = messageText;
    messageEl.style.backgroundColor = backgroundColor;
    messageEl.style.color = fontColor;
    messageEl.style.display = "block";
}