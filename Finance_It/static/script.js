document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    // Validar el formulario antes de enviarlo
    form.addEventListener('submit', (event) => {
        const ingreso = parseFloat(document.getElementById('ingreso').value);
        const esenciales = parseFloat(document.getElementById('esenciales').value);
        const noEsenciales = parseFloat(document.getElementById('no_esenciales').value);

        // Validar que los valores sean positivos y coherentes
        if (ingreso <= 0 || esenciales < 0 || noEsenciales < 0) {
            alert("Por favor, asegúrate de que los valores ingresados sean válidos.");
            event.preventDefault(); // Evita que se envíe el formulario
            return;
        }

        if (esenciales + noEsenciales > ingreso) {
            alert("Los gastos no pueden superar el ingreso mensual.");
            event.preventDefault(); // Evita que se envíe el formulario
        }
    });

    // Agregar un efecto visual cuando se enfoque un campo
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.borderColor = '#007bff';
        });

        input.addEventListener('blur', () => {
            input.style.borderColor = '#ddd';
        });
    });
});
