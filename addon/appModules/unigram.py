# -*- coding: utf-8 -*-

"""
Telegram Justi 
Complemento NVDA para Telegram Unigram.

Autor:
Mauro Ocampo - JustiCode
"""

import time

import api
import controlTypes
import tones
import ui
import wx
import appModuleHandler
import keyboardHandler
import logHandler
import sys
import scriptHandler
from addonHandler import initTranslation

initTranslation()

log = logHandler.log


class AppModule(appModuleHandler.AppModule):
    """AppModule principal para Telegram Unigram."""

    lastAudioGesture = 0

    # =========================================================
    # Utilidades internas
    # =========================================================

    def sendKey(self, keyName):
        """Envía una combinación de teclas."""

        try:
            gesture = keyboardHandler.KeyboardInputGesture.fromName(
                keyName
            )

            gesture.send()

            time.sleep(0.08)

        except Exception:
            log.exception(
                "Error enviando tecla: %s",
                keyName
            )

    def findObjectByName(
        self,
        obj,
        target,
        className=None
    ):
        """
        Busca recursivamente un objeto
        por coincidencia parcial de nombre.
        """

        if not obj:
            return None

        try:
            name = obj.name or ""

            if target.lower() in name.lower():
                return obj

        except Exception:
            pass

        try:
            child = obj.firstChild

            while child:

                result = self.findObjectByName(
                    child,
                    target
                )

                if result:
                    return result

                child = child.next

        except Exception:
            pass

        return None

    def findObjectByAutomationID(self, obj, targetID):
        """Busca un objeto por AutomationID."""

        if not obj:
            return None

        try:
            automationID = getattr(
                obj,
                "UIAAutomationId",
                ""
            ) or ""

            if automationID == targetID:
                return obj

        except Exception:
            pass

        try:
            child = obj.firstChild

            while child:

                result = self.findObjectByAutomationID(
                    child,
                    targetID
                )

                if result:
                    return result

                child = child.next

        except Exception:
            pass

        return None

    def findChildrenByRole(
        self,
        parent,
        role,
        className=None
    ):
        """
        Devuelve una lista con todos los hijos
        que coinciden con un rol determinado.
        """

        matches = []

        if not parent:
            return matches
        try:

            child = parent.firstChild

            while child:

                try:

                    if getattr(child, "role", None) == role:

                        if (
                            className is None
                            or getattr(
                                child,
                                "UIAClassName",
                                ""
                            )
                            == className
                        ):

                            matches.append(
                                child
                            )

                except Exception:
                    pass

                child = child.next

        except Exception:

            log.exception(
                "Error buscando hijos por rol"
            )

        return matches

    def dumpTree(
        self,
        obj,
        level=0,
        maxLevel=3
    ):
        """
        Recorre el árbol UIA y verbaliza
        nombre, rol, AutomationID y clase.
        """

        if not obj or level > maxLevel:
            return

        try:

            ui.message(
                "%sNivel %d | %s | %s | %s | %s" % (
                    "  " * level,
                    level,
                    obj.name or "",
                    getattr(obj, "role", ""),
                    getattr(obj, "UIAAutomationId", ""),
                    getattr(obj, "UIAClassName", "")
                )
            )

        except Exception:
            pass
        try:

            child = obj.firstChild

            while child:

                self.dumpTree(
                    	child,
                    level + 1,
                    maxLevel
                )

                child = child.next

        except Exception:
            pass

    def findObjectByNameAndRole(
        self,
        obj,
        targetName,
        targetRole
    ):
        """
        Busca recursivamente un objeto
        por nombre y rol.
        """

        if not obj:
            return None

        try:

            name = (obj.name or "").lower()

            if (
                name == targetName.lower()
                and obj.role == targetRole
            ):
                return obj

        except Exception:
            pass

        try:

            child = obj.firstChild

            while child:

                result = self.findObjectByNameAndRole(
                    child,
                    targetName,
                    targetRole
                )

                if result:
                    return result

                child = child.next

        except Exception:
            pass

        return None

    def activateObject(self, obj):
        """
        Activa un objeto accesible.

        Primero intenta doAction().
        Si falla, enfoca y pulsa espacio.
        """

        if not obj:
            return False

        try:
            obj.doAction()
            return True

        except Exception:
            pass

        try:
            obj.setFocus()

            time.sleep(0.1)

            self.sendKey("space")

            return True

        except Exception:
            pass

        try:

            obj.setFocus()

            time.sleep(0.1)

            self.sendKey("enter")

            return True

        except Exception:
            pass

        return False

    def invokeObject(self, obj):
        """
        Intenta activar un objeto mediante
        InvokePattern de UI Automation.
        """

        if not obj:
            return False

        try:

            obj.doAction()

            return True

        except Exception:

            pass

        return False

    def activateChildAutomationID(
        self,
        parent,
        automationID,
    ):
        """
        Activa un hijo identificado por AutomationID.
        """

        if not parent:
            return False

        try:

            child = parent.firstChild

            while child:

                try:
                    if (
                        getattr(
                            child,
                            "UIAAutomationId",
                            ""
                        )
                        == automationID
                    ):

                        self.activateObject(
                            child
                        )

                        return True

                except Exception:
                    pass

                child = child.next

        except Exception:

            log.exception(
                "Error buscando hijo AutomationID: %s",
                automationID
            )

        return False
    def activateNamedControl(
        self,
        targetName,
        successMessage=None,
        errorMessage=None,
        beepFrequency=1000
    ):
        """
        Busca y activa un control por nombre.
        """

        fg = api.getForegroundObject()

        try:
            control = self.findObjectByName(
                fg,
                targetName
            )

            if not control:

                if errorMessage:
                    ui.message(errorMessage)

                return False

            self.activateObject(control)

            tones.beep(beepFrequency, 100)

            if successMessage:
                ui.message(successMessage)

            return True

        except Exception:
            log.exception(
                "Error activando control: %s",
                targetName
            )

            if errorMessage:
                ui.message(errorMessage)

        return False

    # =========================================================
    # Eventos
    # =========================================================

    def event_gainFocus(self, obj, nextHandler):
        """
        Enfoca automáticamente
        la lista de chats al iniciar Unigram.
        """

        try:

            if (
                getattr(
                obj,
                "UIAAutomationId",
                    ""
                ) == "Photo"
            ):

                def focusChats():

                    self.sendKey("tab")
                    time.sleep(0.1)

                    self.sendKey("tab")
                    time.sleep(0.1)

                    self.sendKey("tab")

                wx.CallLater(
    600,
    focusChats
)

        except Exception:
            log.exception(
                "Error enfocando lista de chats"
            )

        nextHandler()

        # =========================================================
    # Scripts
    # =========================================================

    @scriptHandler.script(
        description=_("Grabar o enviar mensaje de voz"),
        category=_("Telegram Justi"),
        gesture="kb:control+r"
    )
    def script_voiceMessage(self, gesture):
        """Graba o envía mensajes de voz."""
        currentTime = time.time()

        try:

            if (
                currentTime - self.lastAudioGesture
                < 0.5
            ):

                self.sendKey("control+enter")

                tones.beep(1200, 100)

            else:

                self.sendKey("control+r")

                tones.beep(700, 100)

            self.lastAudioGesture = currentTime

        except Exception:
            log.exception(
                "Error gestionando audio"
            )

    @scriptHandler.script(
        description=_("Cancelar grabación de mensaje de voz"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+r"
    )
    def script_cancelVoiceMessage(self, gesture):

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "ButtonCancelRecording"
        )

        if not button:
            tones.beep(200, 50)
            return

        try:
            button.doAction()

            tones.beep(500, 80)

        except Exception:

            log.exception(
                "Error cancelando grabación"
            )

            ui.message(
                _("No se pudo cancelar la grabación")
            )

    @scriptHandler.script(
        description=_("Reproducir o pausar mensaje de voz"),
        category=_("Telegram Justi"),
        gesture="kb:space"
    )
    def script_playPauseAudio(self, gesture):
        """Reproduce o pausa mensajes de voz."""

        try:

            focus = api.getFocusObject()

            if not focus:
                gesture.send()
                return

            if focus.role == controlTypes.Role.EDITABLETEXT:
                gesture.send()
                return

            button = None

            if (
                focus.role == controlTypes.Role.BUTTON
                and getattr(focus, "UIAAutomationId", "") == "Button"
            ):
                button = focus

            elif focus.role == controlTypes.Role.LISTITEM:
                button = self.findObjectByAutomationID(
                    focus,
                    "Button"
                )

            if not button:
                gesture.send()
                return

            self.activateObject(
                button
            )

            tones.beep(
                900,
                50
            )

        except Exception:

            log.exception(
                "Error reproduciendo mensaje de voz"
            )

            ui.message(
                _("No fue posible reproducir el mensaje de voz")
            )

    @scriptHandler.script(
        description=_("Abrir perfil del chat actual"),
        category=_("Telegram Justi"),
        gesture="kb:control+p"
    )
    def script_openProfile(self, gesture):
        """Abre el perfil del chat actual."""

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "Profile"
        )

        if not button:
            ui.message(
                _("Perfil no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(900, 80)

        except Exception:

            log.exception(
                "Error abriendo perfil"
            )

            ui.message(
                _("No se pudo abrir el perfil")
            )

    @scriptHandler.script(
        description=_("Inicia una llamada de voz"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+l"
    )
    def script_voiceCall(self, gesture):
        """Inicia una llamada de voz."""

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "Call"
        )

        if not button:
            ui.message(
                _("Botón llamar no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(1000, 80)

        except Exception:

            log.exception(
                "Error iniciando llamada"
            )

            ui.message(
                _("No se pudo iniciar la llamada")
            )

    @scriptHandler.script(
        description=_("Iniciar videollamada"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+v"
    )
    def script_videoCall(self, gesture):
        """Inicia una videollamada."""

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "VideoCall"
        )

        if not button:
            ui.message(
                _("Botón videollamada no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(1200, 100)

        except Exception:

            log.exception(
                "Error iniciando videollamada"
            )

            ui.message(
                _("No fue posible iniciar la videollamada")
            )

    @scriptHandler.script(
        description=_("Finalizar llamada"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+n"
    )
    def script_endCall(self, gesture):
        """Finaliza una llamada."""

        try:

            fg = api.getForegroundObject()

            if not fg:
                return

            button = self.findObjectByNameAndRole(
                fg,
                "finalizar",
                controlTypes.Role.BUTTON
            )
            if not button:

                ui.message(
                    _("Botón finalizar no encontrado")
                )

                return

            if self.invokeObject(button):

                tones.beep(
                    700,
                    80
                )

                ui.message(
                    _("Llamada finalizada")
                )

                return
            ui.message(
                _("Botón finalizar no encontrado")
            )

        except Exception:

            log.exception(
                "Error explorando árbol de llamada"
            )

            ui.message(
                _("No fue posible finalizar la llamada")
            )
          
    @scriptHandler.script(
        description=_("Silenciar o activar micrófono"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+s"
    )
    def script_toggleMute(self, gesture):
        """Silencia o activa el micrófono."""
        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "Mute"
            )

            if not button:

                ui.message(
                    _("Botón de activar o silenciar micrófono no encontrado")
                )

                return
            self.activateObject(
                button
            )

            tones.beep(
                800,
                80
            )

        except Exception:

            log.exception(
                "Error activando botón Mute"
            )

            ui.message(
                _("No fue posible cambiar el estado del micrófono")
            )

    @scriptHandler.script(
        description=_("Activar o desactivar compartir pantalla"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+p"
    )
    def script_toggleScreenShare(self, gesture):
        """Activa o desactiva compartir pantalla."""
        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "Screen"
            )

            if not button:

                ui.message(
                    _("Botón activar o desactivar compartir pantalla no encontrado")
                )

                return

            self.activateObject(
                button
            )

            tones.beep(
                950,
                60
            )

        except Exception:

            log.exception(
                "Error activando botón Screen"
            )

            ui.message(
                _("No fue posible activar compartir pantalla")
            )

    @scriptHandler.script(
        description=_("Activar o desactivar cámara"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+c"
    )
    def script_toggleCamera(self, gesture):
        """Activa o desactiva la cámara."""

        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "Camera"
            )

            if not button:

                ui.message(
                    _("Botón activar o desactivar cámara no encontrado")
                )

                return

            self.activateObject(
                button
            )

            tones.beep(
                1000,
                60
            )

        except Exception:

            log.exception(
                "Error activando botón Camera"
            )

            ui.message(
                _("No fue posible activar la cámara")
            )

    @scriptHandler.script(
        description=_("Abrir panel de reacciones"),
        category=_("Telegram Justi"),
        gesture="kb:alt+shift+e"
    )
    def script_openReactions(self, gesture):
        """Abre el panel de reacciones durante una llamada."""
        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "Emoji"
            )

            if not button:

                ui.message(
                    _("Botón abrir panel de reacciones no encontrado")
                )

                return

            self.activateObject(
                button
            )

            tones.beep(
                950,
                60
            )

        except Exception:

            log.exception(
                "Error activando botón Emoji"
            )

            ui.message(
                _("No fue posible abrir el panel de reacciones")
            )

    @scriptHandler.script(
        description=_("Adjuntar multimedia"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+a"
    )
    def script_attachMedia(self, gesture):
        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "ButtonAttach"
        )

        if not button:
            ui.message(
                _("Botón de adjuntar multimedia no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:

            log.exception(
                "Error activando ButtonAttach"
            )

            ui.message(
                _("No fue posible abrir el cuadro para adjuntar archivos")
            )

    @scriptHandler.script(
        description=_("Abrir archivo adjunto"),
        category=_("Telegram Justi"),
        gesture="kb:alt+o"
    )
    def script_openAttachment(self, gesture):
        """Abre el archivo adjunto."""

        try:

            focus = api.getFocusObject()

            if not focus:
                return

            if self.activateChildAutomationID(
                focus,
                "Button"
            ):

                tones.beep(900, 70)

                return

            ui.message(
                _("No se encontró un archivo adjunto")
            )
        except Exception:

            log.exception(
                "Error abriendo archivo adjunto"
            )

            ui.message(
                _("No fue posible abrir el archivo adjunto")
            )

    @scriptHandler.script(
        description=_("Descargar archivo adjunto"),
        category=_("Telegram Justi"),
        gesture="kb:alt+d"
    )
    def script_downloadAttachment(self, gesture):
        """Descarga el archivo adjunto."""
        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "Download"
            )

            if not button:

                ui.message(
                    _("Botón descargar archivo adjunto no encontrado")
                )

                return
            self.activateObject(
                button
            )

            tones.beep(
                950,
                80
            )

        except Exception:

            log.exception(
                "Error activando botón Download"
            )

            ui.message(
                _("No fue posible descargar el archivo")
            )

    @scriptHandler.script(
        description=_("Abrir nuevo chat"),
        category=_("Telegram Justi"),
        gesture="kb:control+n"
    )
    def script_newChat(self, gesture):
        """Abre la ventana nuevo chat."""

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "ComposeButton"
        )

        if not button:
            ui.message(
                _("Botón de nuevo chat no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:

            log.exception(
                "Error activando ComposeButton"
            )

            ui.message(
                _("No fue posible abrir un nuevo chat")
            )

    @scriptHandler.script(
        description=_("Ir al cuadro de mensaje"),
        category=_("Telegram Justi"),
        gesture="kb:alt+e"
    )
    def script_focusMessageEdit(self, gesture):
        """Enfoca el cuadro de mensaje."""

        fg = api.getForegroundObject()

        if not fg:
            return

        edit = self.findObjectByAutomationID(
            fg,
            "TextField"
        )

        if not edit:
            ui.message(
                _("Cuadro de edición de mensajes no encontrado")
            )
            return

        try:
            edit.setFocus()
            tones.beep(700, 80)

        except Exception:

            log.exception(
                "Error enfocando TextField"
            )

            ui.message(
                _("No fue posible enfocar el cuadro de edición de mensajes")
            )

    @scriptHandler.script(
        description=_("Abrir menú de navegación"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+m"
    )
    def script_openNavigationMenu(self, gesture):
        fg = api.getForegroundObject()

        if not fg:
            return

        button = self.findObjectByAutomationID(
            fg,
            "Photo"
        )

        if not button:
            ui.message(
                _("Botón abrir menú de navegación no encontrado")
            )
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:

            log.exception(
                "Error activando botón Photo"
            )

            ui.message(
                _("Botón del menú de navegación no encontrado")
            )

    @scriptHandler.script(
        description=_("Ir al último mensaje"),
        category=_("Telegram Justi"),
        gesture="kb:alt+end"
    )
    def script_goToLatestMessage(self, gesture):
        """Desplaza el chat hasta el mensaje más reciente."""
        try:

            fg = api.getForegroundObject()

            if not fg:
                return

            button = self.findObjectByAutomationID(
                fg,
                "MessagesButton"
            )

            if not button:

                ui.message(
                    _("Botón ir al último mensaje no encontrado")
                )

                return

            self.activateObject(
                button
            )

            tones.beep(
                850,
                80
            )

        except Exception:

            log.exception(
                "Error activando botón MessagesButton"
            )

            ui.message(
                _("No fue posible ir al último mensaje")
            )

    @scriptHandler.script(
        description=_("Abrir transcripción de voz"),
        category=_("Telegram Justi"),
        gesture="kb:alt+t"
    )
    def script_openVoiceTranscript(self, gesture):
        """Abre o cierra la transcripción del mensaje de voz."""
        try:

            fg = api.getForegroundObject()

            if not fg:
                return

            button = self.findObjectByAutomationID(
                fg,
                "Recognize"
            )

            if not button:

                ui.message(
                    _("Botón transcripción de voz no encontrado")
                )

                return
            self.activateObject(
                button
            )

            tones.beep(
                900,
                60
            )

        except Exception:

            log.exception(
                "Error activando botón Recognize"
            )

            ui.message(
                _("No fue posible abrir la transcripción de voz")
            )

    @scriptHandler.script(
        description=_("Abrir panel de emoji, stickers y GIF"),
        category=_("Telegram Justi"),
        gesture="kb:alt+g"
    )
    def script_openStickerPanel(self, gesture):
        """Abre el panel de emoji, stickers y GIF."""
        try:

            fg = api.getForegroundObject()

            button = self.findObjectByAutomationID(
                fg,
                "ButtonStickers"
            )

            if not button:

                ui.message(
                    _("No se encontró el panel de emoji, stickers y GIF")
                )

                return
            self.activateObject(
                button
            )

            tones.beep(
                900,
                60
            )

        except Exception:

            log.exception(
                "Error activando ButtonStickers"
            )

            ui.message(
                _("No fue posible abrir el panel de emoji, stickers y GIF")
            )

    @scriptHandler.script(
        description=_("Volver directamente a la lista de chats"),
        category=_("Telegram Justi"),
        gesture="kb:alt+leftArrow"
    )
    def script_backToChats(self, gesture):
        """Regresa directamente a la lista de chats."""

        fg = api.getForegroundObject()

        if not fg:
            return

        button = self.findObjectByAutomationID(
            fg,
            "BackButton"
        )

        if not button:
            ui.message(
                _("Botón volver a la lista de chats no encontrado")
            )
            return

        try:
            button.doAction()

            tones.beep(800, 80)

        except Exception:

            log.exception(
                "Error activando botón BackButton"
            )

            ui.message(
                _("No se pudo volver a la lista de chats")
            )

    # =========================================================
    # Gestos
    # =========================================================

