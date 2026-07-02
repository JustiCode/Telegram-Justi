# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files whenever possible.

from site_scons.site_tools.NVDATool.typings import (
	AddonInfo,
	BrailleTables,
	SymbolDictionaries,
)

from site_scons.site_tools.NVDATool.utils import _


# Add-on information
addon_info = AddonInfo(

	# Internal add-on identifier
	addon_name="TelegramJusti",

	# User-visible add-on name
	addon_summary=_(
		"TelegramJusti 2.0.0 - Complemento híbrido de accesibilidad para Telegram Desktop y Unigram"
	),

	# Add-on description
	addon_description=_(
		"""TelegramJusti es un complemento híbrido de accesibilidad para NVDA compatible con Telegram Desktop y Unigram.

Proporciona automatización accesible, navegación optimizada y gestos completamente reasignables.

Incluye grabación, envío y reproducción de mensajes de voz, llamadas, videollamadas, perfiles, adjuntos multimedia, descarga y apertura de archivos, paneles de emoji y reacciones, transcripción de voz, acceso rápido al cuadro de edición, menú de navegación, regreso a la lista de chats y enfoque automático al iniciar Unigram.

La versión 2.0.0 incorpora una arquitectura multimotor basada en UI Automation, AutomationID y el Motor V8 de búsqueda de controles accesibles, ofreciendo mayor robustez, compatibilidad multilenguaje y mantenimiento futuro."""
	),

	# Version
	addon_version="2.0.0",

	# Changelog
	addon_changelog=_(
		"""Versión 2.0.0

* Migración completa a @script.
* Eliminación de __gestures.
* Gestos completamente reasignables.
* Arquitectura multimotor.
* Motor V8 para búsqueda de controles.
* Migración progresiva a UI Automation y AutomationID.
* Compatibilidad multilenguaje mejorada.
* Nuevas funciones para mensajes de voz, llamadas, videollamadas, adjuntos, paneles, transcripción y navegación.
* Mejoras generales de estabilidad y rendimiento.
"""
	),

	# Author
	addon_author="Mauro Ocampo - JustiCode <drmauroocampo271@gmail.com>",

	# Documentation URL
	addon_url="https://github.com/JustiCode/TelegramJusti",
	addon_sourceURL="https://github.com/JustiCode/TelegramJusti",

	# Documentation filename
	addon_docFileName="readme.html",

	# NVDA compatibility
	addon_minimumNVDAVersion="2026.1",
	addon_lastTestedNVDAVersion="2026.1.1",

	# Update channel
	addon_updateChannel=None,

	# License
	addon_license="GPL v2",
	addon_licenseURL="https://www.gnu.org/licenses/gpl-2.0.html",
)

# Python source files
pythonSources = [
	"addon/appModules/unigram.py",
]

# Translation sources
i18nSources = pythonSources + [
	"buildVars.py",
]

# Excluded files
excludedFiles = []

# Base language
baseLanguage = "es"

# Markdown extensions
markdownExtensions = [
	"markdown.extensions.tables",
]

# Braille tables
brailleTables: BrailleTables = {}

# Symbol dictionaries
symbolDictionaries: SymbolDictionaries = {}