class Circuito {
    constructor() {
        this.comprobarApiFile();
    }

    comprobarApiFile() {
        if (window.File && window.FileReader && window.FileList && window.Blob) {
            console.log("Este navegador soporta el API File");
        } else {
            
            console.log("¡¡¡ Este navegador NO soporta el API File y este programa puede no funcionar correctamente !!!");
        }
    }

    leerArchivoHTML(archivo) {
        console.log("Leyendo archivo HTML:", archivo.name);
        const lector = new FileReader();
        
        lector.onload = (evento) => {
            console.log("Archivo HTML cargado correctamente");
            const contenido = evento.target.result;
            console.log("Contenido HTML (primeros 200 chars):", contenido.substring(0, 200));
            this.procesarContenidoHTML(contenido);
        };
        
        lector.onerror = () => {
            console.error("Error al leer el archivo HTML");
        };
        
        lector.readAsText(archivo);
    }

    procesarContenidoHTML(contenido) {
        console.log("Procesando contenido HTML");
        const parser = new DOMParser();
        const doc = parser.parseFromString(contenido, 'text/html');
        
        console.log("Documento parseado:", doc);
        this.extraerYMostrarInformacion(doc);
    }

    extraerYMostrarInformacion(doc) {
        console.log("Extrayendo información del documento");
        let seccion = document.querySelector('#contenedorHTML');
        
        if (!seccion) {
            console.log("Creando contenedor HTML");
            seccion = document.createElement('section');
            seccion.id = 'contenedorHTML';
            seccion.style.border = '2px solid blue';
            seccion.style.padding = '20px';
            seccion.style.margin = '20px 0';
            document.body.appendChild(seccion);
        }
        
        seccion.innerHTML = '';
        console.log("Contenedor limpiado");
        
        const h1 = doc.querySelector('h1');
        if (h1) {
            console.log("H1 encontrado:", h1.textContent);
            const titulo = document.createElement('h2');
            titulo.textContent = h1.textContent;
            seccion.appendChild(titulo);
        }
        
        const secciones = doc.querySelectorAll('section');
        console.log("Secciones encontradas:", secciones.length);
        
        secciones.forEach((seccionOriginal, index) => {
            console.log("Procesando sección", index);
            const nuevaSeccion = document.createElement('article');
            nuevaSeccion.style.marginBottom = '20px';
            
            const encabezados = seccionOriginal.querySelectorAll('h2, h3');
            encabezados.forEach((h) => {
                const nuevoEncabezado = document.createElement(h.tagName.toLowerCase());
                nuevoEncabezado.textContent = h.textContent;
                nuevaSeccion.appendChild(nuevoEncabezado);
            });
            
            const parrafos = seccionOriginal.querySelectorAll('p');
            parrafos.forEach((p) => {
                const nuevoParrafo = document.createElement('p');
                nuevoParrafo.textContent = p.textContent;
                nuevaSeccion.appendChild(nuevoParrafo);
            });
            
            const listas = seccionOriginal.querySelectorAll('ul');
            listas.forEach((ul) => {
                const nuevaLista = document.createElement('ul');
                const items = ul.querySelectorAll('li');
                items.forEach((li) => {
                    const nuevoItem = document.createElement('li');
                    const enlace = li.querySelector('a');
                    if (enlace) {
                        const nuevoEnlace = document.createElement('a');
                        nuevoEnlace.href = enlace.href;
                        nuevoEnlace.textContent = enlace.textContent;
                        nuevoItem.appendChild(document.createTextNode(li.childNodes[0].textContent));
                        nuevoItem.appendChild(nuevoEnlace);
                    } else {
                        nuevoItem.textContent = li.textContent;
                    }
                    nuevaLista.appendChild(nuevoItem);
                });
                nuevaSeccion.appendChild(nuevaLista);
            });
            
            const imagenes = seccionOriginal.querySelectorAll('img');
            imagenes.forEach((img) => {
                const nuevaImagen = document.createElement('img');
                let rutaImagen = img.src;
                
                if (rutaImagen.includes('../multimedia/')) {
                    rutaImagen = rutaImagen.replace('../multimedia/', 'multimedia/');
                } else if (img.getAttribute('src') && img.getAttribute('src').includes('../')) {
                    rutaImagen = img.getAttribute('src').replace('../', '');
                }
                
                nuevaImagen.src = rutaImagen;
                nuevaImagen.alt = img.alt;
                nuevaImagen.style.maxWidth = '100%';
                nuevaImagen.onerror = function() {
                    console.error("Error al cargar imagen:", rutaImagen);
                    this.alt = "Error: No se pudo cargar la imagen " + rutaImagen;
                    this.style.border = "1px solid red";
                    this.style.padding = "10px";
                };
                nuevaSeccion.appendChild(nuevaImagen);
            });
            
            const videos = seccionOriginal.querySelectorAll('video');
            videos.forEach((video) => {
                const nuevoVideo = document.createElement('video');
                nuevoVideo.controls = true;
                nuevoVideo.style.maxWidth = '100%';
                const source = video.querySelector('source');
                if (source) {
                    const nuevaSource = document.createElement('source');
                    let rutaVideo = source.src;
                    
                    if (rutaVideo.includes('../multimedia/')) {
                        rutaVideo = rutaVideo.replace('../multimedia/', 'multimedia/');
                    } else if (source.getAttribute('src') && source.getAttribute('src').includes('../')) {
                        rutaVideo = source.getAttribute('src').replace('../', '');
                    }
                    
                    nuevaSource.src = rutaVideo;
                    nuevaSource.type = source.type;
                    nuevoVideo.appendChild(nuevaSource);
                }
                nuevaSeccion.appendChild(nuevoVideo);
            });
            
            seccion.appendChild(nuevaSeccion);
        });
        
        console.log("Información extraída y mostrada correctamente");
    }

