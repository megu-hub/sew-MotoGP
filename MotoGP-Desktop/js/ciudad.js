
"use strict";

class Ciudad {
    #nombre;
    #pais;
    #gentilicio;
    #poblacion;
    #latitud;
    #longitud;

    constructor(nombre, pais, gentilicio) {
        this.#nombre = nombre;
        this.#pais = pais;
        this.#gentilicio = gentilicio;
    }

    rellenarDatos(poblacion, latitud, longitud) {
        this.#poblacion = poblacion;
        this.#latitud = latitud;
        this.#longitud = longitud;
    }

    getNombre() {
        return `Ciudad: ${this.#nombre}`;
    }

    getPais() {
        return `País: ${this.#pais}`;
    }

    getInfoSecundaria() {
        return `
            <li>Gentilicio: ${this.#gentilicio}</li>
            <li>Población: ${this.#poblacion}</li>
        `;
    }

    escribeCoordenadas() {
        const parrafo = document.createElement("p");
        parrafo.textContent = `Coordenadas: (${this.#latitud}, ${this.#longitud})`;
        document.body.appendChild(parrafo);
    }

    getMeteorologiaCarrera() {
        const url = "https://archive-api.open-meteo.com/v1/archive";
        const fecha = "2025-03-25";
        const hora = "16:00";
        $.getJSON("https://archive-api.open-meteo.com/v1/archive", {
            latitude: this.#latitud,
            longitude: this.#longitud,
            start_date: fecha,
            end_date: fecha,
            hourly: "temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,windspeed_10m,winddirection_10m",
            daily: "sunrise,sunset",
            timezone: "America/Argentina/Buenos_Aires"
        }).done(data => {
            
            if (!data || !data.hourly || !data.hourly.time) {
                this.meteorologia = null;
                this.mostrarMeteorologiaCarrera();
                return;
            }
            const target = `${fecha}T${hora}`;
            const index = data.hourly.time.indexOf(target);
            this.meteorologia = (index === -1) ? null : {
                hora: hora,
                temperatura: data.hourly.temperature_2m[index],
                sensacion: data.hourly.apparent_temperature[index],
                lluvia: data.hourly.precipitation[index],
                humedad: data.hourly.relative_humidity_2m[index],
                vientoVelocidad: data.hourly.windspeed_10m[index],
                vientoDireccion: data.hourly.winddirection_10m[index],
                salidaSol: data.daily.sunrise[0].slice(-5),
                puestaSol: data.daily.sunset[0].slice(-5)
            };
            this.mostrarMeteorologiaCarrera();
        }).fail(() => {
            this.meteorologia = null;
            this.mostrarMeteorologiaCarrera();
        });
    }

    mostrarMeteorologiaCarrera() {
        if (!this.meteorologia) {
            document.body.insertAdjacentHTML("beforeend", `<p>No hay datos meteorológicos disponibles para la hora de la carrera.</p>`);
            return;
        }
        const m = this.meteorologia;
        const html = `
            <h4>Meteorología en la hora de la carrera</h4>
            <ul>
                <li>Hora: ${m.hora}</li>
                <li>Temperatura: ${m.temperatura} °C</li>
                <li>Sensación térmica: ${m.sensacion} °C</li>
                <li>Lluvia: ${m.lluvia} mm</li>
                <li>Humedad: ${m.humedad} %</li>
                <li>Viento: ${m.vientoVelocidad} km/h</li>
                <li>Dirección del viento: ${m.vientoDireccion}°</li>
                <li>Salida del sol: ${m.salidaSol}</li>
                <li>Puesta del sol: ${m.puestaSol}</li>
            </ul>
        `;  

        document.body.insertAdjacentHTML("beforeend", html);
    }

