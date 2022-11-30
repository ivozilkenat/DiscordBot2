import discord
from discord.app_commands import Choice, choices, describe, check
from discord.app_commands.checks import has_role, has_permissions
from command_groups._core.c_group_frame import CGroup
from clients.data.guild import TargetGuild

class AdminCommands(CGroup):
	#-----------[Command Group Config]-----------------------------
	GROUP_DESCRIPTION = "A collection of admin commands"
	GROUP_NAME = "admin"
	GROUP_USE_ROLE = TargetGuild.ServerRoles.Gott.value #todo: must be changed accordingly / allow for tuple entry and permission addition

	#-----------[Init]---------------------------------------------
	def __init__(self, client):
		super().__init__(client)
	#-----------[Commands]-----------------------------------------

	async def command_test(self, ctx: discord.Interaction):
		await ctx.response.send_message("Penise: 3== 3== 3==")
