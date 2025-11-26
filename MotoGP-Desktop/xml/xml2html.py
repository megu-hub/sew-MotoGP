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
        return h
        
    def agregarParrafo(self, texto):
        p = ET.SubElement(self.body, 'p')
        p.text = texto
        return p
        
    def agregarSeccion(self):
        return ET.SubElement(self.body, 'section')
        
    def agregarEncabezadoEn(self, padre, texto, nivel=2):
        h = ET.SubElement(padre, f'h{nivel}')
        h.text = texto
        return h
        
    def agregarParrafoEn(self, padre, texto):
        p = ET.SubElement(padre, 'p')
        p.text = texto
        return p
        
    def agregarListaEn(self, padre):
        return ET.SubElement(padre, 'ul')
        
    def agregarItemListaEn(self, lista, texto):
        li = ET.SubElement(lista, 'li')
        li.text = texto
        return li
        
    def agregarEnlaceEn(self, padre, texto, url):
        a = ET.SubElement(padre, 'a', href=url)
        a.text = texto
        return a
        
    def agregarImagenEn(self, padre, src, alt):
        return ET.SubElement(padre, 'img', src=src, alt=alt)
        
    def agregarVideoEn(self, padre, src):
        video = ET.SubElement(padre, 'video', controls='controls')
        ET.SubElement(video, 'source', src=src, type='video/mp4')
        video.text = 'Tu navegador no soporta el elemento de video'
        return video
        
    def escribir(self, nombreArchivo):
        arbol = ET.ElementTree(self.html)
        ET.indent(arbol, space="    ")
        with open(nombreArchivo, 'wb') as f:
            f.write(b'<!DOCTYPE html>\n')
            arbol.write(f, encoding='UTF-8', xml_declaration=False)

def leerCircuitoXML(nombreArchivo):
    try:
        arbol = ET.parse(nombreArchivo)
        raiz = arbol.getroot()
        namespace = {'ns': 'http://www.uniovi.es'}
        datos = {}
        nombre = raiz.find('.//ns:nombre', namespace)
        datos['nombre'] = nombre.text if nombre is not None else ''
        longitud = raiz.find('.//ns:longitudTramo', namespace)
        datos['longitudTramo'] = longitud.text if longitud is not None else ''
        datos['unidadesLongitud'] = longitud.get('unidades') if longitud is not None else ''
        anchura = raiz.find('.//ns:anchuraTramo', namespace)
        datos['anchuraTramo'] = anchura.text if anchura is not None else ''
        datos['unidadesAnchura'] = anchura.get('unidades') if anchura is not None else ''
        fecha = raiz.find('.//ns:fecha', namespace)
        datos['fecha'] = fecha.text if fecha is not None else ''
        inicio = raiz.find('.//ns:inicio', namespace)
        datos['inicio'] = inicio.text if inicio is not None else ''
        vueltas = raiz.find('.//ns:vueltas', namespace)
        datos['vueltas'] = vueltas.text if vueltas is not None else ''
        localidad = raiz.find('.//ns:localidadProx', namespace)
        datos['localidad'] = localidad.text if localidad is not None else ''
        pais = raiz.find('.//ns:pais', namespace)
        datos['pais'] = pais.text if pais is not None else ''
        patrocinador = raiz.find('.//ns:patrocinador', namespace)
        datos['patrocinador'] = patrocinador.text if patrocinador is not None else ''
        datos['referencias'] = []
        referencias = raiz.findall('.//ns:referencia', namespace)
        for ref in referencias:
            datos['referencias'].append({
                'descripcion': ref.get('rDescripcion'),
                'url': ref.get('url'),
                'texto': ref.text
            })
        datos['fotos'] = []
        fotos = raiz.findall('.//ns:foto', namespace)
        for foto in fotos:
            datos['fotos'].append({
                'descripcion': foto.get('fDescripcion'),
                'ruta': foto.text
            })
        datos['videos'] = []
        videos = raiz.findall('.//ns:video', namespace)
        for video in videos:
            datos['videos'].append({
                'descripcion': video.get('vDescripcion'),
                'ruta': video.text
            })
        vencedor = raiz.find('.//ns:vencedor', namespace)
        if vencedor is not None:
            datos['vencedor'] = vencedor.text
            datos['tiempo'] = vencedor.get('tiempo')
        else:
            datos['vencedor'] = ''
            datos['tiempo'] = ''
        datos['clasificados'] = []
        clasificados = raiz.findall('.//ns:clasificado', namespace)
        for clas in clasificados:
            datos['clasificados'].append(clas.text)
        return datos
    except Exception as e:
        print(f"Error: {e}")
        return None

