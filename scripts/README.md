# Generar el CV en PDF

El script `generate-cv-pdf.py` transforma el contenido de `README.md` en un CV PDF A4 con una presentación más limpia: cabecera destacada, jerarquía tipográfica, color de acento, enlaces y reglas de paginación para impresión.

El README es la fuente única del contenido. La versión web mantiene el formato Markdown y el script aplica una capa visual específica para el PDF.

## Requisitos

- Python 3.9 o superior
- Google Chrome o Chromium instalado y disponible en el `PATH`

En macOS también se detectan las instalaciones habituales en `/Applications`.

## Uso

Desde la raíz del repositorio:

```bash
python3 scripts/generate-cv-pdf.py
```

El archivo se genera como `CV-Daniel-Sacco.pdf`. Para elegir otro destino:

```bash
python3 scripts/generate-cv-pdf.py --output ~/Downloads/daniel-sacco-cv.pdf
```

También se puede utilizar otro archivo Markdown como fuente:

```bash
python3 scripts/generate-cv-pdf.py --input README.md --output CV.pdf
```

El HTML intermedio se crea temporalmente y se elimina automáticamente. El PDF no se versiona en el repositorio; después de actualizar el README, vuelve a ejecutar el comando para regenerarlo.
