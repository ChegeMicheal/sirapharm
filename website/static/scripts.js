/* ---menu--- */

const menu = document.querySelector(".menu");
const openMenuBtn = document.querySelector(".open-menu-btn");
const closeMenuBtn = document.querySelector(".close-menu-btn");

[openMenuBtn, closeMenuBtn].forEach((btn) => {
    btn.addEventListener("click", () => {
        menu.classList.toggle("open");
        menu.style.transition = "transform 0.5s ease";
    });
});

menu.addEventListener("transitionend", function() {
    this.removeAttribute("style");
});

menu.querySelectorAll(".dropdown > i").forEach((arrow) => {
    arrow.addEventListener("click", function() {
        this.closest(".dropdown").classList.toggle("active");
    });
});

/* ---offers--- */
const productContainers = [...document.querySelectorAll('.product-container')];
const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
const preBtn = [...document.querySelectorAll('.pre-btn')];

productContainers.forEach((item, i) => {
    const productCardWidth = item.querySelector('.product-card').offsetWidth + 20; // Include margin if needed

    nxtBtn[i].addEventListener('click', () => {
        item.scrollLeft += productCardWidth;
    });

    preBtn[i].addEventListener('click', () => {
        item.scrollLeft -= productCardWidth;
    });

    // Adding scroll behavior for touchscreens
    let isDown = false;
    let startX;
    let scrollLeft;

    item.addEventListener('mousedown', (e) => {
        isDown = true;
        item.classList.add('active');
        startX = e.pageX - item.offsetLeft;
        scrollLeft = item.scrollLeft;
    });

    item.addEventListener('mouseleave', () => {
        isDown = false;
        item.classList.remove('active');
    });

    item.addEventListener('mouseup', () => {
        isDown = false;
        item.classList.remove('active');
    });

    item.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - item.offsetLeft;
        const walk = (x - startX) * 3; // The number 3 can be adjusted for faster/slower scroll
        item.scrollLeft = scrollLeft - walk;
    });

    // Touch events for mobile
    item.addEventListener('touchstart', (e) => {
        isDown = true;
        startX = e.touches[0].pageX - item.offsetLeft;
        scrollLeft = item.scrollLeft;
    });

    item.addEventListener('touchmove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.touches[0].pageX - item.offsetLeft;
        const walk = (x - startX) * 3; // The number 3 can be adjusted for faster/slower scroll
        item.scrollLeft = scrollLeft - walk;
    });

    item.addEventListener('touchend', () => {
        isDown = false;
    });
});

