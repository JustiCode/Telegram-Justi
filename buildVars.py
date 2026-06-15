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
    "TelegramJusti_1.1.0 complemento híbrido de accesibilidad para Telegram y Unigram"
),

	# Add-on description
	addon_description=_(
    """TelegramJusti es un complemento híbrido de accesibilidad compatible con Telegram Desktopy Unigram.

Proporciona atajos de teclado, automatización accesible y navegación optimizada para usuarios de NVDA.

Incluye funciones para mensajes de voz, llamadas, videollamadas, navegación rápida entre chats, acceso a perfiles y adjuntos multimedia.

Los gestos son personalizables desde Gestos de Entrada de NVDA."""
),

	# Version
addon_version="1.2.0",

# Changelog
    addon_changelog=_(
    """Versión 1.2.0

Novedades:

* Añadida función para cancelar grabación de mensajes de voz (Ctrl+Shift+R).
* Añadida función para volver directamente a la lista de chats (Alt+Flecha izquierda).
* Implementado enfoque automático en la lista de chats al iniciar Unigram.
* Migración al sistema moderno de scripts mediante @script.
* Eliminado el sistema heredado __gestures.
* Los gestos ahora son reasignables desde Gestos de Entrada de NVDA.
* Migración progresiva a UI Automation y AutomationID.
* Mejorada significativamente la compatibilidad multilenguaje.
* Optimizada la detección de mensajes de voz mediante AutomationID Recognize.
* Mejorada la estabilidad general del complemento.
"""
),

	# Author
	addon_author="Mauro Ocampo JustiCode <drmauroocampo271@gmail.com>",

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