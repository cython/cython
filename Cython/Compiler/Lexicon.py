# -*- coding: utf-8 -*-
# cython: language_level=3, py2_import=True
#
#   Cython Scanner - Lexical Definitions
#

from __future__ import absolute_import, unicode_literals

raw_prefixes = "rR"
bytes_prefixes = "bB"
string_prefixes = "fFuU" + bytes_prefixes
char_prefixes = "cC"
any_string_prefix = raw_prefixes + string_prefixes + char_prefixes
IDENT = 'IDENT'


def make_lexicon():
    from ..Plex import \
        Str, Any, AnyBut, AnyChar, Rep, Rep1, Opt, Bol, Eol, Eof, \
        TEXT, IGNORE, Method, State, Lexicon, Range

    nonzero_digit = Any("123456789")
    digit = Any("0123456789")
    bindigit = Any("01")
    octdigit = Any("01234567")
    hexdigit = Any("0123456789ABCDEFabcdef")
    indentation = Bol + Rep(Any(" \t"))

    # The list of valid unicode identifier characters are pretty slow to generate at runtime,
    # and require Python3, so are just included directly here
    # (via the generated code block at the bottom of the file)
    unicode_start_character = (Any(unicode_start_ch_any) | Range(unicode_start_ch_range))
    unicode_continuation_character = (
        unicode_start_character |
        Any(unicode_continuation_ch_any) | Range(unicode_continuation_ch_range))

    def underscore_digits(d):
        return Rep1(d) + Rep(Str("_") + Rep1(d))

    def prefixed_digits(prefix, digits):
        return prefix + Opt(Str("_")) + underscore_digits(digits)

    decimal = underscore_digits(digit)
    dot = Str(".")
    exponent = Any("Ee") + Opt(Any("+-")) + decimal
    decimal_fract = (decimal + dot + Opt(decimal)) | (dot + decimal)

    #name = letter + Rep(letter | digit)
    name = unicode_start_character + Rep(unicode_continuation_character)
    intconst = (prefixed_digits(nonzero_digit, digit) |  # decimal literals with underscores must not start with '0'
                (Str("0") + (prefixed_digits(Any("Xx"), hexdigit) |
                             prefixed_digits(Any("Oo"), octdigit) |
                             prefixed_digits(Any("Bb"), bindigit) )) |
                underscore_digits(Str('0'))  # 0_0_0_0... is allowed as a decimal literal
                | Rep1(digit)  # FIXME: remove these Py2 style decimal/octal literals (PY_VERSION_HEX < 3)
                )
    intsuffix = (Opt(Any("Uu")) + Opt(Any("Ll")) + Opt(Any("Ll"))) | (Opt(Any("Ll")) + Opt(Any("Ll")) + Opt(Any("Uu")))
    intliteral = intconst + intsuffix
    fltconst = (decimal_fract + Opt(exponent)) | (decimal + exponent)
    imagconst = (intconst | fltconst) + Any("jJ")

    # invalid combinations of prefixes are caught in p_string_literal
    beginstring = Opt(Rep(Any(string_prefixes + raw_prefixes)) |
                      Any(char_prefixes)
                      ) + (Str("'") | Str('"') | Str("'''") | Str('"""'))
    two_oct = octdigit + octdigit
    three_oct = octdigit + octdigit + octdigit
    two_hex = hexdigit + hexdigit
    four_hex = two_hex + two_hex
    escapeseq = Str("\\") + (two_oct | three_oct |
                             Str('N{') + Rep(AnyBut('}')) + Str('}') |
                             Str('u') + four_hex | Str('x') + two_hex |
                             Str('U') + four_hex + four_hex | AnyChar)

    bra = Any("([{")
    ket = Any(")]}")
    ellipsis = Str("...")
    punct = Any(":,;+-*/|&<>=.%`~^?!@")
    diphthong = Str("==", "<>", "!=", "<=", ">=", "<<", ">>", "**", "//",
                    "+=", "-=", "*=", "/=", "%=", "|=", "^=", "&=",
                    "<<=", ">>=", "**=", "//=", "->", "@=", "&&", "||", ':=')
    spaces = Rep1(Any(" \t\f"))
    escaped_newline = Str("\\\n")
    lineterm = Eol + Opt(Str("\n"))

    comment = Str("#") + Rep(AnyBut("\n"))

    return Lexicon([
        (name, Method('normalize_ident')),
        (intliteral, Method('strip_underscores', symbol='INT')),
        (fltconst, Method('strip_underscores', symbol='FLOAT')),
        (imagconst, Method('strip_underscores', symbol='IMAG')),
        (ellipsis | punct | diphthong, TEXT),

        (bra, Method('open_bracket_action')),
        (ket, Method('close_bracket_action')),
        (lineterm, Method('newline_action')),

        (beginstring, Method('begin_string_action')),

        (comment, IGNORE),
        (spaces, IGNORE),
        (escaped_newline, IGNORE),

        State('INDENT', [
            (comment + lineterm, Method('commentline')),
            (Opt(spaces) + Opt(comment) + lineterm, IGNORE),
            (indentation, Method('indentation_action')),
            (Eof, Method('eof_action'))
        ]),

        State('SQ_STRING', [
            (escapeseq, 'ESCAPE'),
            (Rep1(AnyBut("'\"\n\\")), 'CHARS'),
            (Str('"'), 'CHARS'),
            (Str("\n"), Method('unclosed_string_action')),
            (Str("'"), Method('end_string_action')),
            (Eof, 'EOF')
        ]),

        State('DQ_STRING', [
            (escapeseq, 'ESCAPE'),
            (Rep1(AnyBut('"\n\\')), 'CHARS'),
            (Str("'"), 'CHARS'),
            (Str("\n"), Method('unclosed_string_action')),
            (Str('"'), Method('end_string_action')),
            (Eof, 'EOF')
        ]),

        State('TSQ_STRING', [
            (escapeseq, 'ESCAPE'),
            (Rep1(AnyBut("'\"\n\\")), 'CHARS'),
            (Any("'\""), 'CHARS'),
            (Str("\n"), 'NEWLINE'),
            (Str("'''"), Method('end_string_action')),
            (Eof, 'EOF')
        ]),

        State('TDQ_STRING', [
            (escapeseq, 'ESCAPE'),
            (Rep1(AnyBut('"\'\n\\')), 'CHARS'),
            (Any("'\""), 'CHARS'),
            (Str("\n"), 'NEWLINE'),
            (Str('"""'), Method('end_string_action')),
            (Eof, 'EOF')
        ]),

        (Eof, Method('eof_action'))
        ],

        # FIXME: Plex 1.9 needs different args here from Plex 1.1.4
        #debug_flags = scanner_debug_flags,
        #debug_file = scanner_dump_file
        )


