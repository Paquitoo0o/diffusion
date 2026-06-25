import os
import discord
from discord.ext import commands

# =====================
# INTENTS (IMPORTANT)
# =====================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =====================
# MEMOIRE PANIER
# =====================
carts = {}

# =====================
# BOUTONS PRODUIT
# =====================
class ProductView(discord.ui.View):
    def __init__(self, titre, prix, lien):
        super().__init__(timeout=None)
        self.titre = titre
        self.prix = prix
        self.lien = lien

    @discord.ui.button(label="🧺 Ajouter au panier", style=discord.ButtonStyle.green)
    async def add_cart(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = str(interaction.user.id)

        carts.setdefault(user_id, []).append({
            "titre": self.titre,
            "prix": self.prix,
            "lien": self.lien
        })

        await interaction.response.send_message("✅ Ajouté au panier", ephemeral=True)

    @discord.ui.button(label="🧺 Voir mon panier", style=discord.ButtonStyle.blurple)
    async def show_cart(self, interaction: discord.Interaction, button: discord.ui.Button):

        user_id = str(interaction.user.id)
        items = carts.get(user_id, [])

        if not items:
            await interaction.response.send_message("🧺 Ton panier est vide", ephemeral=True)
            return

        text = ""
        total = 0

        for i, item in enumerate(items, start=1):
            text += (
                f"📦 ARTICLE {i}\n"
                f"🛍 {item['titre']}\n"
                f"💰 {item['prix']}\n"
                f"🔗 {item['lien']}\n"
                f"──────────────────\n"
            )

            try:
                total += int(item['prix'].replace("€", ""))
            except:
                pass

        await interaction.response.send_message(
            f"🧺 TON PANIER\n\n{text}\n💰 TOTAL ~ {total}€",
            ephemeral=True
        )

# =====================
# COMMANDE POST
# =====================
@bot.command()
async def post(ctx, *, args):
    try:
        parts = [x.strip() for x in args.split("|")]

        titre = parts[0]
        prix = parts[1]
        lien = parts[2]
        image = parts[3] if len(parts) > 3 else None

        embed = discord.Embed(
            title=f"🛍 {titre}",
            description=f"💰 {prix}\n🔗 {lien}",
            color=0x00ff00
        )

        if image and image.startswith("http"):
            embed.set_image(url=image)

        await ctx.send(embed=embed, view=ProductView(titre, prix, lien))

    except Exception:
        await ctx.send("❌ Format: !post titre | prix | lien | image(optionnel)")

# =====================
# READY EVENT
# =====================
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

# =====================
# TOKEN SAFE (RENDER)
# =====================
token = os.getenv("TOKEN")

if not token:
    raise ValueError("TOKEN manquant dans Render")

bot.run(token)
