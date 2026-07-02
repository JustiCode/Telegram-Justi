### Changelog

Todos los cambios importantes de TelegramJusti serán documentados en este archivo.

Esta versión representa la primera gran reforma estructural de TelegramJusti, incorporando una profunda modernización de la arquitectura interna, compatibilidad multilenguaje, migración a UI Automation y AutomationID, adopción del sistema moderno de scripts de NVDA e incorporación del Motor V8 para localización inteligente de controles accesibles.

---
# Versión 2.0.0

Fecha de lanzamiento: 2026

## Reforma estructural del proyecto

---
## Nuevas funciones

* Grabación de mensajes de voz.
* Envío de mensajes de voz.
* Cancelación de grabación mediante **Ctrl+Shift+R**.
* Reproducción y pausa inteligente de mensajes de voz.
* Inicio de llamadas de voz.
* Inicio de videollamadas.
* Finalización de llamadas mediante `InvokePattern`.
* Activación y desactivación del micrófono.
* Activación y desactivación de la cámara.
* Activación y desactivación de compartir pantalla.
* Apertura rápida de perfiles.
* Adjuntar archivos multimedia.
* Apertura de archivos adjuntos.
* Descarga de archivos adjuntos.
* Creación de nuevos chats.
* Acceso rápido al cuadro de edición de mensajes.
* Apertura del menú de navegación.
* Apertura del panel de reacciones.
* Apertura del panel de emoji, stickers y GIF.
* Apertura de la transcripción de mensajes de voz.
* Desplazamiento directo al último mensaje.
* Regreso inmediato a la lista de chats mediante **Alt+Flecha izquierda**.
* Enfoque automático en la lista de chats al iniciar Unigram.
* Confirmaciones auditivas mediante tonos en las principales operaciones.
* Gestos completamente reasignables desde Gestos de Entrada de NVDA.

---

## Mejoras técnicas

* Migración completa al sistema moderno de scripts mediante decoradores `@script`.
* Eliminación definitiva del sistema heredado `__gestures`.
* Incorporación de una **arquitectura multimotor**, integrando compatibilidad para Telegram Desktop, Unigram y el nuevo Motor V8 de búsqueda inteligente de controles accesibles.
* Implementación del **Motor V8**, optimizando la localización de controles mediante nombre, rol, UI Automation y AutomationID.
* Incorporación de activación especializada mediante `InvokePattern`.
* Migración prácticamente completa desde etiquetas localizadas hacia **UI Automation** y **AutomationID**.
* Internacionalización completa de mensajes y descripciones mediante `_()`, preparando el complemento para futuras traducciones.
* Compatibilidad multilenguaje significativamente mejorada.
* Reestructuración interna del código para facilitar mantenimiento, escalabilidad y futuras ampliaciones.
* Optimización de la lógica de reproducción de mensajes de voz, diferenciando correctamente entre cuadros de edición y controles reproducibles.
* Optimización general del rendimiento, la estabilidad y la robustez del complemento.

---

## Controles y funciones migrados a UI Automation y AutomationID

* Perfil del chat.
* Llamadas de voz.
* Videollamadas.
* Finalización de llamadas.
* Micrófono.
* Cámara.
* Compartir pantalla.
* Nuevo chat.
* Adjuntar multimedia.
* Cuadro de edición de mensajes.
* Menú de navegación.
* Panel de reacciones.
* Panel de emoji, stickers y GIF.
* Transcripción de mensajes de voz.
* Detección de mensajes de voz.
* Botón de grabación de voz (`btnVoiceMessage`).
* Botón reproducir (`Button`).
* Botón volver atrás (`BackButton`).
* Botón último mensaje (`MessagesButton`).
* Botón de descarga (`Download`).
* Botón de adjuntos (`ButtonAttach`).
* Lógica contextual de reproducción de mensajes de voz mediante detección inteligente del foco.

---

## Compatibilidad

* NVDA 2026.1 o superior.
* Compatible con NVDA 2026.1.1.
* Arquitectura x64.
* Telegram Desktop.
* Unigram.
* Compatibilidad multilenguaje mediante UI Automation y AutomationID.

---

## Correcciones

* Eliminación progresiva de dependencias de etiquetas localizadas en español.
* Mejora en la localización de controles accesibles.
* Mayor estabilidad durante llamadas y videollamadas.
* Optimización de la detección de mensajes de voz mediante AutomationID `Recognize`.
* Mejora del comportamiento contextual de la barra espaciadora para reproducción de mensajes de voz.
* Mejoras generales de compatibilidad con Telegram Desktop y Unigram.
* Corrección de diversos problemas detectados durante las pruebas internas, Beta Testing y el proceso de revisión técnica realizado por NVDA.ES.

---
## Agradecimientos

Esta versión incorpora numerosas mejoras surgidas a partir de la experiencia cotidiana de uso, las pruebas realizadas por Beta Testers y las recomendaciones recibidas durante el proceso de revisión técnica.

Mi agradecimiento a todos y todas los que colaboraron,  por el tiempo dedicado a las pruebas, aportes   y sugerencias.

Un reconocimiento especial a Héctor Benítez y José Manuel Delicado, de NVDA.ES, cuyos comentarios y observaciones técnicas resultaron fundamentales para la modernización del complemento y su adaptación a las recomendaciones actuales de desarrollo para NVDA.