# BEGIN GENERATED CODE
# generated with:
# cpython 3.10.0a0 (heads/master:2b0e654f91, May 29 2020, 16:17:52)

unicode_start_ch_any = (
    u"_ªµºˬˮͿΆΌՙەۿܐޱߺࠚࠤࠨऽॐলঽৎৼਫ਼ઽૐૹଽୱஃஜௐఽಀಽೞഽൎලาຄລາຽໆༀဿၡႎჇჍቘዀៗៜᢪᪧᳺὙ"
    u"ὛὝιⁱⁿℂℇℕℤΩℨⅎⴧⴭⵯꣻꧏꩺꪱꫀꫂיִמּﹱﹳﹷﹹﹻﹽ𐠈𐠼𐨀𐼧𑅄𑅇𑅶𑇚𑇜𑊈𑌽𑍐𑓇𑙄𑚸𑤉𑤿𑥁𑧡𑧣𑨀𑨺𑩐𑪝𑱀𑵆𑶘𑾰𖽐𖿣𝒢"
    u"𝒻𝕆𞅎𞥋𞸤𞸧𞸹𞸻𞹂𞹇𞹉𞹋𞹔𞹗𞹙𞹛𞹝𞹟𞹤𞹾"
)
unicode_start_ch_range = (
    u"AZazÀÖØöøˁˆˑˠˤͰʹͶͷͻͽΈΊΎΡΣϵϷҁҊԯԱՖՠֈאתׯײؠيٮٯٱۓۥۦۮۯۺۼܒܯݍޥߊߪߴߵࠀࠕ"
    u"ࡀࡘࡠࡪࢠࢴࢶࣇऄहक़ॡॱঀঅঌএঐওনপরশহড়ঢ়য়ৡৰৱਅਊਏਐਓਨਪਰਲਲ਼ਵਸ਼ਸਹਖ਼ੜੲੴઅઍએઑઓનપરલળવહ"
    u"ૠૡଅଌଏଐଓନପରଲଳଵହଡ଼ଢ଼ୟୡஅஊஎஐஒகஙசஞடணதநபமஹఅఌఎఐఒనపహౘౚౠౡಅಌಎಐಒನಪಳವಹೠೡೱೲ"
    u"ഄഌഎഐഒഺൔൖൟൡൺൿඅඖකනඳරවෆกะเๆກຂຆຊຌຣວະເໄໜໟཀཇཉཬྈྌကဪၐၕၚၝၥၦၮၰၵႁႠჅაჺჼቈ"
    u"ቊቍቐቖቚቝበኈኊኍነኰኲኵኸኾዂዅወዖዘጐጒጕጘፚᎀᎏᎠᏵᏸᏽᐁᙬᙯᙿᚁᚚᚠᛪᛮᛸᜀᜌᜎᜑᜠᜱᝀᝑᝠᝬᝮᝰកឳᠠᡸᢀᢨ"
    u"ᢰᣵᤀᤞᥐᥭᥰᥴᦀᦫᦰᧉᨀᨖᨠᩔᬅᬳᭅᭋᮃᮠᮮᮯᮺᯥᰀᰣᱍᱏᱚᱽᲀᲈᲐᲺᲽᲿᳩᳬᳮᳳᳵᳶᴀᶿḀἕἘἝἠὅὈὍὐὗὟώᾀᾴ"
    u"ᾶᾼῂῄῆῌῐΐῖΊῠῬῲῴῶῼₐₜℊℓ℘ℝKℹℼℿⅅⅉⅠↈⰀⰮⰰⱞⱠⳤⳫⳮⳲⳳⴀⴥⴰⵧⶀⶖⶠⶦⶨⶮⶰⶶⶸⶾⷀⷆⷈⷎⷐⷖ"
    u"ⷘⷞ々〇〡〩〱〵〸〼ぁゖゝゟァヺーヿㄅㄯㄱㆎㆠㆿㇰㇿ㐀䶿一鿼ꀀꒌꓐꓽꔀꘌꘐꘟꘪꘫꙀꙮꙿꚝꚠꛯꜗꜟꜢꞈꞋꞿꟂꟊꟵꠁꠃꠅꠇꠊ"
    u"ꠌꠢꡀꡳꢂꢳꣲꣷꣽꣾꤊꤥꤰꥆꥠꥼꦄꦲꧠꧤꧦꧯꧺꧾꨀꨨꩀꩂꩄꩋꩠꩶꩾꪯꪵꪶꪹꪽꫛꫝꫠꫪꫲꫴꬁꬆꬉꬎꬑꬖꬠꬦꬨꬮꬰꭚꭜꭩꭰꯢ"
    u"가힣ힰퟆퟋퟻ豈舘並龎ﬀﬆﬓﬗײַﬨשׁזּטּלּנּסּףּפּצּﮱﯓﱝﱤﴽﵐﶏﶒﷇﷰﷹﹿﻼＡＺａｚｦﾝﾠﾾￂￇￊￏￒￗￚￜ𐀀𐀋𐀍𐀦𐀨𐀺"
    u"𐀼𐀽𐀿𐁍𐁐𐁝𐂀𐃺𐅀𐅴𐊀𐊜𐊠𐋐𐌀𐌟𐌭𐍊𐍐𐍵𐎀𐎝𐎠𐏃𐏈𐏏𐏑𐏕𐐀𐒝𐒰𐓓𐓘𐓻𐔀𐔧𐔰𐕣𐘀𐜶𐝀𐝕𐝠𐝧𐠀𐠅𐠊𐠵𐠷𐠸𐠿𐡕𐡠𐡶𐢀𐢞𐣠𐣲𐣴𐣵"
    u"𐤀𐤕𐤠𐤹𐦀𐦷𐦾𐦿𐨐𐨓𐨕𐨗𐨙𐨵𐩠𐩼𐪀𐪜𐫀𐫇𐫉𐫤𐬀𐬵𐭀𐭕𐭠𐭲𐮀𐮑𐰀𐱈𐲀𐲲𐳀𐳲𐴀𐴣𐺀𐺩𐺰𐺱𐼀𐼜𐼰𐽅𐾰𐿄𐿠𐿶𑀃𑀷𑂃𑂯𑃐𑃨𑄃𑄦𑅐𑅲"
    u"𑆃𑆲𑇁𑇄𑈀𑈑𑈓𑈫𑊀𑊆𑊊𑊍𑊏𑊝𑊟𑊨𑊰𑋞𑌅𑌌𑌏𑌐𑌓𑌨𑌪𑌰𑌲𑌳𑌵𑌹𑍝𑍡𑐀𑐴𑑇𑑊𑑟𑑡𑒀𑒯𑓄𑓅𑖀𑖮𑗘𑗛𑘀𑘯𑚀𑚪𑜀𑜚𑠀𑠫𑢠𑣟𑣿𑤆𑤌𑤓"
    u"𑤕𑤖𑤘𑤯𑦠𑦧𑦪𑧐𑨋𑨲𑩜𑪉𑫀𑫸𑰀𑰈𑰊𑰮𑱲𑲏𑴀𑴆𑴈𑴉𑴋𑴰𑵠𑵥𑵧𑵨𑵪𑶉𑻠𑻲𒀀𒎙𒐀𒑮𒒀𒕃𓀀𓐮𔐀𔙆𖠀𖨸𖩀𖩞𖫐𖫭𖬀𖬯𖭀𖭃𖭣𖭷𖭽𖮏𖹀𖹿"
    u"𖼀𖽊𖾓𖾟𖿠𖿡𗀀𘟷𘠀𘳕𘴀𘴈𛀀𛄞𛅐𛅒𛅤𛅧𛅰𛋻𛰀𛱪𛱰𛱼𛲀𛲈𛲐𛲙𝐀𝑔𝑖𝒜𝒞𝒟𝒥𝒦𝒩𝒬𝒮𝒹𝒽𝓃𝓅𝔅𝔇𝔊𝔍𝔔𝔖𝔜𝔞𝔹𝔻𝔾𝕀𝕄𝕊𝕐𝕒𝚥"
    u"𝚨𝛀𝛂𝛚𝛜𝛺𝛼𝜔𝜖𝜴𝜶𝝎𝝐𝝮𝝰𝞈𝞊𝞨𝞪𝟂𝟄𝟋𞄀𞄬𞄷𞄽𞋀𞋫𞠀𞣄𞤀𞥃𞸀𞸃𞸅𞸟𞸡𞸢𞸩𞸲𞸴𞸷𞹍𞹏𞹑𞹒𞹡𞹢𞹧𞹪𞹬𞹲𞹴𞹷𞹹𞹼𞺀𞺉𞺋𞺛"
    u"𞺡𞺣𞺥𞺩𞺫𞺻𠀀𪛝𪜀𫜴𫝀𫠝𫠠𬺡𬺰𮯠丽𪘀"
)
unicode_continuation_ch_any = (
    u"··়ׇֿٰܑ߽ৗ਼৾ੑੵ઼଼ஂௗ಼ൗ්ූัັ༹༵༷࿆᳭ᢩ៝᳴⁔⵿⃡꙯ꠂ꠆ꠋ꠬ꧥꩃﬞꪰ꫁＿𑅳𐨿𐇽𐋠𑈾𑍗𑑞𑥀𑧤𑩇𑴺𑵇𖽏𖿤𝩵"
    u"𝪄"
)
unicode_continuation_ch_range = (
    u"09ֽׁׂًؚ֑ׅ̀ͯ҃҇ׄؐ٩۪ۭۖۜ۟ۤۧۨ۰۹ܰ݊ަް߀߉࡙࡛࣓ࣣ߫߳ࠖ࠙ࠛࠣࠥࠧࠩ࠭࣡ःऺ़ाॏ॑ॗॢॣ०९ঁঃ"
    u"াৄেৈো্ৢৣ০৯ਁਃਾੂੇੈੋ੍੦ੱઁઃાૅેૉો્ૢૣ૦૯ૺ૿ଁଃାୄେୈୋ୍୕ୗୢୣ୦୯ாூெைொ்௦௯ఀఄాౄ"
    u"ెైొ్ౕౖౢౣ౦౯ಁಃಾೄೆೈೊ್ೕೖೢೣ೦೯ഀഃ഻഼ാൄെൈൊ്ൢൣ൦൯ඁඃාුෘෟ෦෯ෲෳำฺ็๎๐๙ຳຼ່ໍ໐໙"
    u"༘༙༠༩༾༿྄ཱ྆྇ྍྗྙྼါှ၀၉ၖၙၞၠၢၤၧၭၱၴႂႍႏႝ፝፟፩፱ᜒ᜔ᜲ᜴ᝒᝓᝲᝳ឴៓០៩᠋᠍᠐᠙ᤠᤫᤰ᤻᥆᥏᧐᧚"
    u"ᨗᨛᩕᩞ᩠᩿᩼᪉᪐᪙᪽ᪿᫀ᪰ᬀᬄ᬴᭄᭐᭙᭫᭳ᮀᮂᮡᮭ᮰᮹᯦᯳ᰤ᰷᱀᱉᱐᱙᳔᳨᳐᳒᳷᷹᷿᳹᷀᷻‿⁀⃥゙゚〪〯⃐⃜⃰⳯⳱ⷠⷿ"
    u"꘠꘩ꙴ꙽ꚞꚟ꛰꛱ꠣꠧꢀꢁꢴꣅ꣐꣙꣠꣱ꣿ꤉ꤦ꤭ꥇ꥓ꦀꦃ꦳꧀꧐꧙꧰꧹ꨩꨶꩌꩍ꩐꩙ꩻꩽꪴꪲꪷꪸꪾ꪿ꫫꫯꫵ꫶ꯣꯪ꯬꯭꯰꯹︀️︠︯"
    u"︳︴﹍﹏０９ﾞﾟ𐍶𐍺𐒠𐒩𐨁𐨃𐨅𐨆𐨌𐨺𐫦𐨏𐨸𐫥𐴤𐴧𐴰𐴹𐽆𐽐𐺫𐺬𑀀𑀂𑀸𑁆𑁦𑁯𑁿𑂂𑂰𑂺𑃰𑃹𑄀𑄂𑄧𑄴𑄶𑄿𑅅𑅆𑆀𑆂𑆳𑇀𑇉𑇌𑇎𑇙𑈬𑈷"
    u"𑋟𑋪𑋰𑋹𑌀𑌃𑌻𑌼𑌾𑍄𑍇𑍈𑍋𑍍𑍢𑍣𑍦𑍬𑍰𑍴𑐵𑑆𑑐𑑙𑒰𑓃𑓐𑓙𑖯𑖵𑖸𑗀𑗜𑗝𑘰𑙀𑙐𑙙𑚫𑚷𑛀𑛉𑜝𑜫𑜰𑜹𑠬𑠺𑣠𑣩𑤰𑤵𑤷𑤸𑤻𑤾𑥂𑥃𑥐𑥙"
    u"𑧑𑧗𑧚𑧠𑨁𑨊𑨳𑨹𑨻𑨾𑩑𑩛𑪊𑪙𑰯𑰶𑰸𑰿𑱐𑱙𑲒𑲧𑲩𑲶𑴱𑴶𑴼𑴽𑴿𑵅𑵐𑵙𑶊𑶎𑶐𑶑𑶓𑶗𑶠𑶩𑻳𑻶𖩠𖩩𖫰𖫴𖬰𖬶𖭐𖭙𖽑𖾇𖾏𖾒𖿰𖿱𛲝𛲞𝅩𝅥"
    u"𝅲𝅻𝆂𝆋𝅭𝆅𝆪𝆭𝉂𝉄𝟎𝟿𝨀𝨶𝨻𝩬𝪛𝪟𝪡𝪯𞀀𞀆𞀈𞀘𞀛𞀡𞀣𞀤𞀦𞀪𞄰𞄶𞅀𞅉𞋬𞋹𞥊𞣐𞣖𞥄𞥐𞥙🯰🯹"
)

# END GENERATED CODE