    getMeteorologiaEntrenos() {
        const url = "https://archive-api.open-meteo.com/v1/archive";
        $.getJSON(url, {
            latitude: this.#latitud,
            longitude: this.#longitud,
            start_date: "2025-03-14",
            end_date: "2025-03-16",
            hourly: "temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,windspeed_10m",
            timezone: "America/Argentina/Buenos_Aires"
        }).done(data => {
            this.procesarJSONEntrenos(data);
            this.calcularMediasEntrenos();
            this.mostrarMediasEntrenos();
        }).fail(() => {
            this.entrenos = [];
            this.mediasEntrenos = [];
            document.body.insertAdjacentHTML("beforeend", `<p>No se pudieron obtener los datos de entrenos.</p>`);
        });
    }

    procesarJSONEntrenos(jsonData) {
        this.entrenos = [];
        if (!jsonData || !jsonData.hourly || !jsonData.hourly.time) return;
        const horas = jsonData.hourly.time;
        const porFecha = new Map();
        for (let i = 0; i < horas.length; i++) {
            const fechaActual = horas[i].split("T")[0];
            if (!porFecha.has(fechaActual)) porFecha.set(fechaActual, []);
            porFecha.get(fechaActual).push({
                hora: horas[i],
                temperatura: jsonData.hourly.temperature_2m[i],
                sensacion: jsonData.hourly.apparent_temperature[i],
                lluvia: jsonData.hourly.precipitation[i],
                humedad: jsonData.hourly.relative_humidity_2m[i],
                vientoVelocidad: jsonData.hourly.windspeed_10m[i]
            });
        }
        for (const [fecha, horasDia] of porFecha.entries()) {
            this.entrenos.push({ fecha, horas: horasDia });
        }
        this.entrenos.sort((a, b) => a.fecha.localeCompare(b.fecha));
    }

    calcularMediasEntrenos() {
        if (!this.entrenos || this.entrenos.length === 0) {
            this.mediasEntrenos = [];
            return;
        }
        this.mediasEntrenos = this.entrenos.map(dia => {
            const n = dia.horas.length;
            if (n === 0) return null;
            const suma = arr => arr.reduce((a, b) => a + b, 0);
            const temp = suma(dia.horas.map(h => h.temperatura)) / n;
            const sens = suma(dia.horas.map(h => h.sensacion)) / n;
            const lluvia = suma(dia.horas.map(h => h.lluvia)) / n;
            const humedad = suma(dia.horas.map(h => h.humedad)) / n;
            const viento = suma(dia.horas.map(h => h.vientoVelocidad)) / n;
            return {
                fecha: dia.fecha,
                temperatura: temp.toFixed(2),
                sensacion: sens.toFixed(2),
                lluvia: lluvia.toFixed(2),
                humedad: humedad.toFixed(2),
                vientoVelocidad: viento.toFixed(2)
            };
        }).filter(d => d !== null);
    }

    mostrarMediasEntrenos() {
        if (!this.mediasEntrenos || this.mediasEntrenos.length === 0) return;
        const contenedor = document.createElement("div");
        this.mediasEntrenos.forEach(dia => {
            const titulo = document.createElement("h4");
            titulo.textContent = `Media del día de entreno ${dia.fecha}`;
            contenedor.appendChild(titulo);
            const ul = document.createElement("ul");
            const liTemp = document.createElement("li");
            liTemp.textContent = `Temperatura: ${dia.temperatura} °C`;
            ul.appendChild(liTemp);
            const liSens = document.createElement("li");
            liSens.textContent = `Sensación térmica: ${dia.sensacion} °C`;
            ul.appendChild(liSens);
            const liLluvia = document.createElement("li");
            liLluvia.textContent = `Lluvia: ${dia.lluvia} mm`;
            ul.appendChild(liLluvia);
            const liHumedad = document.createElement("li");
            liHumedad.textContent = `Humedad: ${dia.humedad} %`;
            ul.appendChild(liHumedad);
            const liViento = document.createElement("li");
            liViento.textContent = `Viento: ${dia.vientoVelocidad} km/h`;
            ul.appendChild(liViento);
            contenedor.appendChild(ul);
        });
        document.body.appendChild(contenedor);
    }
}
