import random
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown


class Waifus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot ~Kakashi command for Zara
    @commands.command(aliases=['Kakashi'])
    @cooldown(1, 0, BucketType.channel)
    async def kakashi(self, ctx):
        channels = ["bot-commands"]
        if str(ctx.channel) not in channels:
            message = await ctx.send("Sorry! I only work in #bot-commands!")

            # Let the user read the message for 2.5 seconds
            await asyncio.sleep(2.5)
            # Delete the message
            await message.delete()

        if str(ctx.channel) in channels:
            kakashi1 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077346238514/image0.jpg"
            kakashi2 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077669331036/image1.jpg"
            kakashi3 = "https://cdn.discordapp.com/attachments/714671068941647933/717201077941829722/image2.jpg"
            kakashi4 = "https://cdn.discordapp.com/attachments/714671068941647933/717201078633889913/image4.jpg"
            kakashi5 = "https://cdn.discordapp.com/attachments/714671068941647933/717201078885810176/image5.jpg"
            kakashi6 = "https://cdn.discordapp.com/attachments/714671068941647933/717203540048871456/40964a8ec3616dd143db1ac63c4090ee.jpg"
            kakashi7 = "https://media.discordapp.net/attachments/714671068941647933/717203546772340846/4707601f950c412dd6978c8264308632.jpg"
            kakashi8 = "https://media.discordapp.net/attachments/714671068941647933/717203597774946354/7941b52067df70825ae3a9051acfd98d.jpg"
            kakashi9 = "https://media.discordapp.net/attachments/714671068941647933/717203650333900840/dafb0bc78adc3548e9c9b24460d7c10d.jpg"
            kakashi10 = "https://media.discordapp.net/attachments/714671068941647933/717203693925040188/aad4edeac8e034683b5602cf01a41333.jpg?width=465&height=658"
            kakashi11 = "https://media.discordapp.net/attachments/714671068941647933/717203717085986836/5851485577679be2a09bdebef7e35522.jpg?width=390&height=658"
            kakashi12 = "https://media.discordapp.net/attachments/714671068941647933/717203783016513626/e2a746123c1e36d995fa95c44a3c3f85.jpg"
            kakashi13 = "https://media.discordapp.net/attachments/714671068941647933/717203811923394611/268a3266d4c255b72925a3eb541f4cf5.jpg?width=517&height=657"
            kakashi14 = "https://media.discordapp.net/attachments/714671068941647933/717203866986479636/b283f71be006957107926e1d5d9ab60e.jpg?width=591&height=658"
            kakashi15 = "https://cdn.discordapp.com/attachments/714671068941647933/717203972925947984/6f46bb96761b673f1c4f4b5584bf1ba8.jpg"
            kakashi16 = "https://cdn.discordapp.com/attachments/714671068941647933/717204020711915581/4025c1241a206406555bd6ab53640291.jpg"
            kakashi17 = "https://cdn.discordapp.com/attachments/714671068941647933/717204198491422770/94287174f2f5e5316144981190a38c66.jpg"
            kakashi18 = "https://cdn.discordapp.com/attachments/714671068941647933/717204289755283547/a9868fb38857dd51ccc93a3e202644ff.gif"
            kakashi19 = "https://cdn.discordapp.com/attachments/714671068941647933/717204351638175784/3967dabc9b069080daded9a38f1d9e49.jpg"
            kakashi20 = "https://cdn.discordapp.com/attachments/714671068941647933/717204405178597396/3d063a07af0cfa320a100e169c959ff4.jpg"
            kakashi21 = "https://cdn.discordapp.com/attachments/714671068941647933/717204454264537151/4c607bbcc9a360257e1d14b5c9858b21.jpg"
            kakashi22 = "https://cdn.discordapp.com/attachments/714671068941647933/717204495939141692/9d85777e4a452f2f38464f8a11dece5b.jpg"
            kakashi23 = "https://cdn.discordapp.com/attachments/714671068941647933/717204530760122478/edeaa333ed2fb68aa1205a783d0bb783.jpg"
            kakashi24 = "https://cdn.discordapp.com/attachments/714671068941647933/717204561936252958/4f39f6de439a99b4113f6a33fd803079.jpg"
            kakashi25 = "https://cdn.discordapp.com/attachments/714671068941647933/717204627484967012/ebb8b6713aff32745503d6cbe8996569.jpg"
            kakashi26 = "https://cdn.discordapp.com/attachments/714671068941647933/717204713648685126/a6cb9a07745c163d14d736e077765ec8.gif"
            kakashi27 = "https://cdn.discordapp.com/attachments/714671068941647933/717204734905417738/3a081283ef670fd5326a694b7d41d35d.jpg"
            kakashi28 = "https://cdn.discordapp.com/attachments/714671068941647933/717204879155921006/864704a29ef1201f78f7f8fd71f57cf7.gif"
            kakashi29 = "https://cdn.discordapp.com/attachments/714671068941647933/717204999792361472/d9b273a711ccf1e6af531443a4cf06b5.jpg"
            kakashi30 = "https://cdn.discordapp.com/attachments/714671068941647933/717205121259405332/d2426eff482c18af2586e1fd2499d3d5.jpg"
            kakashi31 = "https://cdn.discordapp.com/attachments/714671068941647933/717205186463924224/7e27f5a97a80444ab5fc773e4d09d1bb.jpg"
            kakashi32 = "https://cdn.discordapp.com/attachments/714671068941647933/717205371835514930/IMG_20191212_215715_438.jpg"
            kakashi33 = "https://cdn.discordapp.com/attachments/714671068941647933/717205515519655976/df09731e2b38c1f50cc57f4600d937f5.jpg"
            kakashi34 = "https://cdn.discordapp.com/attachments/714671068941647933/717206154882842695/image0.jpg"
            kakashi35 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155356798986/image1.jpg"
            kakashi36 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155562057780/image2.jpg"
            kakashi37 = "https://cdn.discordapp.com/attachments/714671068941647933/717206155797200896/image3.jpg"
            kakashi38 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156031819786/image4.jpg"
            kakashi39 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156191334460/image5.jpg"
            kakashi40 = "https://cdn.discordapp.com/attachments/714671068941647933/717206156673679380/image6.gif"
            kakashi41 = "https://cdn.discordapp.com/attachments/714671068941647933/717206157227327578/image7.jpg"
            kakashi42 = "https://cdn.discordapp.com/attachments/714671068941647933/717206621121544230/image0.jpg"
            kakashi43 = "https://cdn.discordapp.com/attachments/714671068941647933/717206621310418954/image1.jpg"
            kakashi44 = "https://cdn.discordapp.com/attachments/714671068941647933/717206621666672721/image2.jpg"
            kakashi45 = "https://cdn.discordapp.com/attachments/714671068941647933/717206621993959474/image3.jpg"
            kakashi46 = "https://cdn.discordapp.com/attachments/714671068941647933/717206622249943050/image4.jpg"
            kakashi47 = "https://cdn.discordapp.com/attachments/714671068941647933/717206622489018458/image5.jpg"
            kakashi48 = "https://cdn.discordapp.com/attachments/714671068941647933/717206622979489792/image6.jpg"
            kakashi49 = "https://cdn.discordapp.com/attachments/714671068941647933/717545579713921065/image0.gif"
            kakashi50 = "https://cdn.discordapp.com/attachments/714671068941647933/717545580070699068/image1.gif"
            kakashi51 = "https://cdn.discordapp.com/attachments/714671068941647933/717545580393398332/image2.gif"
            kakashi52 = "https://cdn.discordapp.com/attachments/714671068941647933/717545580804702228/image3.gif"
            kakashi53 = "https://cdn.discordapp.com/attachments/714671068941647933/717545581299499179/image4.jpg"
            kakashi54 = "https://cdn.discordapp.com/attachments/714671068941647933/717545581526122586/image5.jpg"
            kakashi55 = "https://cdn.discordapp.com/attachments/714671068941647933/717545581815529532/image6.jpg"
            kakashi56 = "https://cdn.discordapp.com/attachments/714671068941647933/717545582046085140/image7.jpg"
            kakashi57 = "https://cdn.discordapp.com/attachments/714671068941647933/717545582234697748/image8.jpg"
            kakashi58 = "https://cdn.discordapp.com/attachments/714671068941647933/717545582427766784/image9.jpg"
            kakashi59 = "https://cdn.discordapp.com/attachments/714671068941647933/717547623334019102/image0.gif"
            kakashi60 = "https://cdn.discordapp.com/attachments/714671068941647933/717547623762100254/image1.jpg"
            kakashi61 = "https://cdn.discordapp.com/attachments/714671068941647933/717547624122810388/image2.jpg"
            kakashi62 = "https://cdn.discordapp.com/attachments/714671068941647933/717547624374206554/image3.jpg"
            kakashi63 = "https://cdn.discordapp.com/attachments/714671068941647933/717547624655355944/image4.jpg"
            kakashi64 = "https://cdn.discordapp.com/attachments/714671068941647933/717547624906883082/image5.jpg"
            kakashi65 = "https://cdn.discordapp.com/attachments/714671068941647933/717547625095626752/image6.jpg"
            kakashi66 = "https://cdn.discordapp.com/attachments/714671068941647933/717547625557262417/image7.jpg"
            kakashi67 = "https://cdn.discordapp.com/attachments/714671068941647933/717547625762521167/image8.gif"
            kakashi68 = "https://cdn.discordapp.com/attachments/714671068941647933/717547626081288242/image9.jpg"
            kakashi69 = "https://cdn.discordapp.com/attachments/714671068941647933/717548032249430016/image0.jpg"
            kakashi70 = "https://cdn.discordapp.com/attachments/714671068941647933/717548032614465556/image1.jpg"
            kakashi71 = "https://cdn.discordapp.com/attachments/714671068941647933/717548033000079380/image2.jpg"
            kakashi72 = "https://cdn.discordapp.com/attachments/714671068941647933/717548033344143410/image3.jpg"
            kakashi73 = "https://cdn.discordapp.com/attachments/714671068941647933/717548033612709999/image4.jpg"
            kakashi74 = "https://cdn.discordapp.com/attachments/714671068941647933/717548033868300298/image5.jpg"
            kakashi75 = "https://cdn.discordapp.com/attachments/714671068941647933/717548034149449738/image6.jpg"
            kakashi76 = "https://cdn.discordapp.com/attachments/714671068941647933/717548034359296046/image7.jpg"
            kakashi77 = "https://cdn.discordapp.com/attachments/714671068941647933/717548034631663616/image8.jpg"
            kakashi78 = "https://cdn.discordapp.com/attachments/714671068941647933/717548034820538406/image9.jpg"
            kakashi79 = "https://cdn.discordapp.com/attachments/714671068941647933/717551546946158602/image0.jpg"
            kakashi80 = "https://cdn.discordapp.com/attachments/714671068941647933/717551547197947954/image1.jpg"
            kakashi81 = "https://cdn.discordapp.com/attachments/714671068941647933/717551547525103616/image2.gif"
            kakashi82 = "https://cdn.discordapp.com/attachments/714671068941647933/717551547776630824/image3.jpg"
            kakashi83 = "https://cdn.discordapp.com/attachments/714671068941647933/717551548170764398/image4.jpg"
            kakashi84 = "https://cdn.discordapp.com/attachments/714671068941647933/717551548380610570/image5.jpg"
            kakashi85 = "https://cdn.discordapp.com/attachments/714671068941647933/717551548720349235/image6.jpg"
            kakashi86 = "https://cdn.discordapp.com/attachments/714671068941647933/717551549139648592/image7.jpg"
            kakashi87 = "https://cdn.discordapp.com/attachments/714671068941647933/717551549357883512/image8.jpg"
            kakashi88 = "https://cdn.discordapp.com/attachments/714671068941647933/717551549525786745/image9.jpg"
            kakashi89 = "https://cdn.discordapp.com/attachments/714671068941647933/717551728316121148/image0.jpg"
            kakashi90 = "https://cdn.discordapp.com/attachments/714671068941647933/717551728873963610/image1.jpg"
            kakashi91 = "https://cdn.discordapp.com/attachments/714671068941647933/717551729343725568/image2.jpg"
            kakashi92 = "https://cdn.discordapp.com/attachments/714671068941647933/717551729343725568/image2.jpg"
            kakashi93 = "https://cdn.discordapp.com/attachments/714671068941647933/717551729683595334/image3.jpg"
            kakashi94 = "https://cdn.discordapp.com/attachments/714671068941647933/717551730065276948/image4.jpg"
            kakashi95 = "https://cdn.discordapp.com/attachments/714671068941647933/717551730400821298/image5.jpg"
            kakashi96 = "https://cdn.discordapp.com/attachments/714671068941647933/717551731537477662/image6.jpg"
            kakashi97 = "https://cdn.discordapp.com/attachments/714671068941647933/717551731969622039/image7.jpg"
            kakashi98 = "https://cdn.discordapp.com/attachments/714671068941647933/717551732338458654/image8.jpg"
            kakashi99 = "https://cdn.discordapp.com/attachments/714671068941647933/717551732594442290/image9.jpg"
            kakashi100 = "https://cdn.discordapp.com/attachments/714671068941647933/717552058877739119/image0.gif"

            kakashi_array = [kakashi1, kakashi2, kakashi3, kakashi4, kakashi5, kakashi6, kakashi7, kakashi8, kakashi9,
                             kakashi10,
                             kakashi11, kakashi12, kakashi13, kakashi14, kakashi15, kakashi16, kakashi17, kakashi18,
                             kakashi19,
                             kakashi20,
                             kakashi21, kakashi22, kakashi23, kakashi24, kakashi25, kakashi26, kakashi27, kakashi28,
                             kakashi29,
                             kakashi30,
                             kakashi31, kakashi32, kakashi33, kakashi34, kakashi35, kakashi36, kakashi37, kakashi38,
                             kakashi39,
                             kakashi40,
                             kakashi41, kakashi42, kakashi43, kakashi44, kakashi45, kakashi46, kakashi47, kakashi48,
                             kakashi49,
                             kakashi50,
                             kakashi51, kakashi52, kakashi53, kakashi54, kakashi55, kakashi56, kakashi57, kakashi58,
                             kakashi59,
                             kakashi60,
                             kakashi61, kakashi62, kakashi63, kakashi64, kakashi65, kakashi66, kakashi67, kakashi68,
                             kakashi69,
                             kakashi70,
                             kakashi71, kakashi72, kakashi73, kakashi74, kakashi75, kakashi76, kakashi77, kakashi78,
                             kakashi79,
                             kakashi80,
                             kakashi81, kakashi82, kakashi83, kakashi84, kakashi85, kakashi86, kakashi87, kakashi88,
                             kakashi89,
                             kakashi90,
                             kakashi91, kakashi92, kakashi93, kakashi94, kakashi95, kakashi96, kakashi97, kakashi98,
                             kakashi99,
                             kakashi100]

            embed = discord.Embed(title="```Random Kakashi Image```", colour=discord.Colour(0xff0000), )
            embed.set_image(url=random.choice(kakashi_array))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Waifus(bot))
