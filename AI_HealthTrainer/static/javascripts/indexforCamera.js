var totalSet, doneSet, mins, secs, feedback;

function countdown() {
    if (secs > 0) {
        secs--;
    } else if (mins > 0) {
        mins--;
        secs = 59;
    } else {
        clearInterval(interval);
        return;
    }
    document.getElementById("mins").innerText = String(mins);
    document.getElementById("seconds").innerText = String(secs);
}

fetch("") // 서버 주소
    .then(response => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
    })
    .then(data => {
        totalSet = data.totalSet;
        doneSet = data.doneSet;
        mins = data.mins;
        secs = data.secs;
        feedback = data.feedback;

        document.getElementById("set-num").innerText = doneSet + "/" + totalSet;
        document.getElementById("mins").innerText = String(mins);
        document.getElementById("seconds").innerText = String(secs);
        document.getElementById("feedback").innerText = feedback;
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        mins = 10;
        secs = 0;
        const interval = setInterval(countdown, 1000);
    });


document.getElementById("set-num").addEventListener("click", function () {
    const setE = document.getElementById("set-num");
    if (setE) { 
        doneSet++;
        setE.innerText = doneSet + "/" + totalSet;
        if (doneSet == totalSet) window.location.href = "./compeletion.html";
    }
}); // 수행한 세트 수 변경