    cargarArchivo() {
        console.log("cargarArchivo invocado");
        const input = document.querySelector('input[type="file"]#inputHTML');
        console.log("Input HTML encontrado:", input);
        console.log("Archivos:", input ? input.files : "no input");
        
        if (input && input.files.length > 0) {
            const archivo = input.files[0];
            console.log("Archivo HTML seleccionado:", archivo.name);
            this.leerArchivoHTML(archivo);
        } else {
            console.error("No se seleccionó ningún archivo HTML");
        }
    }
}

class CargadorSVG {
    constructor() {
        this.comprobarApiFile();
    }

    comprobarApiFile() {
        if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
            document.write("<p>Este navegador NO soporta el API File</p>");
        }
    }

    leerArchivoSVG(archivo) {
        console.log("Leyendo archivo SVG:", archivo.name);
        const lector = new FileReader();
        
        lector.onload = (evento) => {
            console.log("Archivo cargado correctamente");
            const contenido = evento.target.result;
            console.log("Contenido:", contenido.substring(0, 100));
            this.insertarSVG(contenido);
        };
        
        lector.onerror = () => {
            console.error("Error al leer el archivo SVG");
            alert("Error al leer el archivo SVG");
        };
        
        lector.readAsText(archivo);
    }

    insertarSVG(contenido) {
        console.log("Insertando SVG en el documento");
        const parser = new DOMParser();
        const doc = parser.parseFromString(contenido, 'image/svg+xml');
        const svg = doc.querySelector('svg');
        
        console.log("SVG encontrado:", svg);
        
        if (svg) {
            let contenedor = document.querySelector('#contenedorSVG');
            console.log("Contenedor encontrado:", contenedor);
            
            if (!contenedor) {
                console.log("Creando nuevo contenedor");
                contenedor = document.createElement('div');
                contenedor.id = 'contenedorSVG';
                contenedor.style.width = '100%';
                contenedor.style.margin = '20px 0';
                contenedor.style.border = '2px solid red';
                const seccion = document.querySelector('section');
                if (seccion) {
                    seccion.appendChild(contenedor);
                } else {
                    document.body.appendChild(contenedor);
                }
            }
            
            contenedor.innerHTML = '';
            contenedor.style.display = 'block';
            contenedor.style.minHeight = '600px';
            svg.style.width = '100%';
            svg.style.height = 'auto';
            contenedor.appendChild(svg);
            console.log("SVG insertado correctamente");
            console.log("Contenedor después de insertar:", contenedor);
        } else {
            console.error("No se encontró el elemento SVG");
        }
    }

    cargarArchivoSVG() {
        console.log("cargarArchivoSVG invocado");
        const input = document.querySelector('input[type="file"][accept=".svg"]');
        console.log("Input encontrado:", input);
        console.log("Archivos:", input ? input.files : "no input");
        
        if (input && input.files.length > 0) {
            const archivo = input.files[0];
            console.log("Archivo seleccionado:", archivo.name);
            this.leerArchivoSVG(archivo);
        } else {
            console.error("No se seleccionó ningún archivo");
        }
    }
}

