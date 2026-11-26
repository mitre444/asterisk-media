# Guía de estilo v3 · With an Asterisk / Con Asterisco

**Vigente desde el 22 nov. 2026.** Mitre aprobó adoptar todo lo investigado sobre los competidores hechos con IA (docs 08 y 09 del proyecto). Primer video con este estándar: 005 GTA 6, el primer día. Lo que contradiga esta guía en docs o videos anteriores ya no aplica.

Cada regla dice de dónde sale (A1–A10 = principios del doc 09; datos = nuestras métricas).

## 1. Antes de escribir
1. **Referencias:** 1–3 videos de la competencia (prioridad: cuentas hechas con IA, doc 09), al menos uno visto escena por escena. Van a `videos/<id>/referencias.md` con la plantilla: qué tomamos, qué hacemos distinto.
2. **Tema:** "¿por qué pasó X?" o "¿cuál es el truco?" sobre una marca o cosa que todos conocen. Evitar temas que pidan saber de finanzas (dividendos, segmentos, proyecciones): son nuestros peores videos (002, 012, 004).
3. **Ancla por idioma:** la misma marca si se conoce en los dos mercados; si no, una marca local del mismo dueño (verificada) o el ángulo del bolsillo; si no hay ancla, sale solo en EN. El español se escribe, no se traduce.

## 2. Estructura (60–80 s)
- **Gancho (0–5 s):** contradicción + marca conocida + cifra, dicha y escrita completa desde el cuadro 1. Pregunta corta al final ("¿Cómo?"). Nada de nombres que poca gente ubica en el gancho. (Datos: 003 y 006, los dos mejores skips, son contradicciones.)
- **Remate temprano (antes del segundo 15–18):** media respuesta que sorprenda ("respuesta corta: no es el mismo dinero"). Nunca guardar todo para el final. (A1; la gente se iba a los ~20 s.)
- **3 capas numeradas (1/3, 2/3, 3/3):** cada una con su propio dato y su golpe visual, una cada 10–20 s. El número de capa siempre visible. (A1, A7)
- **El asterisco:** un giro final que el espectador no esperaba, con fuente.
- **Respuesta completa** a la pregunta del gancho + "nuestra lectura" dicha y escrita cuando es interpretación.
- **Cierre:** compartir con un **arquetipo concreto ligado al tema** ("mándaselo a ese amigo que…") o una pregunta para comentar, y seguir. Nada de "mándaselo a alguien" genérico (0 compartidos en 013 y 006). (A8)
- **Sin timer de gancho** (no cambió nada en los datos).
- Una cifra por momento. Toda cifra grande con una comparación que se sienta. Jerga solo si se explica en la misma frase.

## 3. Visual
- **Un mundo concreto que la cámara recorre** (`world=` en el spec, `engine/world.py`): calle, tienda, puerto, oficina. Cada beat dice dónde está la cámara (`at=`). Se acabó el fondo abstracto con partículas para videos nuevos. (A3)
- **Alguien vive la historia:** "tú" en la fila, personajes genéricos sin cara, empresas como edificios. (A2)
- **Marca como lugar u objeto** (fachada, letrero, camión, documento), con el nombre en texto. No se dibujan logos; un logo real solo si Mitre aporta el archivo oficial con licencia (`assets_externos/` + `licencias.md`). Nada que sugiera patrocinio. (A5)
- Texto grande arriba (cielo) sobre franja oscura translúcida; mundo en el centro; subtítulos sobre la calle; la franja de abajo queda libre para la interfaz de cada red.
- Planos de 4–7 s con movimiento dentro (personajes, monedas, cámara que viaja), no cortes cada 2 s sin narrativa. (A9)
- Estilo "tarjeta impresa" (contorno de tinta, sombra dura, semitono) para todo lo dibujado.
- El asterisco de marca nunca grande al centro.
- Revisar la hoja de cuadros (`--frames`) antes del render completo, al lado de capturas de la referencia.

## 4. Sonido
- **Música con ritmo, bajita y brillante** (`music=dict(style="groove", bpm=112, gain=0.17, duck=0.6)`), no música de tensión. Sin silencio total. (A4)
- Efectos ligados a lo que pasa en pantalla (moneda, caja, sello), no por relleno.
- Voz: EN af_heart, ES em_alex. −14 LUFS. Revisar con el reconocedor las frases marcadas "REVISAR" (si solo cambia el formato de un número, está bien).
- Inglés: siglas con puntos ("G.T.A."). Español: lexicón del spec.

## 5. Fuentes
- Cada afirmación en `libro_de_afirmaciones.md` con valor exacto, fuente y nota. Cálculos propios marcados.
- **Nada de etiquetas de fuente en las escenas.** Al final, una **tarjeta de fuentes** de ~1.8 s (`sources_card=[...]`, `tail=2.5`) y las fuentes completas en la descripción de cada red. (Pedido de Mitre, A6)

## 6. Antes de renderizar y después de publicar
- Puntuar el guion con el marco de 8 criterios del doc 08 (mínimo 12/16, ningún 0) y anotarlo en `referencias.md`.
- A las 48 h, medir contra el promedio de la cuenta (skip <3 s y tiempo medio en IG; vistas por red) y anotarlo en el laboratorio del doc 08.

## Plantilla mínima del spec v3
```python
SPEC = dict(
    id="0XX_tema", lang="en-us", lang_tag="EN", voice="af_heart", brand="WITH AN ASTERISK",
    world=dict(shops=[...], queue=dict(x0=880, n=6, gap=82)),
    camera=dict(push=0.03, enter=0.08, punch=[...], shake=[...]),
    music=dict(style="groove", bpm=112, gain=0.17, duck=0.6),
    tail=2.5, card_dur=1.8, card_title="SOURCES", sources_card=["...", "..."],
    beats=[dict(scene="w_hook", at=..., ...), dict(scene="w_board", ...), dict(scene="w_layer", ...) x3,
           dict(scene="w_note", ...), dict(scene="w_answer", ...)],
    post=dict(tiktok="... fuentes completas ...", title="..."),
)
```
Escenas del mundo: `w_hook` (pregunta), `w_board` (dos cifras + remate temprano, cue `nb`), `w_layer` (capa N/M; `anim` = register | split | stack), `w_note` (documento con su nota al pie, cue `est`), `w_answer` (respuesta + seguir). Ejemplo completo: `videos/005_gta6_dia_uno/`.
