# Cómo producir un video (cualquier sesión o tarea)

Este repo es **público**: se instala sin permisos. Todo vive aquí: motor, guiones, logos y videos terminados.

## 1. Instalar (3–5 min)
```bash
git clone --depth 1 -b claude/videos https://github.com/mitre444/asterisk-media /home/claude/asterisk-media
bash /home/claude/asterisk-media/setup.sh        # dependencias, voces y enlaces en /home/claude/pipeline
```
Si el clon ya existe: `git -C /home/claude/asterisk-media pull --depth 1 origin claude/videos`.

## 2. Producir
1. Leer en el proyecto "With an Asterisk · Canal": `claude/13 Reglas vigentes.md` (única fuente de verdad), el reporte del día del doc 03 y el doc 00.
2. Crear `guiones/<NNN>_<empresa>_<tema>/es.py` y `en.py` (copiar la estructura de `guiones/017_dominos_masa/`) y `libro_de_afirmaciones.md`.
3. Vista previa: `cd /home/claude/pipeline && python3 -I engine/render.py videos/<id>/es.py --frames` → revisar `videos/<id>/out_ES/frames/sheet.jpg` (nada encimado, nada cortado, ningún tramo vacío, utilería a escala 1.0–1.2).
4. Render: `python3 -I engine/render.py videos/<id>/es.py` y `en.py`.
5. Logos: `logo="/home/claude/asterisk-media/logos/<empresa>.png"` en `store` y `fridge`. Si no hay logo, el nombre va en texto sobre el color de la marca.

## 3. Subir y publicar (necesita permiso de escritura en este repo)
```bash
mkdir -p <NNN> && cp .../out_EN/<id>_EN.mp4 <NNN>/<NNN>_EN.mp4 && cp .../out_ES/<id>_ES.mp4 <NNN>/<NNN>_ES.mp4
git add <NNN> guiones/<id> && git commit -m "<NNN> ..." && git -c push.negotiate=true push origin claude/videos
```
URL pública para Metricool: `https://raw.githubusercontent.com/mitre444/asterisk-media/claude/videos/<NNN>/<NNN>_EN.mp4`.

**Metricool:** antes de crear nada, `getScheduledPosts` en las dos marcas (EN 8160226, ES 8162052) para el día. Si ya hay una publicación del día, NO se crea otra. Solo la tarea de producción crea publicaciones, y las crea como **borrador** (`draft: true`). Los chats solo aprueban (pasan el borrador a `draft: false`) o cambian.

## 4. Anotar
En cuanto los MP4 estén subidos, anotar el video en el doc 00 del proyecto (tabla "Videos publicados" o "Listos para aprobar"), con los ids de Metricool.
