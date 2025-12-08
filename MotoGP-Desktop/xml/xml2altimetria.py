#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import math

class Svg:
    """Clase para generar archivos SVG simples con polylines y texto."""
    
    def __init__(self, width="2200", height="1000"):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', 
                               xmlns="http://www.w3.org/2000/svg", 
                               version="2.0",
                               width=width,
                               height=height)
        

    def addPolyline(self,points,stroke,strokeWidth,fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz,'polyline',
                      points=points,
                      stroke=stroke,
                      **{'stroke-width': strokeWidth},
                      fill=fill)
            
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        """
        Añade un elemento texto
        """
        text_elem = ET.SubElement(self.raiz,'text',
                                   x=x,
                                   y=y,
                                   **{'font-family': fontFamily,
                                      'font-size': fontSize},
                                   style=style)
        text_elem.text = texto
    
    def addLine(self,x1,y1,x2,y2,stroke,strokeWidth):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz,'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      **{'stroke-width': strokeWidth})
        
       
    def escribir(self,nombreArchivoSVG):
        """
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentación y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        
        arbol.write(nombreArchivoSVG, 
                    encoding='utf-8', 
                    xml_declaration=True
                    )



def leerCircuitoXML(nombreArchivo):
    try:
        arbol = ET.parse(nombreArchivo)
        raiz = arbol.getroot()
        namespace = {'ns': 'http://www.uniovi.es'}
        coordenadas = []
        
        # Usar XPath para buscar todos los puntos
        puntos = raiz.findall('.//ns:punto', namespace)
        
        for punto in puntos:
            # Usar XPath para buscar longitud, latitud y altitud
            lon = punto.find('ns:pLongitud', namespace)
            lat = punto.find('ns:pLatitud', namespace)
            alt = punto.find('ns:pAltitud', namespace)
            
            if lon is not None and lat is not None and alt is not None:
                coordenadas.append((float(lon.text), float(lat.text), float(alt.text)))

        return coordenadas
    except Exception as e:
        print(f"Error: {e}")
        return []

def generarAltimetria(coordenadas):
    print(Svg.__doc__)
    nombreArchivo = "altimetria.svg"

    nuevoSVG = Svg()
    
    ancho_svg = 800
    alto_svg = 600
    margen = 100

    # Extraer solo las altitudes
    altitudes = [alt for _, _, alt in coordenadas]
    min_alt = min(altitudes)
    max_alt = max(altitudes)
    rango_alt = max_alt - min_alt if max_alt != min_alt else 1
    n = len(altitudes)
    points = []
    
    # Area de dibujo con márgenes
    ancho_grafico = ancho_svg - 2 * margen
    alto_grafico = alto_svg - 2 * margen
    
    for i, alt in enumerate(altitudes):
        # X position evenly spaced along the SVG width
        x = margen + (i * ancho_grafico / (n - 1) if n > 1 else 0)
        # Y position scaled inversely because SVG y=0 is top
        y = margen + (alto_grafico - ((alt - min_alt) / rango_alt * alto_grafico))
        points.append(f"{x},{y}")

    points_str = " ".join(points)
    
    nuevoSVG.addLine(str(margen), str(margen), str(margen), str(alto_svg - margen), 'white', '2')
    
    nuevoSVG.addLine(str(margen), str(alto_svg - margen), str(ancho_svg - margen), str(alto_svg - margen), 'white', '2')
    
    nuevoSVG.addText(f"{max_alt:.0f}m", str(margen - 60), str(margen + 5), 
                     'Arial', '14', 'fill:white')
    nuevoSVG.addText(f"{min_alt:.0f}m", str(margen - 60), str(alto_svg - margen + 5), 
                     'Arial', '14', 'fill:white')
    
    nuevoSVG.addText("Distancia", str(ancho_svg / 2 - 40), str(alto_svg - margen + 40), 
                     'Arial', '16', 'fill:white')
    
    nuevoSVG.addPolyline(points_str, 'red', '4', 'none') 
    
    nuevoSVG.escribir(nombreArchivo)
    print("Creado el archivo: ", nombreArchivo)

def main():
    archivoEntrada = 'circuitoEsquema.xml'
    archivoSalida = 'altimetria.svg'
    coordenadas = leerCircuitoXML(archivoEntrada)
    if not coordenadas:
        print("No se encontraron coordenadas")
        return
    generarAltimetria(coordenadas)


if __name__ == '__main__':
    main()