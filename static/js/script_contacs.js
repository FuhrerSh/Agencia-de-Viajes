document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll("nav ul li a");
    const sections = document.querySelectorAll(".section");

    // Manejar clics en los enlaces de navegación
    links.forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();
            const targetSectionId = link.getAttribute("data-section");

            // Ocultar todas las secciones y mostrar solo la seleccionada
            sections.forEach(section => {
                if (section.id === targetSectionId) {
                    section.classList.add("active");
                } else {
                    section.classList.remove("active");
                }
            });
        });
    });

    console.log("Navegación lista y funcional.");
});
