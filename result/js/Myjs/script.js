let nav = document.querySelector("#navArea");
let js = document.querySelector("#js-navbar");
let btn = document.querySelector(".toggle-btn");
let a =document.querySelector(".a");
let mask = document.querySelector("#mask");
let menu = document.querySelector("#menu");


btn.onclick = () => {
    nav.classList.toggle("open")
    menu.classList.toggle("open")
    mask.classList.toggle("open")
};

/* btn.onclick = () => {
    menu.classList.toggle("open")
};

btn.onclick = () => {
    mask.classList.toggle("open")
}; */