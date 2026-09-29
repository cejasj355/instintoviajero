document.addEventListener('DOMContentLoaded', ()=> {
    const cartas = document.querySelectorAll('.trekking_cba_carta');
    cartas.forEach(carta => {
        carta.addEventListener('click', (e) => {
            const boton = carta.querySelector('.card-btn');
            if (!boton) return;
            if (e.target.closest('.card-btn')) return;
            if (e.ctrlKey || e.metaKey || e.button === 1){
                window.open(boton.href, '_blank');
            }else{
                window.location.href = boton.href;
            }
        });
    });
});