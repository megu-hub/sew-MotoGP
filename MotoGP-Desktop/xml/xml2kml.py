#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class Kml:
    
    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')
        
    def addPlacemark(self,nombre,descripcion,long,lat,alt, modoAltitud):
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud
        
    def addLineString(self,nombre,extrude,tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """

        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = str(ancho)

        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellation').text = tesela
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud 

        
        coords_text = "\n".join(
            f"{lon},{lat},{alt}" for lon, lat, alt in listaCoordenadas
        )
        ET.SubElement(ls, 'coordinates').text = coords_text

        
        
    def escribir(self, nombreArchivo):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
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
    kml.addLineString("Altimetría","1","1",
                           coordenadas,'relativeToGround',
                           '#ff0000ff',"5")
    kml.escribir(archivoSalida)

if __name__ == '__main__':
    main()
