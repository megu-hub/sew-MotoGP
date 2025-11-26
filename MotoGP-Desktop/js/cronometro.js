"use strict";

class Cronometro {
  #tiempo
  #stop
  #corriendo
  #inicio
  constructor() {
    this.#tiempo = 0;
    this.#stop = true;
    this.#corriendo = null;
    this.#inicio = null;

    this.mostrar();
  }

  inicializar(){
    
		let botones = document.querySelectorAll("button");
		botones[0].addEventListener("click", () => this.arrancar());
		botones[1].addEventListener("click", () => this.parar());
		botones[2].addEventListener("click", () => this.reiniciar());
  }

  ahora() {
    try {
      return Temporal.Now.instant();
    } catch {
      return new Date();
    }
  }

  toMs(x) {
    if (!x) return 0;
    // Temporal.Instant
    if (typeof x.epochMilliseconds === "number") return x.epochMilliseconds;
    // Date
    if (typeof x.getTime === "function") return x.getTime();
    return 0;
  }

  calculaDif(ahora, inicio) {
    return this.toMs(ahora) - this.toMs(inicio);
  }

  arrancar() {
    if (this.#stop) {
      this.#stop = false;
      this.#inicio = this.ahora();

      if (!Number.isFinite(this.#tiempo) || this.#tiempo < 0) this.#tiempo = 0;

      this.#corriendo = window.setInterval(this.actualizar.bind(this), 100);
    }
  }

  parar() {
    if (!this.#stop) {
      this.#stop = true;
      clearInterval(this.#corriendo);
      this.#corriendo = null;

      if (this.#inicio) {
        const ahora = this.ahora();
        const diff = this.calculaDif(ahora, this.#inicio);
        if (Number.isFinite(diff) && diff >= 0) {
          this.#tiempo += diff;
        }
      }

      this.#inicio = null;
      this.mostrar();
    }
  }

  reiniciar() {
    this.#stop = true;
    this.#tiempo = 0;
    this.#inicio = null;

    clearInterval(this.#corriendo);
    this.#corriendo = null;
    this.mostrar();
  }

  actualizar() {
    if (!this.#stop) {
      this.mostrar();
    }
  }

  mostrar() {
    let ms = this.#tiempo;

    if (!this.#stop && this.#inicio) {
      const ahora = this.ahora();
      const diff = this.calculaDif(ahora, this.#inicio);
      if (Number.isFinite(diff) && diff >= 0) {
        ms += diff;
      }
    }

    if (!Number.isFinite(ms) || ms < 0) ms = 0;

    const totalSegundos = Math.floor(ms / 1000);
    const minutos = Math.floor(totalSegundos / 60);
    const segundos = totalSegundos % 60;
    const decimas = Math.floor((ms % 1000) / 100);

    const stringMinutos = String(minutos).padStart(2, "0");
    const stringSegundos = String(segundos).padStart(2, "0");

    const parrafo = document.querySelector("main p");
    if (parrafo) {
      parrafo.textContent = `${stringMinutos}:${stringSegundos}:${decimas}`;
    }
  }

  
}
