var totalSet, doneSet, mins, secs, storeMin, storeSec, interval;
var video = document.getElementById('camera-viewer');
var prev_feedback = "";
video.src = "/video_feed";
let synth = speechSynthesis;

//-----------------------------------------------------------------------------------------

function countdown() {
    if (secs > 0) {
        secs--;
    } else if (mins > 0) {
        mins--;
        secs = 59;
    } else {
        clearInterval(interval);
        console.log("end");
        return;
    }
    document.getElementById("mins").innerText = String(mins);
    document.getElementById("seconds").innerText = String(secs);
}

function fetchFirst() {
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
        storeMin = mins;
        storeSec = secs;

        document.getElementById("set-num").innerText = doneSet + "/" + totalSet;
        document.getElementById("mins").innerText = String(mins);
        document.getElementById("seconds").innerText = String(secs);
    })
    .catch(error => {
        console.error("There was a problem with the fetch operation:", error);
        mins = 0; secs = 5;
        storeMin = mins; storeSec = secs;
    });

}

function fetchData() {
    fetch("/get_feedback/")
        .then(response => response.json())
        .then(data => {
            const userInfoElement = document.getElementById("feedback");
            var feedback_text = data.textData
            userInfoElement.innerHTML = `
                 ${feedback_text}<br>
            `;
            
            if (feedback_text != prev_feedback){
                prev_feedback = feedback_text;

                if (feedback_text === "Rest") {
                    console.log(feedback_text);
                    interval = setInterval(countdown, 1000);
                } else if (feedback_text === "Rest time is over, Let's workout") {
                    console.log(feedback_text);
                    clearInterval(interval);
                    mins = storeMin;
                    secs = storeSec;
                    document.getElementById("mins").innerText = String(mins);
                    document.getElementById("seconds").innerText = String(secs);

                    var temp = document.getElementById("set-num");
                    temp.innerText = parseInt(temp.innerText) + 1;
                } else if (feedback_text === "All sets is done, congratulation!") {
                    console.log(feedback_text);
                    reqRedirect();
                }

                return textToSpeech(feedback_text);
            } 

        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

function reqRedirect() {
    fetch('') //redirection
    .then(response => response.json())
    .then(data => {
    if (data.redirectUrl) {
        window.location.href = data.redirectUrl;
    }
  })
    .catch(error => console.error('Error:', error));

}

function textToSpeech(text) {
    console.log("call textToSpeech");
    let utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en'
    synth.speak(utterance);
    
}

//-----------------------------------------------------------------------------------------

fetchFirst(); 
setInterval(fetchData, 300);

