
const scene = document.getElementById("bookScene");

if (scene && window.matchMedia("(hover: hover)").matches) {
    scene.addEventListener("mousemove", (event) => {
        const bounds = scene.getBoundingClientRect();

        const x = (event.clientX - bounds.left) / bounds.width;
        const y = (event.clientY - bounds.top) / bounds.height;

        const rotateY = (x - 0.5) * 12;
        const rotateX = (0.5 - y) * 10;

        scene.style.transform =
            `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
    });

    scene.addEventListener("mouseleave", () => {
        scene.style.transform = "";
    });
}
