# Cómo producir un video (flujo del 27 nov. 2026)

Las reglas que mandan están en el proyecto de claude.ai "With an Asterisk · Canal": **«00 · LEER PRIMERO»** (roles, permisos, presupuesto, flujo) y **«01 · Reglas del video»** (formato y estilo). Este archivo solo explica la parte técnica. Si algo aquí choca con esos docs, ganan los docs.

## Quién hace qué
1. **8:17 · tarea "producción: guion"**: escribe `guiones/<NNN>_<empresa>_<tema>/guion.md` + `libro_de_afirmaciones.md`, lo sube y se lo manda a Mitre. No renderiza ni genera imágenes.
2. **Chat de control, después del sí de Mitre al guion**: imágenes (banco o nuevas dentro del tope semanal) → `es.py` / `en.py` → vista previa → render → subir → borrador en Metricool → mandarle los dos MP4 a Mitre en el chat (SendUserFile, display render).
3. **Ok final de Mitre** → el chat pasa los borradores a `draft: false`.

## 1. Instalar (3–5 min)
```bash
git clone --depth 1 -b claude/videos https://github.com/mitre444/asterisk-media /home/claude/asterisk-media
bash /home/claude/asterisk-media/setup.sh        # dependencias, voces y enlaces en /home/claude/pipeline
```

## 2. Imágenes (estilo 2D plano)
- Primero el banco: `banco/` (inventario y puntos útiles en el doc «06 · Referencia visual y banco»).
- Imágenes nuevas: solo dentro del tope semanal de «02 · Estado de hoy» y después del sí al guion. `vidiq_image_generate`, `aspectRatio: "9:16"`, todas en una llamada, `referenceImages` = una imagen 2D del banco (solo estilo). Prompt base en el doc 06 (sin texto ni logos dentro de la imagen; tercio superior vacío para el titular).
- Cada `vidiq_job_poll` completado guarda la imagen en el directorio tool-results de la sesión (la ruta sale como "source:"). Cópiala a `guiones/<id>/img/` y, si es reutilizable, también a `banco/` con un nombre descriptivo (`2d_<escena>.jpg`), y agrégala al inventario del doc 06.

## 3. Escenas (motor v4 con fondos de imagen = estilo v5)
Plantilla: `guiones/018_pepsico_papas/gen_v5.py` (genera `es.py` y `en.py` con el mismo plan visual).
- Cada beat: `scene="v4"` y `p["bg"] = [dict(src=img, cue=None, z=(z0, z1), c0=(x, y), c1=(x, y), shade=(arriba, abajo))]`. Cámara lenta: zoom z0→z1 y centro c0→c1 (0–1). Un segundo fondo con `cue` cambia de imagen con destello. `shade` oscurece arriba/abajo para que se lea el titular (1.3–1.5 si el cielo es claro o naranja).
- Titular abajo con `top=1470` y `shade=(0.45, 2.2)` cuando lo importante de la imagen está arriba.
- Logo real: `dict(kind="logo", src="/home/claude/asterisk-media/logos/<marca>.png", x, y, w, h, pin=True)`. `pin=True` lo pega a la imagen aunque la cámara se mueva (también en `counter`).
- Coordenadas: imagen generada 1152x2048 → cuadro 1080x1920 (× 0.9375).
- Sobre imágenes ilustradas: tag, bubble, badge, counter y logo sí; stamp y utilería geométrica (store, fridge, person…) no.

## 4. Vista previa y render
```bash
cd /home/claude/pipeline
python3 -I engine/render.py videos/<id>/es.py --frames   # revisa videos/<id>/out_ES/frames/sheet.jpg
python3 -I engine/render.py videos/<id>/es.py            # render completo (~40 s)
python3 -I engine/render.py videos/<id>/en.py
python3 -I engine/render.py videos/<id>/es.py --scene 2  # rehacer solo una escena
```
Revisa el sheet contra el del episodio anterior: nada encimado, cortado, ilegible o vacío, y que no se parezca al de ayer. Duración 35–50 s (si no, ajusta el guion).

## 5. Subir y Metricool
```bash
mkdir -p <NNN> && cp /home/claude/pipeline/videos/<id>/out_EN/<id>_EN.mp4 <NNN>/<NNN>_EN.mp4 && cp /home/claude/pipeline/videos/<id>/out_ES/<id>_ES.mp4 <NNN>/<NNN>_ES.mp4
git add <NNN> guiones/<id> banco && git commit -m "<NNN> ..." && git -c push.negotiate=true push origin claude/videos
```
URL para Metricool: `https://raw.githubusercontent.com/mitre444/asterisk-media/claude/videos/<NNN>/<NNN>_EN.mp4` (comprueba que responde 200). Antes de crear: `getScheduledPosts` del día en las dos marcas (EN 8160226, ES 8162052); si ya hay publicación, no se crea otra. Parámetros en «01 · Reglas del video» (sección Publicación). Siempre `draft: true` hasta el ok final. Cada `updateScheduledPost` cambia el id: anota el nuevo en «02 · Estado de hoy».
