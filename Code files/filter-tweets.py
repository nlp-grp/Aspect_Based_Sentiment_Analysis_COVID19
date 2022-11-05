import gzip
import glob
import json

path='/Users/Meghna/Desktop/Twitter_Covid_Data/*.json.gz'

files=glob.glob(path)
hashtags=set()


filter_hashtags=["jackblack", "blackout", "ianblackford", "pourleblackfridayjeveux", "blacksabbath", "blackfenandlamorbey", "blackfridaychollometrototal", "jumiablackfridays", "adablackjackrising", "theravenblackcourt", "blackbuckpoachingcase", "cuomoblackmailed", "blackfriars", "blackfridaydeals", "vodafoneblackfriday", "blackmailbritain", "blackmetal", "callofdutyblackopscoldwar", "blackadder", "blackpool", "boohoomanblackfriday", "blackholes", "quaranteamblackpinki", "blackpink", "blackpanther", "blacklabrador", "blackfridaygiveback", "blackcatcafe", "foxblackout", "quaranteamblackpink", "brightasablackout", "blackpinkditokopediawib", "belfastblacksanta", "blackfriday2020", "blackurnsmatter", "blackwidow", "blackfridayamazon", "istreamblackmamba", "blacklab", "awablackfriday", "blackandgreytattoo", "blacksea", "blacknobility", "blackflies", "theblacklist", "blackfridaysale", "chicagoblackhawks", "blackburn", "blackswan", "blackpink_boomboom", "blackbirdnews", "blackcoffee", "blackhawks", "blackeyedpeas", "blackboard", "blackhawkcounty", "allyblackmailing", "blackandwhitephotography", "blackrock", "globalblacklist", "blackwallstreetrenaissance", "blackdress", "justintrudeaublackface", "blacknoir", "blackmoth", "swedenblackswan", "blackedout", "blacksonville", "blackopscoldwar", "blackmarket", "blackmirror", "blackcountry", "blackopstech", "blackmailed", "blacktop", "blackhole", "blackstar", "theinvitation_blackpink", "orangeisthenewblack", "boohooblackfriday", "westreamblackmambafor100m", "blackpill", "blackberry", "blackfall", "bigblackdickbull", "blackmask", "blackmarkethappiness", "blackcat", "blacklightning", "blackmailing", "blackshiny", "anbublackops", "blackmail", "blackopscoldwarzombies", "blackfriday", "blackmamba" "blackhair", "blackinmarinescienceweek", "rslashblacktears",  "blackholes",  "itsblackleatherforareason", "goblackknights",  "whitegirlsgoneblack", "ianblackfordpropaganda", "quaranteamblackpi", "blackblock", "blackincarnaby", "blackeuphoria",  "blackopstech", "bigblackbullbulls", "blackmask", "blackmarkethappiness", "blacksanta", "resististhenewblack"]

black_hashtags=[
    "blackthroatsmatter",
    "blackdeath",
    "buyblacklocal",
    "blackatlanta",
    "blackamericans",
    "blackademics",
    "newblackmedia",
    "blacktechtwitter",
    "blackscientistsmatter",
    "blackwhite",
    "blackselflove",
    "blacktea",
    "blackpeople",
    "blacknativity",
    "blackentrepreneurs",
    "noantiblackracism",
    "allblackeverything",
    "blackhistoryflash",
    "blackowned",
    "amplifyblackstem",
    "blackandwhite",
    "blackdollars",
    "blackboyjoy",
    "blackhealthmatters",
    "mybeautifulblacksisters",
    "blackwriters",
    "giveblack",
    "blackscientist_series",
    "blackwealth",
    "blackexcellence",
    "blacklove",
    "blackandbrown",
    "buyblackowned",
    "blackboy",
    "defundedblackneighborhoods",
    "blackfolks",
    "blackwomenlead",
    "supportblackownedbusinesses",
    "writingblackness",
    "repealblacklaws",
    "blacklivesstillmatter",
    "blackheath",
    "blackpowermatters",
    "truthbeblack",
    "blacksfortrump",
    "thenewblacks",
    "blackhospitalityexperience",
    "listentoblackwomen",
    "blackgirlsrock",
    "buyblack",
    "blackhistory",
    "almightblackdollar",
    "blackgirl",
    "blacklovematters",
    "blackfolk",
    "blackmodel",
    "blackjoy",
    "blackdaddy",
    "blackspinglobal",
    "blackonblack",
    "undertheblacklight",
    "blackbusiness",
    "blackownership",
    "blackfamily",
    "blackaccine",
    "blackboris",
    "blacklivesmetter",
    "blackbusinesses",
    "trustblackwomen",
    "blackall",
    "blackface",
    "blackmuscle",
    "blacklivesmatter",
    "blackish",
    "blackwomendoctors",
    "blackchurches",
    "almightyblackdollar",
    "blackpodcast",
    "blackbeauty",
    "immigrationisablackissue",
    "blackgirlwriters",
    "blacklockdownlivesmatter",
    "blackhealthmattersgm",
    "supportblackbusiness",
    "blackvotersmatter",
    "blackisgold",
    "black",
    "blacklifematters",
    "blackled",
    "blackmothers",
    "youaintblack",
    "codeblack",
    "blackindata",
    "stopkillingblackpeople",
    "blacklivematter",
    "blackmen",
    "supportblackbusinesses",
    "youngblackandgifted",
    "blackman",
    "blackcommunity",
    "blackprofessional",
    "congressionalblackconjob",
    "blackgirlmagic",
    "blacknews",
    "blacktwitter",
    "5blackmoms",
    "blackwomen",
    "blacknbritish",
    "vaxtheblacks",
    "antiblackwar",
    "blackbuck",
    "blackownedbusiness",
    "habariblacknovember",
    "blackhomeschooling",
    "blackhealth",
    "blackpride",
    "allblacks",
    "fakeblmhasgotblackskillingblacks",
    "allblackaffair",
    "blackwoman",
    "blacks",
    "blacksantaclaus",
    "blackwivesmatter"]

for i in range(len(files)):
    print("opening file", files[i])
    file_name=files[i].split("/")[-1]
    try:
        with gzip.open(files[i],'r') as fin:
            for line in fin:
                tweet=json.loads(line)
                hashtag_list=tweet['entities']['hashtags'] 
                if hashtag_list!=[] :
                    for hashtag in hashtag_list:
                        got_hashtag=hashtag['text'].lower()
                        if ((got_hashtag in black_hashtags) and (got_hashtag not in filter_hashtags)):
                            file_is='/Users/Meghna/Desktop/Filtered_BlackA_Tweets/'+file_name
                            with gzip.open(file_is,'ab') as fout:
                                fout.write(json.dumps(tweet).encode('utf-8')+b"\n")
        print(f"Written for file {files[i]}")
    except:
        print("Faulty file ", files[i])

