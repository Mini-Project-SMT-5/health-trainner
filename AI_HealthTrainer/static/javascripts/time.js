const plus = document.querySelector(".plus"),
minus = document.querySelector(".minus"),
num = document.querySelector(".num");

let a = 0;

plus.addEventListener("click", ()=>{
    a++
    a = (a < 10 ) ? "0" + a : a;
    num.innerText = a;
});

minus.addEventListener("click", ()=>{
    if(a>0){
        a--;
        a = (a < 10 ) ? "0" + a : a;
        num.innerText = a;
    }
});

const plus2 = document.querySelector(".plus2"),
minus2 = document.querySelector(".minus2"),
num2 = document.querySelector(".num2");

let b = 0;

plus2.addEventListener("click", ()=>{
    b++
    b = (b < 10 ) ? "0" + b : b;
    num2.innerText = b;
});

minus2.addEventListener("click", ()=>{
    if(b>0){
        b--;
        b = (b < 10 ) ? "0" + b : b;
        num2.innerText = b;
    }
});


const plus3 = document.querySelector(".plus3"),
minus3 = document.querySelector(".minus3"),
num3 = document.querySelector(".num3");

let c = 0;

plus3.addEventListener("click", ()=>{
    c++
    c = (c < 10 ) ? "0" + c : c;
    num3.innerText = c;
});

minus3.addEventListener("click", ()=>{
    if(c>0){
        c--;
        c = (c < 10 ) ? "0" + c : c;
        num3.innerText = c;
    }
});