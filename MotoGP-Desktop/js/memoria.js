"use strict";
class Memoria {
    #tablero_bloqueado;
    #primera_carta;
    #segunda_carta;
    #cronometro;
    
    constructor() {
        this.#tablero_bloqueado = true;
        this.#primera_carta = null;
        this.#segunda_carta = null;
        this.barajarCartas();
        this.#tablero_bloqueado = false;
        this.#cronometro=new Cronometro();
        this.#cronometro.arrancar();
        this.inicializar();
    }

    inicializar(){
        const cartas = document.querySelectorAll('main > article');
        cartas.forEach(carta => {
            carta.addEventListener('click', () => this.voltearCarta(carta));
        });
    }

    voltearCarta(carta) {
        if (this.#tablero_bloqueado || carta.dataset.estado === "volteada") return;

        carta.dataset.estado = "volteada";

        if (!this.#primera_carta) {
            this.#primera_carta = carta;
        } else if (!this.#segunda_carta) {
            this.#segunda_carta = carta;
            this.comprobarPareja();
        }
    }

    reiniciarAtributos() {
        this.#primera_carta = null;
        this.#segunda_carta = null;
    }

    barajarCartas() {
        let cartas = Array.from(document.querySelectorAll("main > article"));
        for (let i = cartas.length - 1; i >= 0; i--) {
            const random = Math.floor(Math.random() * (i + 1));
            [cartas[i], cartas[random]] = [cartas[random], cartas[i]];
        }
    
        const main = document.querySelector("main");
        cartas.forEach(carta => main.appendChild(carta));
    
        this.#tablero_bloqueado = false; 
    }
    
    deshabilitarCartas() {
        if (this.comprobarJuego()) {
            let cartas = Array.from(document.querySelectorAll("main > article"));
            cartas.forEach(carta => carta.dataset.estado = "revelada");
            this.#tablero_bloqueado = true;
        }
    }

    comprobarJuego() {
        let cartas = Array.from(document.querySelectorAll("main > article"));
        let ganado = cartas.every(carta => carta.dataset.estado === "revelada");
        if(ganado) this.#cronometro.parar();
        return ganado;
    }

    cubrirCartas() {
        this.#tablero_bloqueado = true; 

        setTimeout(() => {
            if (this.#primera_carta) this.#primera_carta.dataset.estado = "";
            if (this.#segunda_carta) this.#segunda_carta.dataset.estado = "";

            this.reiniciarAtributos(); 
            this.#tablero_bloqueado = false;
        }, 1200);
    }
    
    comprobarPareja() {
        if (!this.#primera_carta || !this.#segunda_carta) return;

        this.#tablero_bloqueado = true;

        const primeraSrc = this.#primera_carta.querySelector('img').src;
        const segundaSrc = this.#segunda_carta.querySelector('img').src;

        if (primeraSrc && segundaSrc && primeraSrc === segundaSrc) {
            this.#primera_carta.dataset.estado = "revelada";
            this.#segunda_carta.dataset.estado = "revelada";

            this.reiniciarAtributos();
            this.deshabilitarCartas();
            this.#tablero_bloqueado = false; 
        } else {
            this.cubrirCartas();
        }
    }
}