const cargadorSVG = new CargadorSVG();
const circuito = new Circuito();

class CargadorKML {
    constructor() {
        this.mapa = null;
        this.coordenadas = [];
    }

    leerArchivoKML(archivo) {
        console.log("Leyendo archivo KML:", archivo.name);
        const lector = new FileReader();
        
        lector.onload = (evento) => {
            console.log("Archivo KML cargado correctamente");
            const contenido = evento.target.result;
            this.procesarKML(contenido);
        };
        
        lector.onerror = () => {
            console.error("Error al leer el archivo KML");
            alert("Error al leer el archivo KML");
        };
        
        lector.readAsText(archivo);
    }

    procesarKML(contenido) {
        console.log("Procesando KML");
        const parser = new DOMParser();
        const doc = parser.parseFromString(contenido, 'text/xml');
        
        const coordinates = doc.querySelector('coordinates');
        if (coordinates) {
            const coordText = coordinates.textContent.trim();
            const puntos = coordText.split('\n').filter(l => l.trim());
            
            this.coordenadas = puntos.map(punto => {
                const [lng, lat] = punto.trim().split(',');
                return [parseFloat(lng), parseFloat(lat)];
            });
            
            console.log("Coordenadas extraídas:", this.coordenadas.length);
            this.inicializarMapa();
        } else {
            console.error("No se encontraron coordenadas en el KML");
        }
    }

    inicializarMapa() {
        if (this.coordenadas.length === 0) {
            console.error("No hay coordenadas para mostrar");
            return;
        }

        let contenedor = document.querySelector('#mapaCircuito');
        if (!contenedor) {
            contenedor = document.createElement('div');
            contenedor.id = 'mapaCircuito';
            contenedor.style.width = '100%';
            contenedor.style.height = '600px';
            contenedor.style.margin = '20px 0';
            document.body.appendChild(contenedor);
        }

        const centro = this.coordenadas[0];
        
        mapboxgl.accessToken = 'pk.eyJ1IjoibWVndXNldyIsImEiOiJjbWlmNmNhNDMwOXhmM2tzOXcxOWR4ejk3In0.pQD9ydhii7vFLSjupm9Hmg';
        
        this.mapa = new mapboxgl.Map({
            container: 'mapaCircuito',
            style: 'mapbox://styles/mapbox/streets-v11',
            center: centro,
            zoom: 14
        });

        this.mapa.on('load', () => {
            this.mapa.addSource('ruta', {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'LineString',
                        'coordinates': this.coordenadas
                    }
                }
            });

            this.mapa.addLayer({
                'id': 'ruta',
                'type': 'line',
                'source': 'ruta',
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': '#FF0000',
                    'line-width': 4
                }
            });

            this.coordenadas.forEach((coord, index) => {
                if (index === 0) {
                    new mapboxgl.Marker({ color: 'green' })
                        .setLngLat(coord)
                        .setPopup(new mapboxgl.Popup().setHTML('<h3>Inicio</h3>'))
                        .addTo(this.mapa);
                } else if (index === this.coordenadas.length - 1) {
                    new mapboxgl.Marker({ color: 'red' })
                        .setLngLat(coord)
                        .setPopup(new mapboxgl.Popup().setHTML('<h3>Fin</h3>'))
                        .addTo(this.mapa);
                }
            });

            const bounds = this.coordenadas.reduce((bounds, coord) => {
                return bounds.extend(coord);
            }, new mapboxgl.LngLatBounds(this.coordenadas[0], this.coordenadas[0]));

            this.mapa.fitBounds(bounds, { padding: 50 });
        });
    }

    cargarArchivoKML() {
        console.log("cargarArchivoKML invocado");
        const input = document.querySelector('input[type="file"]#inputKML');
        console.log("Input KML encontrado:", input);
        
        if (input && input.files.length > 0) {
            const archivo = input.files[0];
            console.log("Archivo KML seleccionado:", archivo.name);
            this.leerArchivoKML(archivo);
        } else {
            console.error("No se seleccionó ningún archivo KML");
        }
    }
}

const cargadorKML = new CargadorKML();