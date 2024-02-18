import disnake
from disnake.ext import commands
from cfg.cfg import *


class Report(disnake.ui.Modal):
    def __init__(self, chose):
        self.chose = chose
        components = [
            disnake.ui.TextInput(
                label="Project",
                placeholder=" tell us about your project",
                custom_id="Project",
                max_length=50
            ),
            disnake.ui.TextInput(
                label="Map size",
                placeholder="what is the approximate map size?",
                custom_id='Map',
                max_length=50
            ),
        ]
        super().__init__(title="New Order", components=components)

    async def callback(self, inter: disnake.ModalInteraction,):
        await inter.response.send_message('wait for a response', ephemeral=True)
        try:
            embed = disnake.Embed(title="``New job:``",
                                  description=self.chose,
                                  color=disnake.Color.blurple())
            for key, value in inter.text_values.items():
                embed.add_field(
                    name=key.capitalize(),
                    value=value[:1024],
                    inline=False,
                )
            channel = await inter.guild.create_text_channel(f'💇| {inter.user.name}',
                                                                  category=disnake.utils.get(
                                                                      inter.guild.categories,
                                                                      id=1206569549026295808))
            await channel.set_permissions(inter.guild.get_role(inter.guild.id),
                                          send_messages=False,
                                          read_messages=True)
            await channel.send(embed=embed)
        except (Exception) as error:
            print(error)


class SelectChosee(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(
                label="$0-$20",
                description="Budget",
            ),
            disnake.SelectOption(
                label="$20-$100",
                description="Budget"
            ),
            disnake.SelectOption(
                label="$100-$200",
                description="Budget"
            ),
            disnake.SelectOption(
                label="$200-$500",
                description="Budget"
            ),
            disnake.SelectOption(
                label="$500+",
                description="Budget"
            )
        ]
        super().__init__(
            placeholder="📃 Select budget",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        chose = self.values[0]
        modal = Report
        await inter.response.send_modal(modal=modal(chose))


class DropDownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectChosee())

class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Open new order', style=disnake.ButtonStyle.red, emoji='📕')
    async def button(self, button: disnake.ui.Button, inter):
        view = DropDownView()
        await inter.response.send_message(view=view, ephemeral=True)


class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Ticket is Load')

    @commands.slash_command(guild_ids=[guild])
    @commands.has_permissions(administrator=True)
    async def ticket(self, inter: disnake.ApplicationCommandInteraction):
        view = ButtonView()
        await inter.response.send_message(view=view)


def setup(bot: commands.Bot):
    bot.add_cog(Ticket(bot))