import json
import os

from settings import *

import discord
from discord.ext import commands
from discord import ui, ButtonStyle, Embed, Interaction
from discord import app_commands

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix=prefix)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} ({bot.user.id})')
    print('-')
    print('Conectado a los siguientes servidores:')
    await bot.tree.sync()  # Sincronizar los comandos de la aplicación
    print('-')
    print('Comandos de la aplicación sincronizados.')
        
class AprobacionView(ui.View):
    def __init__(self, autor_id):
        super().__init__(timeout=None)
        self.autor_id = autor_id

    @ui.button(label="Aprobado", style=ButtonStyle.success, custom_id="aprobado_btn")
    async def aprobado(self, interaction: Interaction, button: ui.Button):
        await handle_aprobado(interaction, self.autor_id)

    @ui.button(label="Suspendido", style=ButtonStyle.danger, custom_id="suspendido_btn")
    async def suspendido(self, interaction: Interaction, button: ui.Button):
        await handle_suspendido(interaction, self.autor_id)

class MotivoRechazoModal(ui.Modal, title="Motivo del rechazo"):
    motivo = ui.TextInput(label="Motivo", style=discord.TextStyle.paragraph, placeholder="Escribe el motivo del rechazo aquí...")
    def __init__(self, autor_id):
        super().__init__()
        self.autor_id = autor_id
    async def on_submit(self, interaction: Interaction):
        await handle_motivo_rechazo(interaction, self.autor_id, self.motivo.value)

