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

async function login () {

    try {
        const email = document.getElementById("emailInput").value;
        const password = document.getElementById("passwordInput").value;

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

                const token = result.access_token;
                localStorage.setItem("access token", token)
                updateMessageBlock(responseMessage, "green", "white")

                setTimeout(() => {
                    makeRequestWithJWT();
                    }, 1000);
            }
        } catch (error){
            console.log("Inner try block error: ", error);
        }

        } catch (error){
            console.log("Outter try block error occurred: ", error);
            }
};

async function makeRequestWithJWT() {

    const token = localStorage.getItem("access token")

    const options = {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${token}`
        },
    };

    const response = await fetch('/home', options)

    if (response.ok){
        const homepage = await response.text();
        document.documentElement.innerHTML = homepage;
        // update browser url
        window.history.pushState({}, '', '/home');

    } else {
        alert("error")
    }
};  