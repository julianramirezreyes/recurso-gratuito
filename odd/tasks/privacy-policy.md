# Publicar la política de privacidad de Oficina de Agentes

## Objetivo

Publicar una URL pública para la política de privacidad de la app Oficina de Agentes, usada con Instagram @modoverbo.

## Alcance y restricciones

- Crear únicamente la página nueva `/privacidad`; no modificar otras páginas ni la configuración de Meta.
- Usar el texto previamente aprobado por la persona usuaria, limitado al tratamiento de datos de Oficina de Agentes.
- No incorporar analítica ni scripts a la página de política.
- Mantener la rama `main` por instrucción de la persona usuaria.
- URL prevista: `https://modoverborecursos.vercel.app/privacidad`.

## Tareas

- [x] **T1 — Crear y comprobar la página.** Escribir primero una prueba que falle por la ausencia de la página; crear `privacidad/index.html` con la política aprobada; ejecutar la prueba y toda la suite. Criterio: el contenido y correo acordados se leen en el HTML, la página no carga scripts ni analítica, y todas las pruebas pasan. Ruta: delegada directa; la prueba y la página son dos archivos no triviales.
- [x] **T2 — Publicar y verificar la URL.** Publicar exclusivamente este cambio en Vercel y comprobar sin iniciar sesión que `/privacidad` abre y devuelve el texto. Criterio: URL pública con contenido aprobado y sin regresión de la página principal. Ruta: directa; despliegue manual desde el commit en `main`.

## Verificación y progreso

- TDD estricto: RED → GREEN → REFACTOR, indicado por las instrucciones de la sesión.
- Pruebas: `python3 -m unittest discover -s tests -v`.
- Estrategia de entrega: `ask-on-risk`; previsión inferior a 400 líneas de cambios propios.
- Estado inicial: `main` limpia; sin página de privacidad.
- T1: se observaron 2 fallos esperados por página ausente antes de crearla. Después, la prueba focalizada pasó (2 pruebas) y la suite completa pasó (23 pruebas); `git diff --check` pasó. La página no tiene scripts ni recursos externos. Commit `b363022` en `main`.
- T2: `b363022` se envió a GitHub y se desplegó manualmente en producción desde Vercel porque el push no generó un despliegue automático. `https://modoverborecursos.vercel.app/privacidad` respondió HTTP 200 sin autenticación y devolvió el título acordado. La página principal no se modificó.
- Próximo paso: entregar la URL pública a la persona usuaria.

Ruta relativa del documento: `odd/tasks/privacy-policy.md`.