class SolicitarOposicionesView(ui.View):
    def __init__(self, user_id, fecha, hora):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.fecha = fecha
        self.hora = hora

    @ui.button(label="Aprobar", style=ButtonStyle.success, custom_id="aprobar_oposicion_btn")
    async def aprobar(self, interaction: Interaction, button: ui.Button):
        await handle_aprobar_oposicion(interaction, self.user_id, self.fecha, self.hora)

    @ui.button(label="Rechazar", style=ButtonStyle.danger, custom_id="rechazar_oposicion_btn")
    async def rechazar(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_modal(MotivoRechazoOposicionModal(self.user_id))

class MotivoRechazoOposicionModal(ui.Modal, title="Motivo del rechazo"):
    motivo = ui.TextInput(label="Motivo", style=discord.TextStyle.paragraph, placeholder="Escribe el motivo del rechazo aquí...")
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
    async def on_submit(self, interaction: Interaction):
        await handle_rechazar_oposicion(interaction, self.user_id, self.motivo.value)

@bot.tree.command(name="solicitar_oposiciones", description="Solicita oposiciones")
@app_commands.describe(fecha="Fecha de la oposición", hora="Hora de la oposición")
async def solicitar_oposiciones(interaction: Interaction, fecha: str, hora: str):
    embed = Embed(title="Solicitud de Oposiciones", color=0x3498db)
    embed.add_field(name="Nombre del agente", value=interaction.user.mention, inline=False)
    embed.add_field(name="Fecha", value=fecha, inline=True)
    embed.add_field(name="Hora", value=hora, inline=True)
    view = SolicitarOposicionesView(interaction.user.id, fecha, hora)
    canal_solicitudes = interaction.guild.get_channel(solicitudes_oposiciones_channel_id)
    if canal_solicitudes:
        await canal_solicitudes.send(embed=embed, view=view)
        await interaction.response.send_message("Solicitud enviada correctamente.", ephemeral=True)
    else:
        await interaction.response.send_message("No se encontró el canal de solicitudes.", ephemeral=True)

async def handle_aprobado(interaction, autor_id):
    guild = interaction.guild
    member = guild.get_member(autor_id)
    rol_aceptada = guild.get_role(rol_aceptada_id)
    rol_rechazada_1 = guild.get_role(rol_rechazada_1_id)
    rol_rechazada_2 = guild.get_role(rol_rechazada_2_id)
    rol_sin_plantilla = guild.get_role(rol_sin_plantilla_id)
    color_embed = MENSAJE_PLANTILLA_ACEPTADA_COLOR
    if member:
        if rol_aceptada:
            await member.add_roles(rol_aceptada)
        if rol_rechazada_1 and rol_rechazada_1 in member.roles:
            await member.remove_roles(rol_rechazada_1)
        if rol_sin_plantilla and rol_sin_plantilla in member.roles:
            await member.remove_roles(rol_sin_plantilla)
    else:
        await interaction.response.send_message(MENSAJE_ERROR_USUARIO, ephemeral=True)
        return
    if not rol_aceptada or not rol_rechazada_1 or not rol_sin_plantilla:
        await interaction.response.send_message(MENSAJE_ERROR_ROL, ephemeral=True)
        return
    try:
        await interaction.message.delete()
    except Exception as e:
        print(f"No se pudo eliminar el mensaje: {e}")
    embed = Embed(title=MENSAJE_PLANTILLA_ACEPTADA_TITULO, color=color_embed)
    embed.description = MENSAJE_PLANTILLA_ACEPTADA_DESCRIPCION
    if MENSAJE_PLANTILLA_ACEPTADA_FOOTER:
        embed.set_footer(text=MENSAJE_PLANTILLA_ACEPTADA_FOOTER)
    canal_resultados = guild.get_channel(resultados_channel_id)
    if canal_resultados:
        await canal_resultados.send(f"{member.mention}", embed=embed)
        await member.send(embed=embed)
    canal_registro = guild.get_channel(registro_plantillas_channel_id)
    if canal_registro:
        embed_registro = Embed(title="Registro de Plantilla", color=MENSAJE_PLANTILLA_ACEPTADA_COLOR)
        embed_registro.add_field(name="Plantilla", value=interaction.message.content, inline=False)
        embed_registro.add_field(name="Usuario", value=member.mention, inline=True)
        embed_registro.add_field(name="Corregido por", value=interaction.user.mention, inline=True)
        embed_registro.add_field(name="Estado", value="Aceptada", inline=True)
        await canal_registro.send(embed=embed_registro)
    await interaction.response.send_message(MENSAJE_PLANTILLA_APROBADA, ephemeral=True)

async def handle_suspendido(interaction, autor_id):
    guild = interaction.guild
    member = guild.get_member(autor_id)
    rol_aceptada = guild.get_role(rol_aceptada_id)
    rol_rechazada_1 = guild.get_role(rol_rechazada_1_id)
    rol_rechazada_2 = guild.get_role(rol_rechazada_2_id)
    rol_sin_plantilla = guild.get_role(rol_sin_plantilla_id)

    if not member:
        await interaction.response.send_message("No se encontró al usuario en el servidor.", ephemeral=True)
        return

    if rol_sin_plantilla and rol_sin_plantilla in member.roles:
        await member.remove_roles(rol_sin_plantilla)
        await member.add_roles(rol_rechazada_1)
        await interaction.response.send_modal(MotivoRechazoModal(autor_id))
        return
    elif rol_rechazada_1 and rol_rechazada_1 in member.roles:
        await member.remove_roles(rol_rechazada_1)
        await member.add_roles(rol_rechazada_2)
        await interaction.response.send_modal(MotivoRechazoModal(autor_id))
        return
    elif rol_rechazada_2 and rol_rechazada_2 in member.roles:
        await interaction.response.send_message("El usuario no posee más intentos.", ephemeral=True)
        return

    # Si el usuario no tiene ninguno de los roles esperados
    await interaction.response.send_message("El usuario no tiene ningún rol de plantilla para suspender.", ephemeral=True)
    return
    
async def handle_motivo_rechazo(interaction, autor_id, motivo):
    guild = interaction.guild
    member = guild.get_member(autor_id)
    rol_aceptada = guild.get_role(rol_aceptada_id)
    rol_rechazada_1 = guild.get_role(rol_rechazada_1_id)
    rol_rechazada_2 = guild.get_role(rol_rechazada_2_id)
    resultados = guild.get_channel(resultados_channel_id)
    registro = guild.get_channel(registro_plantillas_channel_id)
    rol_sin_plantilla = guild.get_role(rol_sin_plantilla_id)
    color_embed = MENSAJE_PLANTILLA_RECHAZADA_COLOR
    if member not in guild.members:
        await interaction.response.send_message(MENSAJE_ERROR_USUARIO, ephemeral=True)
        return
    if rol_rechazada_1 in member.roles:
        intentos_restantes = 1
        embed = Embed(title=MENSAJE_PLANTILLA_RECHAZADA_TITULO, description=MENSAJE_PLANTILLA_RECHAZADA_DESCRIPCION.format(intentos=intentos_restantes, motivo=motivo), color=MENSAJE_PLANTILLA_RECHAZADA_COLOR)
        if MENSAJE_PLANTILLA_RECHAZADA_FOOTER:
            embed.set_footer(text=MENSAJE_PLANTILLA_RECHAZADA_FOOTER)
        await member.send(embed=embed)
        await resultados.send(f'{member.mention}')
        await resultados.send(embed=embed)
    elif rol_rechazada_2 in member.roles:
        intentos_restantes = 0
        embed = Embed(title=MENSAJE_PLANTILLA_RECHAZADA_TITULO, description=MENSAJE_PLANTILLA_RECHAZADA_DESCRIPCION.format(intentos=intentos_restantes, motivo=motivo)+"\nRecuerde que para volver a presentarse deberá realizarse CK.", color=MENSAJE_PLANTILLA_RECHAZADA_COLOR)
        if MENSAJE_PLANTILLA_RECHAZADA_FOOTER:
            embed.set_footer(text=MENSAJE_PLANTILLA_RECHAZADA_FOOTER)
        await member.send(embed=embed)
        await resultados.send(f'{member.mention}')
        await resultados.send(embed=embed)
    if registro:
        embed_registro = Embed(title="Registro de Plantilla", color=MENSAJE_PLANTILLA_RECHAZADA_COLOR)
        embed_registro.add_field(name="Plantilla", value=interaction.message.content, inline=False)
        embed_registro.add_field(name="Usuario", value=member.mention, inline=True)
        embed_registro.add_field(name="Corregido por", value=interaction.user.mention, inline=True)
        embed_registro.add_field(name="Estado", value="Rechazada", inline=True)
        await registro.send(embed=embed_registro)
    try:
        await interaction.message.delete()
    except Exception as e:
        print(f"No se pudo eliminar el mensaje: {e}")
    


async def handle_aprobar_oposicion(interaction, user_id, fecha, hora):
    guild = interaction.guild
    user = guild.get_member(user_id)
    canal_oposiciones = guild.get_channel(oposiciones_channel_id)
    if canal_oposiciones:
        async for msg in canal_oposiciones.history(limit=1):
            try:
                await msg.delete()
            except Exception:
                pass
        with open(MENSAJE_CONVOCATORIA_TXT_PATH, "r", encoding="utf-8") as f:
            texto = f.read().replace("{fecha}", fecha).replace("{hora}", hora)
        embed = Embed(title=MENSAJE_CONVOCATORIA_TITULO, description=texto, color=MENSAJE_CONVOCATORIA_COLOR)
        convocante = user.display_name if user else "Desconocido"
        autorizador = interaction.user.display_name if interaction.user else "Desconocido"
        embed.set_footer(text=MENSAJE_CONVOCATORIA_FOOTER.format(convocante=convocante, autorizador=autorizador))
        await canal_oposiciones.send(embed=embed)
    try:
        await interaction.message.delete()
    except Exception:
        pass
    await interaction.response.send_message(MENSAJE_OPOSICION_APROBADA, ephemeral=True)

async def handle_rechazar_oposicion(interaction, user_id, motivo):
    guild = interaction.guild
    user = guild.get_member(user_id)
    if user:
        try:
            await user.send(f"Tu solicitud de oposiciones ha sido rechazada. Motivo: {motivo}")
        except Exception:
            pass
    try:
        await interaction.message.delete()
    except Exception:
        pass
    await interaction.response.send_message(MENSAJE_OPOSICION_RECHAZADA, ephemeral=True)

@bot.tree.command(name="aprobar_oposicion", description="Aprueba a un agente y le asigna el rol de Policía Nacional")
@app_commands.describe(usuario="Usuario a aprobar")
async def aprobar_oposicion(interaction: Interaction, usuario: discord.Member):
    roles_a_quitar = [r for r in usuario.roles if r.id != interaction.guild.id]
    try:
        await usuario.remove_roles(*roles_a_quitar)
    except Exception:
        pass
    rol_policia = interaction.guild.get_role(rol_policia_nacional_id)
    if rol_policia:
        await usuario.add_roles(rol_policia)
        await interaction.response.send_message(MENSAJE_APROBAR_POLICIA.format(usuario=usuario.mention), ephemeral=True)
    else:
        await interaction.response.send_message(MENSAJE_ERROR_ROL_POLICIA, ephemeral=True)

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Comandos de la aplicación sincronizados.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == enviar_plantilla_channel_id:
        target_channel = bot.get_channel(por_corregir_channel_id)
        if target_channel:
            view = AprobacionView(message.author.id)
            await target_channel.send(f"{message.author.display_name}: {message.content}", view=view)
        else:
            print(f"No se encontró el canal de destino con ID {por_corregir_channel_id}")
    await bot.process_commands(message)

bot.run(TOKEN)

