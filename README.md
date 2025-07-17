# 🤖 Bot Discord Policía Nacional - Gestión de Plantillas y Oposiciones

¡Bienvenido! Este bot está diseñado para gestionar plantillas y oposiciones de la Policía Nacional en servidores de Discord de forma intuitiva, visual y totalmente configurable.

## 🚀 Características principales

- **Reenvío de plantillas** entre canales con botones de aprobación/rechazo.
- **Gestión de roles** automática según el estado de la plantilla (aceptada, rechazada 1/2, rechazada 2/2, sin plantilla, policía nacional).
- **Registro de acciones** en canales específicos con mensajes y embeds personalizados.
- **Motivos de rechazo** editables y con opción de escribir manualmente.
- **Solicitudes y convocatorias de oposiciones** con fecha/hora y botones de gestión.
- **Textos, colores y variables** totalmente editables desde `settings.py`.
- **Eliminación automática** de mensajes y roles según el flujo.
- **Sin menciones a roles** en anuncios, solo al usuario.

---

## 🛠️ Instalación y configuración

1. **Clona o descarga** este repositorio en tu equipo.
2. Instala las dependencias necesarias:
   ```bash
   pip install -U discord.py
   ```
3. Edita el archivo `settings.py`:
   - Añade tu `TOKEN` de bot de Discord.
   - Configura los IDs de canales y roles según tu servidor.
   - Personaliza textos, colores y mensajes a tu gusto.
4. (Opcional) Edita el mensaje de convocatoria en `convocatoria_oposiciones.txt`.

---

## 📝 Uso básico

- Los usuarios envían sus plantillas en el canal configurado.
- El bot reenvía la plantilla al canal de corrección con botones para aprobar o suspender.
- Al aprobar/rechazar, el bot gestiona roles, envía mensajes y registra la acción.
- Los motivos de rechazo pueden ser seleccionados o escritos manualmente.
- El comando `/solicitar_oposiciones` permite a los usuarios solicitar oposiciones con fecha y hora.
- El comando `/aprobar_oposicion` aprueba a un usuario y le asigna el rol de Policía Nacional.

---

## ⚙️ Personalización

Todo lo editable está en `settings.py`:
- **IDs de canales y roles**
- **Textos de embeds y mensajes**
- **Colores de embeds**
- **Mensajes de error y éxito**

---

## 📂 Estructura del proyecto

```
Bot.Discord_Rol/
├── main.py                  # Lógica principal del bot
├── settings.py              # Configuración editable
├── convocatoria_oposiciones.txt # Mensaje editable de convocatoria
├── data/
│   └── data.json            # (Opcional) Datos persistentes
└── README.md                # (Este archivo)
```

---

## 🧑‍💻 Créditos y soporte

Desarrollado por Iñigo Arredondo.

¿Dudas o sugerencias? ¡Abre un issue o contacta al desarrollador!

---

¡Disfruta de tu bot de gestión policial en Discord! 🚓
