const showPasswordBtn = document.querySelector(".loginEyeIcon");
const passwordField = document.getElementById("passwordInput");
const messageEl = document.querySelector(".messageEl");
const submitBtnEl = document.querySelector(".submitBtn");

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

function updateMessageBlock(messageText, backgroundColor, fontColor){

    messageEl.innerHTML = messageText;
    messageEl.style.backgroundColor = backgroundColor;
    messageEl.style.color = fontColor;
    messageEl.style.display = "block";
}

async function login() {

    const password = document.getElementById("passwordInput").value;
    const email = document.getElementById("emailInput").value;

    const data = {
        "email": email,
        "password": password,
        };
    const options = {method: 'POST', headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)};
            
    try{
        updateMessageBlock("Überprüfe Daten...", "yellow", "black")

        const response = await fetch("/login", options);
        const result = await response.json()
        const responseMessage = JSON.stringify(result.message)

        if (!response.ok){

            updateMessageBlock(responseMessage, "#FC4343", "white")

        } else if (response.ok) {
            
            updateMessageBlock(responseMessage, "green", "white")
            window.location.href = result.redirect_url
         }
    } catch (error){
        console.log("Inner try block error: ", error);
    }
};  