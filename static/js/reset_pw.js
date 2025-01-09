const passwordField1 = document.getElementById("password1");
const passwordField2 = document.getElementById("password2");
const messageEl = document.querySelector(".messageEl");
const anzeigenBtn = document.querySelector(".anzeigenBtn");
const submitBtn = document.querySelector(".submitBtn");

console.log("messageEl ist: ", messageEl)
console.log("submitBtn is ", submitBtn)
submitBtn.addEventListener("click", () => {
    if (passwordField2.value !== passwordField1.value){
        updateMessageBlock("Passwörter stimmen nicht überein", "#FC4343", "white")
    } else {
        sendData()
    }
})

anzeigenBtn.addEventListener("click", () => toggleShowPassword(passwordField1, passwordField2))

function toggleShowPassword(pw1, pw2){

    console.log("show password func was called")
    if (pw1.type === "password" || pw2.type === "password"){
        pw1.type = "text";
        pw2.type = "text";
    } else {
        pw1.type = "password";
        pw2.type = "password";
    }
}

async function sendData() {

    const options = {method: 'POST', headers: {"Content-Type": "application/json"}, body: JSON.stringify({"password": passwordField1.value})};
            
    try{

        updateMessageBlock("Übersende Daten..", "yellow", "black");
        const response = await fetch("/reset_password", options);
        const result = await response.json()
        const responseMessage = JSON.stringify(result.message)

        if (!response.ok){

            updateMessageBlock(responseMessage, "#FC4343", "white")

        } else if (response.ok) {
                alert(responseMessage);
                window.location.href = result.redirect_url;
         }
    } catch (error){
        console.log("Inner try block error: ", error);
    }
}

function updateMessageBlock(messageText, backgroundColor, fontColor){

    messageEl.innerHTML = messageText;
    messageEl.style.fontFamily = "arial";
    messageEl.style.backgroundColor = backgroundColor;
    messageEl.style.color = fontColor;
    messageEl.style.display = "inline-block";
}