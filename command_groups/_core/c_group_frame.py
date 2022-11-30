import discord
from discord.app_commands import Group, Command, CommandInvokeError
from abc import ABC

from typing import Set

#Super Command-Group Class
class CGroup(ABC):
	GROUP_DESCRIPTION: str = None
	GROUP_NAME: str = None
	# Roles can have same permissions! (Be careful to make every role more powerful than @everyone)
	GROUP_USE_ROLE: str = None # if None use default permissions / role is always searched for on active guild
	_GROUP_DEFAULT_PERMISSIONS = discord.Permissions() #todo: role -> permissions # is there an easier solution only requiring roles?
	_COMMAND_METH_KEYWORD = "command_"

	def __init__(self, client): #: MyClient #todo: allow for type annotation
		if self.GROUP_DESCRIPTION is None:
			raise ValueError(f"'GROUP_DESCRIPTION' of class '{self.__class__.__name__}' must be set")
		self._attached = False
		self.client = client
		self.group = Group(
			name=self.__class__.__name__.lower() if self.GROUP_NAME is None else self.GROUP_NAME.lower(),
			description=self.GROUP_DESCRIPTION,
			default_permissions=
			self._GROUP_DEFAULT_PERMISSIONS
			if self.GROUP_USE_ROLE is None
			else self.client.get_role_obj(self.GROUP_USE_ROLE).permissions
		)
		self._setup_commands()
		self.attach_group()

	def _setup_commands(self):
		# Automagically setup all commands
		self.class_commands: Set[callable] = set()
		for i in dir(self.__class__):
			if i.startswith(self._COMMAND_METH_KEYWORD) and callable((d_attr := getattr(self.__class__, i))):
				self.class_commands.add(d_attr)

		for c in self.class_commands:
			self._create_command(coroutine=c, name=c.__name__.split(self._COMMAND_METH_KEYWORD)[1])

	def _create_command(self, coroutine, name=None, description=None):
		if name is None:
			name = coroutine.__name__[:32]
		if description is None:
			if (d := coroutine.__doc__) is None:
				description = "[NO DESCRIPTION PROVIDED]" #todo: outsource strings
			else:
				description = d[:100] # len(description) <= 100

		c = Command(name=name, description=description, callback=coroutine)
		c.binding = self #todo: why must binding be set manually?

		c.error(generalBotErrorHandler) #todo: smart idea?
		self.group.add_command(c)
		return c

	def attach_group(self):

		if not self._attached:
			self.client.tree.add_command(self.group, guild=self.client.GUILD_OBJ)


class InvalidCommandArgumentValue(discord.DiscordException):
	def __init__(self, msg=None):
		self.msg = f"An invalid command argument was provided!" if msg is None else msg
		super().__init__(self.msg)


async def generalBotErrorHandler(binder, ctx: discord.Interaction, error: discord.DiscordException):

	if not isinstance(error, discord.DiscordException):
		raise RuntimeError(f"A non discord related exception was thrown: {error}") # critical error
	if type(error) in (
		discord.app_commands.MissingPermissions,
		discord.app_commands.MissingRole
	):
		await ctx.response.send_message(error)
	elif type(error) == CommandInvokeError:
		await ctx.response.send_message(error.original)
	else:
		await ctx.response.send_message(f"An unhandled exception occurred: {error}")
		#print(f"An unhandled exception occurred: {error}")
		raise error



#todo: prettyfie strings
#todo: how to create subcommand groups? -> make group creation easier
#todo: toggle command response visibility
#todo: mark error