const stars = document.querySelectorAll('#stars i');
const estrelasInput = document.getElementById('estrelas');

stars.forEach(star => {
    star.addEventListener('click', () => {
        const value = star.getAttribute('data-value');
        estrelasInput.value = value;

        stars.forEach(s => {
            s.classList.remove('text-warning');
            if (s.getAttribute('data-value') <= value) {
                s.classList.add('text-warning');
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {

    var slider = document.getElementById("price-range");
    if (!slider) return;

    var minInput = document.getElementById("preco_min");
    var maxInput = document.getElementById("preco_max");

    var lowerValue = document.getElementById("lower-value");
    var upperValue = document.getElementById("upper-value");

    var min = parseInt(minInput.value) || 0;
    var max = parseInt(maxInput.value) || 10000;

    noUiSlider.create(slider, {
        start: [min, max],
        connect: true,
        step: 50,
        range: {
            min: 0,
            max: 10000
        }
    });

    slider.noUiSlider.on("update", function (values) {
        lowerValue.innerHTML = Math.round(values[0]);
        upperValue.innerHTML = Math.round(values[1]);

        minInput.value = Math.round(values[0]);
        maxInput.value = Math.round(values[1]);
    });

    slider.noUiSlider.on("end", function () {
        document.getElementById("filtros").submit();
    });

});

function setOrdem(valor){
    document.getElementById('ordem_hidden').value = valor;
    document.getElementById('filtros').submit();
}

