#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class Kml:
    
    def __init__(self):
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')
        
    def agregarPunto(self, nombre, longitud, latitud, altitud=0):
        placemark = ET.SubElement(self.doc, 'Placemark')
        nombreElem = ET.SubElement(placemark, 'name')
        nombreElem.text = nombre
        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = f"{longitud},{latitud},{altitud}"
        
    def agregarLineaString(self, nombre, listaCoords, modoAltitud='clampToGround', extrude='1'):
        placemark = ET.SubElement(self.doc, 'Placemark')
        nombreElem = ET.SubElement(placemark, 'name')
        nombreElem.text = nombre
        lineString = ET.SubElement(placemark, 'LineString')
        extrudeElem = ET.SubElement(lineString, 'extrude')
        extrudeElem.text = extrude
        tessellate = ET.SubElement(lineString, 'tessellate')
        tessellate.text = '1'
        altitudeModeElem = ET.SubElement(lineString, 'altitudeMode')
        altitudeModeElem.text = modoAltitud
        coordinates = ET.SubElement(lineString, 'coordinates')
        coordText = '\n'
        for coord in listaCoords:
            if len(coord) == 2:
                coordText += f"                {coord[0]},{coord[1]},0\n"
            else:
                coordText += f"                {coord[0]},{coord[1]},{coord[2]}\n"
        coordinates.text = coordText + "            "
        
    def escribir(self, nombreArchivo):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol, space="    ")
        arbol.write(nombreArchivo, encoding='UTF-8', xml_declaration=True)
        print(f"Archivo '{nombreArchivo}' generado correctamente")

def leerCircuitoXML(nombreArchivo):
    try:
        arbol = ET.parse(nombreArchivo)
        raiz = arbol.getroot()
        namespace = {'ns': 'http://www.uniovi.es'}
        coordenadas = []
        puntos = raiz.findall('.//ns:punto', namespace)
        for punto in puntos:
            lon = punto.find('ns:pLongitud', namespace)
            lat = punto.find('ns:pLatitud', namespace)
            alt = punto.find('ns:pAltitud', namespace)
            if lon is not None and lat is not None:
                altitud = alt.text if alt is not None else '0'
                coordenadas.append((lon.text, lat.text, altitud))
        return coordenadas
    except Exception as e:
        print(f"Error al leer el archivo XML: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    archivoEntrada = 'circuitoEsquema.xml'
    archivoSalida = 'circuito.kml'
    coordenadas = leerCircuitoXML(archivoEntrada)
    if not coordenadas:
        print(f"No se encontraron coordenadas en el archivo '{archivoEntrada}'")
        return
    print(f"Se encontraron {len(coordenadas)} coordenadas")
    kml = Kml()
    kml.agregarLineaString('Circuito', coordenadas)
    kml.escribir(archivoSalida)

if __name__ == '__main__':
    main()