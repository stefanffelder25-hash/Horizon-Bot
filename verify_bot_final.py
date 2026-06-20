import discord
from discord.ext import commands
from discord import app_commands

# ====== KONFIGURATION ======
TOKEN = "DEIN_BOT_TOKEN_HIER"          # aus dem Developer Portal
MEMBER_ROLE_NAME = "Member"             # exakter Name deiner Member-Rolle
EMBED_TITLE = "VERIFIZIERUNG ERFORDERLICH"
EMBED_DESCRIPTION = "Willkommen auf unserem Server! Verifiziere dich in 5 Sekunden und erhalte sofort Zugriff auf alle exklusiven Channels und Features."
EMBED_COLOR = 0x00d4ff                  # Cyan
# ============================

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Jetzt Verifizieren", style=discord.ButtonStyle.primary, emoji="✨", custom_id="verify_button")
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
                "Verifiziert! Willkommen auf dem Server. 🎉",
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
    bot.add_view(VerifyButton())
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
    
    # Features hinzufügen
    embed.add_field(
        name="⚡ Sofortzugriff",
        value="auf alle Community-Channels",
        inline=True
    )
    embed.add_field(
        name="🎮 Events & Spiele",
        value="mit anderen Membern",
        inline=True
    )
    embed.add_field(
        name="💬 Community-Chat",
        value="und Austausch",
        inline=True
    )
    embed.add_field(
        name="👑 Member-Status",
        value="mit Rolle",
        inline=True
    )
    
    # Info Cards
    embed.add_field(
        name="⏱️ Dauer",
        value="5 Sekunden",
        inline=True
    )
    embed.add_field(
        name="🔐 Sicherheit",
        value="Verifiziert",
        inline=True
    )
    
    embed.set_footer(text="→ Klick den Button unten um sofort zu starten")
    
    await ctx.send(embed=embed, view=VerifyButton())
    await ctx.message.delete()


bot.run(TOKEN)
