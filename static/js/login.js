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

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    try {
        const email = document.getElementById("emailInput").value;
        const password = document.getElementById("passwordInput").value;

        const data = {
            "email": email,
            "password": password,
            };
        
        try{
            updateMessageBlock("Überprüfe Daten...", "yellow", "black")

            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            let result = await response.json()
            let responseMessage = JSON.stringify(result.message)

            if (!response.ok){

                updateMessageBlock(responseMessage, "#FC4343", "white")

            } else {

                updateMessageBlock(responseMessage, "green", "white")

                setTimeout(() => {
                    window.location.href="/home";
                }, 1500);
            }
        } catch (error){
            console.log("Inner try block error: ", error);
        }

        } catch (error){
            console.log("Outter try block error occurred: ", error);
            }
});