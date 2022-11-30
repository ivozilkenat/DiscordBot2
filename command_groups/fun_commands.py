import discord
from discord.app_commands import Choice, choices, describe, check
from discord.app_commands.checks import has_role, has_permissions
from command_groups._core.c_group_frame import CGroup, InvalidCommandArgumentValue
from random import randint
from clients.data.guild import TargetGuild

class FunCommands(CGroup):
	# -----------[Command Group Config]-----------------------------
	GROUP_DESCRIPTION = "Commands just for fun"
	GROUP_NAME = "fun"
	GROUP_USE_ROLE = TargetGuild.ServerRoles.Student.value  # todo: must be changed accordingly / allow for tuple entry and permission addition

	# -----------[Init]---------------------------------------------
	def __init__(self, client):
		super().__init__(client)

	# -----------[Commands]-----------------------------------------

	@choices(die=[
		Choice(name="d4", value=4),
		Choice(name="d6", value=6),
		Choice(name="d8", value=8),
		Choice(name="d10", value=10),
		Choice(name="d12", value=12),
		Choice(name="d20", value=20),
		Choice(name="d100", value=100),
	])
	async def command_role_dice(self, ctx: discord.Interaction, die: Choice[int]):
		result = randint(1, die.value)
		if die.value == 20 and result in (1, 20):
			if result == 20:
				response = f"You rolled a **NATURAL TWENTY** 🎉🎉"
			else:
				response = f"You rolled a **NATURAL ONE** 🤣"
		else:
			response = f"You rolled a **{result}**"

		await ctx.response.send_message(response)

	# Add better parameter check!
	async def command_role_ndice(self, ctx: discord.Interaction, d: int):
		if d < 1:
			raise InvalidCommandArgumentValue("The selected die must have at least 1 side")
		await ctx.response.send_message(f"You rolled a **{randint(1, d)}**")



