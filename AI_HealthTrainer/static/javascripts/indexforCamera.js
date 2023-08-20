var totalSet, doneSet, mins, secs;

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

        document.getElementById("set-num").innerText = doneSet + "/" + totalSet;
        document.getElementById("mins").innerText = mins;
        document.getElementById("seconds").innerText = secs;
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
    });

document.getElementById("min-unit").addEventListener("click", function () {
    const minE = document.getElementById("mins");
    const secE = document.getElementById("seconds");
    if (minE && secE) { 
        mins = parseInt(minE.innerText);
        secs = parseInt(secE.innerText);

        if (secs > 0) secs--;
        else {
            mins--;
            secs = 59;
            minE.innerText = mins;
        }
        secE.innerText = secs;
    }
}); // 시간 변경

document.getElementById("set-num").addEventListener("click", function () {
    const setE = document.getElementById("set-num");
    if (setE) { 
        doneSet++;
        setE.innerText = doneSet + "/" + totalSet;
        if (doneSet == totalSet) window.location.href = "./compeletion.html";
    }
}); // 수행한 세트 수 변경
