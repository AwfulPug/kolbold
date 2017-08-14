import discord
import random
import re
from discord.ext import commands as kobold

class Basic:

    def __init__(self,kobold):
        self.kobold = kobold

    @kobold.command(pass_context=True)
    async def hello(self,ctx):
        """Hello : .kobold greets the user that calls the command."""
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.title = "Greetings"
        embed.add_field(name="Greeting", value="Hello " + ctx.message.author.mention + ", how are you today?")
        await self.kobold.say(embed=embed)
 #       await self.kobold.say("Hello " + ctx.message.author.mention + ", how are you today?")

    @kobold.command(pass_context=True)
    async def roll(self,ctx,dice:str="1d4",bonus:str="0"):
        """Roll : rolls a dice type the user inputs in a 1d4 format
           and adds/subtracts bonuses from the roll.Prints out into
           the text channel the command was invoked. Default die is
           1d4 and bonus default is 0."""
        r = Dice(dice,bonus)
        r.add_dice()
        if r.faces == 20:
            await  self.kobold.say(ctx.message.author.mention + "```" + "\nDice type: d" + str(r.faces) +
                      "\nAmount of rolls: " + str(r.rolls) + "\nCrit success(es): " + str(r.crit_success) +
                      "\nCrit failure(s): " + str(r.crit_fail) + "\nBonus: " + bonus + "\nTotal: " + str(r.total_amount) + "```")
        else:
            await  self.kobold.say(ctx.message.author.mention + "```" + "\nDice type: d" + str(r.faces) +
                                   "\nAmount of rolls: " + str(r.rolls) + "\nBonus: " + bonus + "\nTotal: " + str(r.total_amount) + "```")

    @kobold.command(pass_context=True)
    async def dmroll(self,ctx,dice:str="1d4",bonus:str="0"):
        """Dmroll : rolls a dice type the user inputs in a 1d4 format
           and adds/subtracts bonuses from the roll and send the result
           directly to the user. Perfect for behind the screen rolls.
           Default die is 1d4 and bonus default is 0."""
        user = ctx.message.author
        r = Dice(dice, bonus)
        r.add_dice()
        if r.faces == 20:
            await self.kobold.send_message(user,"```" + "\nDice type: d" + str(r.faces) +
                                   "\nAmount of rolls: " + str(r.rolls) + "\nCrit success(es): " + str(r.crit_success) +
                                   "\nCrit failure(s): " + str(r.crit_fail) + "\nBonus: " + bonus + "\nTotal: " + str(r.total_amount) + "```")
        else:
            await self.kobold.send_message(user,"```" + "\nDice type: d" + str(r.faces) +
                                  "\nAmount of rolls: " + str(r.rolls) + "\nBonus: " + bonus + "\nTotal: " + str(r.total_amount) + "```")

    @kobold.command()
    async def coinflip(self):
        coinflip = ("Heads","Tails")
        await self.kobold.say(random.choice(coinflip))

class Dice:
    def __init__(self,dice,bonus):
        values = re.findall('[0-9][0-9]*', dice)
        self.bonus = bonus
        self.rolls = int(values[0])
        self.faces = int(values[1])
        self.total_amount = 0
        self.crit_fail = 0
        self.crit_success = 0

    def add_dice(self):
        for x in range(0, self.rolls):
            roll = random.randint(1, self.faces)
            if self.faces == 20:
                if roll == 1:
                    self.crit_fail += 1
                elif roll == 20:
                    self.crit_success += 1
            self.total_amount += roll
        self.total_amount += int(self.bonus)

def setup(kobold):
    kobold.add_cog(Basic(kobold))