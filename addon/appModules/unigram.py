# -*- coding: utf-8 -*-

"""
Telegram Justi 1.0
Complemento NVDA para Telegram Unigram.

Autor:
Mauro Ocampo - JustiCode
"""

import time

import api
import tones
import ui
import wx
import appModuleHandler
import keyboardHandler
import logHandler
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

    def findObjectByName(self, obj, target):
        """
        """
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
            ui.message(
                "No se pudo cancelar la grabación"
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

            if focus:

                audioMessage = self.findObjectByAutomationID(
                    focus,
                    "Recognize"
                )

                if audioMessage:

                    try:

                        focus.doAction()

                        tones.beep(900, 50)

                        return

                    except Exception:
                        pass

                    playButton = self.findObjectByName(
                        focus,
                        "Reproducir"
                    )

                    if not playButton:

                        playButton = self.findObjectByName(
                            focus,
                            "Pausar"
                        )

                    if playButton:

                        self.activateObject(
                            playButton
                        )

                        tones.beep(900, 50)

                        return

        except Exception:
            log.exception(
                "Error reproduciendo audio"
            )

        gesture.send()

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
            ui.message("Perfil no encontrado")
            return

        try:
            button.doAction()
            tones.beep(900, 80)

        except Exception:
            ui.message("No se pudo abrir el perfil")

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
            ui.message("Llamar no encontrado")
            return

        try:
            button.doAction()
            tones.beep(1000, 80)

        except Exception:
            ui.message("No se pudo iniciar la llamada")

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
            ui.message("NO ENCONTRÉ VIDEOCALL")
            return

        try:
            button.doAction()
            tones.beep(1200, 100)

        except Exception:
            ui.message("ERROR VIDEOCALL")

    @scriptHandler.script(
        description=_("Finalizar llamada"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+n"
    )
    def script_endCall(self, gesture):
        """Finaliza una llamada."""

        fg = api.getForegroundObject()

        button = self.findObjectByName(
            fg,
            "finalizar"
        )

        if not button:
            ui.message("NO ENCONTRÉ FINALIZAR")
            return

        try:
            button.doAction()
            tones.beep(500, 80)

        except Exception:
            ui.message("ERROR FINALIZAR")

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
            ui.message("NO ENCONTRÉ BUTTONATTACH")
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:
            ui.message("ERROR BUTTONATTACH")

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
            ui.message("Botón nuevo chat no encontrado")
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:
            ui.message("No se pudo abrir nuevo chat")

    @scriptHandler.script(
        description=_("Ir al cuadro de mensaje"),
        category=_("Telegram Justi"),
        gesture="kb:alt+e"
    )
    def script_focusMessageEdit(self, gesture):
        """Enfoca el cuadro de mensaje."""

        fg = api.getForegroundObject()

        edit = self.findObjectByAutomationID(
            fg,
            "TextField"
        )

        if not edit:
            ui.message("Cuadro de mensaje no encontrado")
            return

        try:
            edit.setFocus()
            tones.beep(700, 80)

        except Exception:
            ui.message("No se pudo enfocar el cuadro de mensaje")

    @scriptHandler.script(
        description=_("Abrir menú de navegación"),
        category=_("Telegram Justi"),
        gesture="kb:control+shift+m"
    )
    def script_openNavigationMenu(self, gesture):
        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "Photo"
        )

        if not button:
            ui.message("Menú no encontrado")
            return

        try:
            button.doAction()
            tones.beep(700, 80)

        except Exception:
            ui.message("No se pudo abrir el menú")

    @scriptHandler.script(
        description=_("Volver directamente a la lista de chats"),
        category=_("Telegram Justi"),
        gesture="kb:alt+leftArrow"
    )
    def script_backToChats(self, gesture):
        """Regresa directamente a la lista de chats."""

        fg = api.getForegroundObject()

        button = self.findObjectByAutomationID(
            fg,
            "BackButton"
        )

        if not button:
            ui.message(_("Botón volver atrás no encontrado"))
            return

        try:
            button.doAction()

            tones.beep(800, 80)

        except Exception:
            ui.message(
                _("No se pudo volver a la lista de chats")
            )

    # =========================================================
    # Gestos
    # =========================================================

