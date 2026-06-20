import discord
import os
from discord.ext import commands
from discord import app_commands

# ====== KONFIGURATION ======
TOKEN = os.environ["DISCORD_TOKEN"]     # wird in Railway als Umgebungsvariable gesetzt
MEMBER_ROLE_NAME = "Member"             # exakter Name deiner Member-Rolle
VERIFY_CHANNEL_NAME = "verify"          # Channel wo der Button gepostet wird
EMBED_TITLE = "Verifizierung"
EMBED_DESCRIPTION = "Klick auf den Button unten, um dich zu verifizieren und Zugriff auf den Server zu bekommen."
EMBED_COLOR = 0x2ecc71                  # grün, als hex
# ============================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Button bleibt für immer aktiv

    @discord.ui.button(label="Verifizieren", style=discord.ButtonStyle.success, emoji="✅", custom_id="verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, name=MEMBER_ROLE_NAME)

        if role is None:
            await interaction.response.send_message(
                "Fehler: Member-Rolle wurde nicht gefunden. Sag das einem Admin.",
                ephemeral=True
            )
            return

        if role in interaction.user.roles:
            await interaction.response.send_message(
                "Du bist bereits verifiziert.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "Verifiziert! Willkommen auf dem Server.",
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "Fehler: Bot hat keine Berechtigung, die Rolle zu vergeben. "
                "Stell sicher, dass die Bot-Rolle über der Member-Rolle steht.",
                ephemeral=True
            )


@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")
    bot.add_view(VerifyButton())  # macht Button auch nach Bot-Neustart klickbar
    print("Verify-Button ist aktiv.")


@bot.command()
@commands.has_permissions(administrator=True)
async def setupverify(ctx):
    """Postet die Verify-Nachricht im aktuellen Channel. Nur von Admins nutzbar."""
    embed = discord.Embed(
        title=EMBED_TITLE,
        description=EMBED_DESCRIPTION,
        color=EMBED_COLOR
    )
    await ctx.send(embed=embed, view=VerifyButton())
    await ctx.message.delete()  # löscht den !setupverify Befehl danach


bot.run(TOKEN)