def generarHTML(datos, nombreArchivo):
    html = Html(f"Información del Circuito - {datos['nombre']}")
    html.agregarCSS('../estilo/estilo.css')
    html.agregarEncabezado(datos['nombre'], 1)
    seccionInfo = html.agregarSeccion()
    html.agregarEncabezadoEn(seccionInfo, 'Informacion General', 2)
    html.agregarParrafoEn(seccionInfo, f"Longitud del tramo: {datos['longitudTramo']} {datos['unidadesLongitud']}")
    html.agregarParrafoEn(seccionInfo, f"Anchura del tramo: {datos['anchuraTramo']} {datos['unidadesAnchura']}")
    html.agregarParrafoEn(seccionInfo, f"Número de vueltas: {datos['vueltas']}")
    html.agregarParrafoEn(seccionInfo, f"Fecha: {datos['fecha']}")
    html.agregarParrafoEn(seccionInfo, f"Hora de inicio: {datos['inicio']}")
    seccionUbicacion = html.agregarSeccion()
    html.agregarEncabezadoEn(seccionUbicacion, 'Ubicación', 2)
    html.agregarParrafoEn(seccionUbicacion, f"Localidad próxima: {datos['localidad']}")
    html.agregarParrafoEn(seccionUbicacion, f"País: {datos['pais']}")
    html.agregarParrafoEn(seccionUbicacion, f"Patrocinador: {datos['patrocinador']}")
    if datos['referencias']:
        seccionRefs = html.agregarSeccion()
        html.agregarEncabezadoEn(seccionRefs, 'Referencias', 2)
        listaRefs = html.agregarListaEn(seccionRefs)
        for ref in datos['referencias']:
            item = html.agregarItemListaEn(listaRefs, '')
            html.agregarEnlaceEn(item, ref['texto'].strip(), ref['url'])
            item.text = f"{ref['descripcion']}: "
            item[-1].tail = ''
    if datos['fotos']:
        seccionFotos = html.agregarSeccion()
        html.agregarEncabezadoEn(seccionFotos, 'Fotografías', 2)
        for foto in datos['fotos']:
            html.agregarImagenEn(seccionFotos, foto['ruta'], foto['descripcion'])
    if datos['videos']:
        seccionVideos = html.agregarSeccion()
        html.agregarEncabezadoEn(seccionVideos, 'Videos', 2)
        for video in datos['videos']:
            html.agregarParrafoEn(seccionVideos, video['descripcion'])
            html.agregarVideoEn(seccionVideos, video['ruta'])
    if datos['vencedor']:
        seccionResultados = html.agregarSeccion()
        html.agregarEncabezadoEn(seccionResultados, 'Resultados', 2)
        html.agregarParrafoEn(seccionResultados, f"Vencedor: {datos['vencedor']}")
        html.agregarParrafoEn(seccionResultados, f"Tiempo: {datos['tiempo']}")
        if datos['clasificados']:
            html.agregarEncabezadoEn(seccionResultados, 'Clasificación', 3)
            listaClasif = html.agregarListaEn(seccionResultados)
            for i, clas in enumerate(datos['clasificados'], 1):
                html.agregarItemListaEn(listaClasif, f"{i}. {clas}")
    html.escribir(nombreArchivo)

def main():
    archivoEntrada = 'circuitoEsquema.xml'
    archivoSalida = 'infoCircuito.html'
    datos = leerCircuitoXML(archivoEntrada)
    if not datos:
        return
    generarHTML(datos, archivoSalida)

if __name__ == '__main__':
    main()