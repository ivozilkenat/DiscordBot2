#IPOS - Intelligent Piece of Script
import discord
from discord.app_commands import CommandTree
from command_groups.member_commands import MemberCommands
from command_groups.admin_commands import AdminCommands
from command_groups.fun_commands import FunCommands
from clients.data.guild import TargetGuild

class ClientIPOS(discord.Client):
	#todo: temporarily bot is only allowed on one guild at a time
	GUILD_ID = TargetGuild.GUILD_ID
	GUILD_OBJ = discord.Object(GUILD_ID) #todo: whats the difference to real guild obj

	def __init__(self):
		super().__init__(intents=discord.Intents.all())
		self.active_guild = None
		self.synced = False
		self.tree = CommandTree(self)

	async def on_ready(self):
		await self.wait_until_ready() #todo: necessary?
		self.active_guild = self.get_guild(self.GUILD_ID)
		# Init all command groups
		self.cogs = {
			MemberCommands(self),
			AdminCommands(self),
			FunCommands(self)
		}
		if not self.synced: #todo: synced condition necessary? <- called once, right?
			await self.tree.sync(guild=self.GUILD_OBJ)
			self.synced = True
		print(f"Login Successful as {self.user}")

	async def on_message(self, message: discord.Message):
		if message.author == self.user:
			return
		if isinstance(message.channel, discord.DMChannel):
			await message.author.send("Hello there! I'm sorry to inform you that I can only help you if you're calling me on a server :E")

	def get_role_obj(self, role: str):
		roles = self.active_guild.roles
		r: discord.Role = discord.utils.get(roles, name=role)
		assert r is not None, f"Role: '{role}' does not exist in guild: '{self.active_guild}'"
		return r