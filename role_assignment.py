import nextcord
from nextcord.ext import commands
import sqlite3

class RoleAssignment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Connect to the database
        self.conn = sqlite3.connect('roles.db')
        self.c = self.conn.cursor()

        # Create the table if it doesn't exist
        self.c.execute('''CREATE TABLE IF NOT EXISTS role_assignment
             (server_id INTEGER, role_id INTEGER)''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get role data from the database
        self.c.execute('SELECT role_id FROM role_assignment WHERE server_id=?', (member.guild.id,))
        role_id = self.c.fetchone()

        if role_id:
            role = nextcord.utils.get(member.guild.roles, id=role_id[0])
            await member.add_roles(role)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def setrole(self, ctx, role_id):
        """
        `.setrole <Role id>`
        """
        role_id = int(role_id)

        # Write/update role data in the database
        self.c.execute('INSERT OR REPLACE INTO role_assignment (server_id, role_id) VALUES (?, ?)', (ctx.guild.id, role_id))
        self.conn.commit()

        await ctx.send(f'Role set to <@&{role_id}>')

def setup(bot):
    bot.add_cog(RoleAssignment(bot))
