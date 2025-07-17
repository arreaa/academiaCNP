import discord

TOKEN = "MTMzNTYzNDI2NjI4MDY5Mzc3MA.GyewU7.f2UAPcIxbxtvWBw2V13iPlAmiK2JCsfHPFVsLc"
prefix = "a!"

# Canales
enviar_plantilla_channel_id = 1223935677171761162  # Canal donde los usuarios envían sus plantillas
por_corregir_channel_id = 1223935697153687582      # Canal donde se aprueban/rechazan las plantillas
resultados_channel_id = 1224101879760551956        # Canal de resultados (puedes eliminar si no lo usas)
registro_plantillas_channel_id = 1223935717005197313 # Canal de registro de plantillas
solicitudes_oposiciones_channel_id = 1394012201328840775  # Canal para solicitudes de oposiciones
oposiciones_channel_id = 1394012232815214642  # Canal donde se publican oposiciones aprobadas

# Roles
rol_aceptada_id = 1223947156873023548
rol_rechazada_1_id = 1223947188304875593
rol_rechazada_2_id = 1223947229216243773
rol_policia_nacional_id = 1394022059880743082  # ID del rol Policía Nacional
rol_sin_plantilla_id = 1224326269106262097  # ID del rol Sin Plantilla

motivos_rechazo = [
    ("Falta información", "La plantilla no contiene toda la información requerida."),
    ("Formato incorrecto", "El formato de la plantilla no es válido."),
    ("No cumple requisitos", "La plantilla no cumple los requisitos mínimos."),
    ("Otro", "Otro motivo.")
]

# Mensajes y textos editables
MENSAJE_PLANTILLA_ACEPTADA_TITULO = "PLANTILLA  ACEPTADA"
MENSAJE_PLANTILLA_ACEPTADA_DESCRIPCION = "¡Tu plantilla ha sido **aprobada**!\n\nRecuerda estudiar todo lo necesario para entrar al cuerpo.\n\nMucha suerte."
MENSAJE_PLANTILLA_ACEPTADA_COLOR = 0x00ff00
MENSAJE_PLANTILLA_ACEPTADA_FOOTER = ""

MENSAJE_PLANTILLA_RECHAZADA_TITULO = "PLANTILLA RECHAZADA"
MENSAJE_PLANTILLA_RECHAZADA_DESCRIPCION = "Tu plantilla ha sido **rechazada**.\n\nTe quedan {intentos} intentos.\n\nMotivo: {motivo}"
MENSAJE_PLANTILLA_RECHAZADA_COLOR = 0xff0000
MENSAJE_PLANTILLA_RECHAZADA_FOOTER = ""

MENSAJE_CONVOCATORIA_TITULO = "CONVOCATORIA OFICIAL DE OPOSICIONES A LA POLICÍA NACIONAL"
MENSAJE_CONVOCATORIA_COLOR = 0x3498db
MENSAJE_CONVOCATORIA_FOOTER = "Oposiciones convocadas por: {convocante} | Autorizadas por: {autorizador}"

MENSAJE_CONVOCATORIA_TXT_PATH = "convocatoria_oposiciones.txt"

MENSAJE_SOLICITUD_OPOSICIONES_TITULO = "Solicitud de Oposiciones"
MENSAJE_SOLICITUD_OPOSICIONES_COLOR = 0x3498db
MENSAJE_SOLICITUD_OPOSICIONES_FOOTER = ""

MENSAJE_APROBAR_POLICIA = "{usuario} ha sido aprobado y ahora es Policía Nacional."
MENSAJE_ERROR_ROL_POLICIA = "No se encontró el rol de Policía Nacional. Revisa el ID en settings.py."
MENSAJE_ERROR_ROL = "Algún rol no existe en el servidor. Revisa los IDs en settings.py."
MENSAJE_ERROR_USUARIO = "No se encontró al usuario para asignar roles."
MENSAJE_SOLICITUD_ENVIADA = "Solicitud enviada correctamente."
MENSAJE_SOLICITUD_NO_CANAL = "No se encontró el canal de solicitudes."
MENSAJE_OPOSICION_APROBADA = "Oposición aprobada y publicada."
MENSAJE_OPOSICION_RECHAZADA = "Motivo enviado al solicitante."
MENSAJE_PLANTILLA_APROBADA = "Plantilla aprobada y rol asignado."
MENSAJE_PLANTILLA_RECHAZADA = "Motivo registrado: {motivo}"