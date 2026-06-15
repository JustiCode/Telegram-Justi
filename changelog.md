# Changelog

Todos los cambios importantes de TelegramJusti serán documentados en este archivo.

---

## Versión 1.2.0
Fecha de lanzamiento: 2026

### Segunda versión pública

### Funciones añadidas

* Añadida función para cancelar grabación de mensajes de voz mediante Ctrl+Shift+R.
* Añadida función para volver directamente a la lista de chats mediante Alt+Flecha izquierda.
  * Implementado enfoque automático en la lista de chats al iniciar Unigram.
* Incorporada confirmación sonora mediante beeps en diversas operaciones del complemento.
* Los gestos ahora pueden reasignarse desde Gestos de Entrada de NVDA.

### Mejoras

* Migración de los scripts al sistema moderno de decoradores mediante `@script`.
* Eliminado el sistema heredado `__gestures`.
* Mejorada significativamente la compatibilidad multilenguaje.
* Migración progresiva de controles a UI Automation y AutomationID.
* Mejorada la compatibilidad con Telegram Desktop y Unigram.
* Reorganización interna del código para facilitar mantenimiento y futuras ampliaciones.
* Mejor compatibilidad con NVDA 2026.1 y posteriores en arquitectura x64.
* Optimizada la detección de mensajes de voz mediante AutomationID `Recognize`.
* Identificado el botón de grabación de voz mediante AutomationID `btnVoiceMessage`.

### Controles migrados a UI Automation y AutomationID

* Perfil del chat.
* Llamadas de voz.
* Videollamadas.
* Nuevo chat.
* Adjuntar multimedia.
* Cuadro de edición de mensajes.
* Menú de navegación.
* Detección de mensajes de voz.
* Botón de grabación de voz (`btnVoiceMessage`).

### Correcciones

* Reducida significativamente la dependencia de etiquetas localizadas en español.
* Migración progresiva desde etiquetas localizadas hacia identificadores UI Automation.
* Mejorada la estabilidad general del complemento.
* Mejorada la detección de perfiles, llamadas y videollamadas.
* Corregidos diversos problemas menores detectados durante las pruebas internas.

### Agradecimientos

Esta versión incorpora numerosas mejoras surgidas a partir de las recomendaciones y sugerencias realizadas durante el proceso de revisión técnica y pruebas de compatibilidad.
