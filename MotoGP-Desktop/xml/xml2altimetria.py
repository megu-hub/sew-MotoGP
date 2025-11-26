#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import math

class Svg:
    
    def __init__(self, ancho, alto):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1", width=str(ancho), height=str(alto))
        
    def agregarPolilinea(self, puntos, color='black', grosor='2', relleno='none'):
        puntosStr = ' '.join([f"{x},{y}" for x, y in puntos])
        ET.SubElement(self.raiz, 'polyline', points=puntosStr, style=f"fill:{relleno};stroke:{color};stroke-width:{grosor}")
        
    def agregarLinea(self, x1, y1, x2, y2, color='black', grosor='1'):
        ET.SubElement(self.raiz, 'line', x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), style=f"stroke:{color};stroke-width:{grosor}")
        
    def agregarTexto(self, x, y, texto, tamaño='12', color='black', ancla='start'):
        elem = ET.SubElement(self.raiz, 'text', x=str(x), y=str(y), style=f"font-size:{tamaño}px;fill:{color};text-anchor:{ancla}")
        elem.text = texto
        
    def agregarTextoVertical(self, x, y, texto, tamaño='12', color='black'):
        elem = ET.SubElement(self.raiz, 'text', x=str(x), y=str(y), transform=f"rotate(-90 {x} {y})", style=f"font-size:{tamaño}px;fill:{color};text-anchor:middle")
        elem.text = texto
        
    def agregarRectangulo(self, x, y, ancho, alto, color='white', relleno='white'):
        ET.SubElement(self.raiz, 'rect', x=str(x), y=str(y), width=str(ancho), height=str(alto), style=f"fill:{relleno};stroke:{color};stroke-width:1")
        
    def escribir(self, nombreArchivo):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol, space="    ")
        arbol.write(nombreArchivo, encoding='UTF-8', xml_declaration=True)

def calcularDistancias(coordenadas):
    distancias = [0]
    for i in range(1, len(coordenadas)):
        lon1, lat1 = float(coordenadas[i-1][0]), float(coordenadas[i-1][1])
        lon2, lat2 = float(coordenadas[i][0]), float(coordenadas[i][1])
        R = 6371000
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distancia = R * c
        distancias.append(distancias[-1] + distancia)
    return distancias

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
            if lon is not None and lat is not None and alt is not None:
                coordenadas.append((lon.text, lat.text, alt.text))
        return coordenadas
    except Exception as e:
        print(f"Error: {e}")
        return []

def generarAltimetria(coordenadas, nombreArchivo):
    anchoSVG = 1200
    altoSVG = 600
    margenIzq = 80
    margenDer = 40
    margenArr = 40
    margenAbj = 80
    anchoGrafico = anchoSVG - margenIzq - margenDer
    altoGrafico = altoSVG - margenArr - margenAbj
    distancias = calcularDistancias(coordenadas)
    altitudes = [float(coord[2]) for coord in coordenadas]
    distMax = max(distancias)
    altMin = min(altitudes)
    altMax = max(altitudes)
    svg = Svg(anchoSVG, altoSVG)
    svg.agregarRectangulo(0, 0, anchoSVG, altoSVG, 'lightgray', 'white')
    puntosSVG = []
    for i in range(len(distancias)):
        x = margenIzq + (distancias[i] / distMax) * anchoGrafico
        y = margenArr + altoGrafico - ((altitudes[i] - altMin) / (altMax - altMin)) * altoGrafico
        puntosSVG.append((x, y))
    puntosSVG.append((margenIzq + anchoGrafico, margenArr + altoGrafico))
    puntosSVG.append((margenIzq, margenArr + altoGrafico))
    svg.agregarPolilinea(puntosSVG, color='blue', grosor='2', relleno='lightblue')
    svg.agregarLinea(margenIzq, margenArr, margenIzq, margenArr + altoGrafico, 'black', '2')
    svg.agregarLinea(margenIzq, margenArr + altoGrafico, margenIzq + anchoGrafico, margenArr + altoGrafico, 'black', '2')
    numMarcasY = 5
    for i in range(numMarcasY + 1):
        alt = altMin + (altMax - altMin) * i / numMarcasY
        y = margenArr + altoGrafico - (alt - altMin) / (altMax - altMin) * altoGrafico
        svg.agregarLinea(margenIzq - 5, y, margenIzq, y, 'black', '1')
        svg.agregarTexto(margenIzq - 10, y + 5, f"{alt:.0f}m", '12', 'black', 'end')
    numMarcasX = 10
    for i in range(numMarcasX + 1):
        dist = distMax * i / numMarcasX
        x = margenIzq + (dist / distMax) * anchoGrafico
        svg.agregarLinea(x, margenArr + altoGrafico, x, margenArr + altoGrafico + 5, 'black', '1')
        svg.agregarTexto(x, margenArr + altoGrafico + 20, f"{dist:.0f}m", '12', 'black', 'middle')
    svg.agregarTexto(anchoSVG / 2, altoSVG - 20, 'Distancia (m)', '14', 'black', 'middle')
    svg.agregarTextoVertical(20, altoSVG / 2, 'Altitud (m)', '14', 'black')
    svg.agregarTexto(anchoSVG / 2, 25, 'Perfil Altimetrico del Circuito', '16', 'black', 'middle')
    svg.escribir(nombreArchivo)

def main():
    archivoEntrada = 'circuitoEsquema.xml'
    archivoSalida = 'altimetria.svg'
    coordenadas = leerCircuitoXML(archivoEntrada)
    if not coordenadas:
        print("No se encontraron coordenadas")
        return
    generarAltimetria(coordenadas, archivoSalida)

if __name__ == '__main__':
    main()