# Generar el CV en PDF

El script `generate-cv-pdf.py` transforma el contenido de `README.md` en un PDF con formato A4, tipografía limpia, colores y estilos de CV. La tabla de contenidos se conserva en GitHub, pero se excluye del PDF.

## Requisitos

- Python 3.9 o superior
- Google Chrome o Chromium instalado y disponible en el `PATH`

## Uso

Desde la raíz del repositorio:

```bash
python3 scripts/generate-cv-pdf.py
```

El archivo se genera como `CV-Daniel-Sacco.pdf`. Para elegir otro destino:

```bash
python3 scripts/generate-cv-pdf.py --output ~/Downloads/daniel-sacco-cv.pdf
```

El HTML intermedio se crea temporalmente y se elimina automáticamente. El PDF no se versiona en el repositorio; se puede regenerar cada vez que se actualice el README.
