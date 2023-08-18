var userName , goalTime, doneRatio, doneTime, usedCalories;

fetch("") // 서버 주소
    .then(response => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then(data => {
        userName = data.userName;
        goalTime = data.goalTime;
        doneTime = data.doneTime;
        usedCalories = data.usedCalories;
        doneRatio = doneTime / goalTime * 100;

        document.getElementsByClassName("username-text")[0].innerText = userName;
        document.getElementById("goal-time-num").innerText = "(" + goalTime;
        document.getElementById("percentage-num").innerText = doneRatio;
        document.getElementById("calories-num").innerText = usedCalories;
        document.getElementById("total-hour-num").innerText = doneTime;
    })
    .catch(error => {   
        console.error("There was a problem with the fetch operation:", error);
    });


const progressBar = document.getElementsByClassName("progress-bar")[0]; 
const progressBg = document.getElementsByClassName("progress-bg")[0];
const maxWidth = parseFloat(window.getComputedStyle(progressBg).width); // 'progress-bg'의 최대 넓이를 가져옵니다.
progressBar.style.width = (maxWidth * doneRatio / 100) + "px"; // 'progress-bar'의 넓이를 설정합니다.  

document.getElementsByClassName("start-button")[0].addEventListener("click", function() {
    window.location.href = "././index.html";
});

document.getElementsByClassName("set-goal-indicator")[0].addEventListener("click", function() {
    window.location.href = "././index.html";
});

document.getElementsByClassName("set-goal-text")[0].addEventListener("click", function() {
    window.location.href = "././index.html";
});
