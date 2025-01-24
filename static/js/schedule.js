const rows = document.querySelectorAll(".stunden")
const userInfo = document.getElementById("userEmail")

let subjects = ["Englisch", "Kunst", "Religion", "Deutsch", "Mathematik", "Sport", "Musik", "Geschichte", "Sachunterricht"]



rows.forEach((row) => {
        row.innerHTML = generateSchedule()
    });

userInfo.innerHTML += user1.email;

function generateSchedule(){

        const randomSubject = Math.floor(Math.random() * subjects.length);
        return subjects[randomSubject];
}