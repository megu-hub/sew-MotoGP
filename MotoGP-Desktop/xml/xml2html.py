#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class Html:
    
    def __init__(self, titulo):
        self.html = ET.Element('html', lang='es')
        self.head = ET.SubElement(self.html, 'head')
        self.body = ET.SubElement(self.html, 'body')
        ET.SubElement(self.head, 'meta', charset='UTF-8')
        ET.SubElement(self.head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
        tituloElem = ET.SubElement(self.head, 'title')
        tituloElem.text = titulo
        
    def agregarCSS(self, rutaCSS):
        ET.SubElement(self.head, 'link', rel='stylesheet', href=rutaCSS)
        
    def agregarEncabezado(self, texto, nivel=1):
        h = ET.SubElement(self.body, f'h{nivel}')
        h.text = texto
        
    def agregarParrafo(self, texto):
        p = ET.SubElement(self.body, 'p')
        p.text = texto
        
    def agregarSeccion(self):
        return ET.SubElement(self.body, 'section')
        
    def agregarEncabezadoEn(self, padre, texto, nivel=2):
        h = ET.SubElement(padre, f'h{nivel}')
        h.text = texto
        
    def agregarParrafoEn(self, padre, texto):
        p = ET.SubElement(padre, 'p')
        p.text = texto
        
    def agregarImagenEn(self, padre, src, alt):
        ET.SubElement(padre, 'img', src=src, alt=alt)
        
    def escribir(self, nombreArchivo):
        arbol = ET.ElementTree(self.html)
        ET.indent(arbol, space="    ")
        with open(nombreArchivo, 'wb') as f:
            f.write(b'<!DOCTYPE html>\n')
            arbol.write(f, encoding='UTF-8', xml_declaration=False)


def obtenerTexto(raiz, xpath, ns):
    """Función auxiliar para obtener texto de un elemento usando XPath"""
    elem = raiz.find(xpath, ns)
    return elem.text if elem is not None else ''


def obtenerAtributo(raiz, xpath, ns, atributo):
    """Función auxiliar para obtener un atributo de un elemento usando XPath"""
    elem = raiz.find(xpath, ns)
    return elem.get(atributo) if elem is not None else ''


def leerCircuitoXML(nombreArchivo):
    try:
        arbol = ET.parse(nombreArchivo)
        raiz = arbol.getroot()
        ns = {'ns': 'http://www.uniovi.es'}
        
        datos = {
            'nombre': obtenerTexto(raiz, './/ns:nombre', ns),
            'longitudTramo': obtenerTexto(raiz, './/ns:longitudTramo', ns),
            'unidadesLongitud': obtenerAtributo(raiz, './/ns:longitudTramo', ns, 'unidades'),
            'anchuraTramo': obtenerTexto(raiz, './/ns:anchuraTramo', ns),
            'unidadesAnchura': obtenerAtributo(raiz, './/ns:anchuraTramo', ns, 'unidades'),
            'fecha': obtenerTexto(raiz, './/ns:fecha', ns),
            'inicio': obtenerTexto(raiz, './/ns:inicio', ns),
            'vueltas': obtenerTexto(raiz, './/ns:vueltas', ns),
            'localidad': obtenerTexto(raiz, './/ns:localidadProx', ns),
            'pais': obtenerTexto(raiz, './/ns:pais', ns),
            'patrocinador': obtenerTexto(raiz, './/ns:patrocinador', ns),
            'fotos': []
        }
        
        # Usar XPath para obtener todas las fotos
        fotos = raiz.findall('.//ns:foto', ns)
        for foto in fotos:
            datos['fotos'].append({
                'descripcion': foto.get('fDescripcion', ''),
                'ruta': foto.text
            })
        
        return datos
    except Exception as e:
        print(f"Error: {e}")
        return None


def generarHTML(datos, nombreArchivo):
    html = Html(f"Información del Circuito - {datos['nombre']}")
    html.agregarCSS('../estilo/estilo.css')
    
    html.agregarEncabezado(datos['nombre'], 1)
    
    # Sección de información general
    seccionInfo = html.agregarSeccion()
    html.agregarEncabezadoEn(seccionInfo, 'Información General', 2)
    html.agregarParrafoEn(seccionInfo, f"Longitud: {datos['longitudTramo']} {datos['unidadesLongitud']}")
    html.agregarParrafoEn(seccionInfo, f"Anchura: {datos['anchuraTramo']} {datos['unidadesAnchura']}")
    html.agregarParrafoEn(seccionInfo, f"Vueltas: {datos['vueltas']}")
    html.agregarParrafoEn(seccionInfo, f"Fecha: {datos['fecha']} - Hora: {datos['inicio']}")
    
    # Sección de ubicación
    seccionUbicacion = html.agregarSeccion()
    html.agregarEncabezadoEn(seccionUbicacion, 'Ubicación', 2)
    html.agregarParrafoEn(seccionUbicacion, f"{datos['localidad']}, {datos['pais']}")
    html.agregarParrafoEn(seccionUbicacion, f"Patrocinador: {datos['patrocinador']}")
    
    # Sección de fotografías
    if datos['fotos']:
        seccionFotos = html.agregarSeccion()
        html.agregarEncabezadoEn(seccionFotos, 'Fotografías', 2)
        for foto in datos['fotos']:
            html.agregarImagenEn(seccionFotos, foto['ruta'], foto['descripcion'])
    
    html.escribir(nombreArchivo)
    print(f"Archivo HTML generado: {nombreArchivo}")


def main():
    archivoEntrada = 'circuitoEsquema.xml'
    archivoSalida = 'infoCircuito.html'
    datos = leerCircuitoXML(archivoEntrada)
    if datos:
        generarHTML(datos, archivoSalida)


if __name__ == '__main__':
    main()