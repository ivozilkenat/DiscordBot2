import discord
from discord.app_commands import Choice, choices, describe, check
from discord.app_commands.checks import has_role, has_permissions
from command_groups._core.c_group_frame import CGroup
from random import randint
from clients.data.guild import TargetGuild
from discord import ui

class MemberCommands(CGroup):
	#-----------[Command Group Config]-----------------------------
	GROUP_DESCRIPTION = "General discord user utility commands"
	GROUP_NAME = "member" #todo: use shortcut like 'm' instead?
	GROUP_USE_ROLE = TargetGuild.ServerRoles.Student.value #todo: must be changed accordingly / allow for tuple entry and permission addition

	#-----------[Init]---------------------------------------------
	def __init__(self, client):
		super().__init__(client)
	#-----------[Commands]-----------------------------------------

	@has_role("Gott")
	#@check()
	#@has_permissions(manage_roles=True)
	#@describe(color="colors to choose from")
	@choices(color=[
		Choice(name="red", value=1),
		Choice(name="green", value=2),
		Choice(name="blue", value=3),
	])
	async def command_test(self, ctx: discord.Interaction, name: discord.Member, color: Choice[int]):
		"""
		This function exists for testing purposes!
		"""
		await ctx.response.send_message("this is a test: {} chose {}".format(name, color.name))

	#@autocomplete(name=missing_role_autocomplete) #todo: autocomplete seems to be not working with members
	async def command_add_student22(self, ctx: discord.Interaction, name: discord.Member):
		if TargetGuild.ServerRoles.Student.value in [r.name for r in name.roles]:
			await ctx.response.send_message(f"User '{name}' already had role '{TargetGuild.ServerRoles.Student.value}'!")
		else:
			await name.add_roles(self.client.get_role_obj(TargetGuild.ServerRoles.Student.value)) #todo: make cleaner
			await ctx.response.send_message(f"Successfully added role '{TargetGuild.ServerRoles.Student.value}' to user '{name}'!")

	async def command_remove_student22(self, ctx: discord.Interaction, name: discord.Member):
		pass

	@choices(duration=[
		Choice(name="30 Seconds", value=30),
		Choice(name="2 Minutes", value=120),
		Choice(name="5 Minutes", value=300),
		Choice(name="15 Minutes", value=900),
	])
	async def command_binary_poll(self, ctx: discord.Interaction, poll_question: str, duration: Choice[int]):
		yes_button = ui.Button(label="Yes", style=discord.ButtonStyle.red)
		no_button = ui.Button(label="No", style=discord.ButtonStyle.green)
		view = ui.View()
		view.add_item(yes_button)
		view.add_item(no_button)

		await ctx.response.send_message(f"{str(ctx.user).split('#')[0]} has started a poll:	{poll_question}\n Vote Now!", view = view)