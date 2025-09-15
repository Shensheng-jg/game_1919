# -*- coding: utf-8 -*-
# 在不改变剧情走向的前提下，补充属性与条件判断

# ===== 变量 =====
# 运动层面
default reputation = 0           # 社会支持度（-3 ~ +3）
default risk = 0                 # 风险值（0 ~ 5）
default route_taken = ""         # direct / detour
default action_at_zjl = ""       # attack / parade
default city_support = 0         # 各地响应度（由过程动态累计）
default media_attention = 0      # 媒体关注度


default passion = 0              # 爱国热情
default insight = 0              # 思想觉悟
default fame = 0                 # 社会声望（个人影响力）
# 旗标
default jailed = False           # 是否被捕
default wrote_radical = False    # 是否写过檄文
default wrote_commentary = False # 是否写过评论
default strategy_work = ""    # 记录“街头演讲 / 办报写文章”


# ===== 角色 =====
define s = Character("你", color="#66ccff")
define c = Character("同学", color="#f5a623")
define l = Character("领队", color="#7ed321")
define g = Character("工人代表", color="#f45b69")
define m = Character("商会代表", color="#b28bd0")
define j = Character("记者", color="#c1a45b")
define n = Character("旁白")

label start:
    scene black
    with fade

    # 剧情身份介绍
    n "巴黎和会消息传来，校园内群情激愤。"

    $ reputation = 0
    $ risk = 0
    $ route_taken = ""
    $ action_at_zjl = ""
    $ city_support = 0
    $ media_attention = 0
    $ passion = 0
    $ insight = 0
    $ fame = 0
    $ jailed = False
    $ wrote_radical = False
    $ wrote_commentary = False

    n "学生号召明日上街游行，你是否参加？"
    menu:
        "积极参加":
            # 个人成长与舆论面增益
            $ passion += 2
            $ fame += 1
            $ reputation += 1
            jump join

        "谨慎观望":
            # 冷静评估，觉悟上升但声望略降
            $ insight += 2
            $ reputation -= 1
            $ media_attention += 0
            jump hesitate

        "拒绝参加":
            # 自我抽离，声望与社会支持下降
            $ fame -= 1
            $ reputation -= 2
            jump refuse

label join:
    s "不能再沉默了，我们要让全国知道我们的立场。"
    c "队伍正在操场集合，领队在等你给个主意。"
    $ media_attention += 1
    jump plan_route

label plan_route:
    n "需要决定游行路线，是直达目标地点，还是选择更安全的迂回路线？"

    menu:
        "直达赵家楼（更快但风险高）":
            $ route_taken = "direct"
            $ risk += 2
            $ media_attention += 1
            # 冲劲会被同伴认可，热情小幅上涨
            $ passion += 1
            n "你决定直奔赵家楼，队伍情绪高涨，但沿路阻力也在增加。"
            jump zhaojialou_choice

        "迂回前进（较安全，可沿途发动群众）":
            $ route_taken = "detour"
            $ risk += 0
            $ reputation += 1
            $ media_attention += 1
            $ insight += 1
            # 沿途演讲可累积个人声望
            $ fame += 1
            n "你带队选择相对安全的路线，沿途发表演讲，争取更多人加入。"
            jump detour_route

label detour_route:
    n "你们在胡同口和茶楼前停下，向店家与路人说明学生们的诉求。"
    s "我们维护国家尊严，并非生事。请大家理解与支持。"
    $ reputation += 1
    $ media_attention += 1
    $ fame += 1
    c "越来越多人愿意同行了！"
    n "队伍重新集合，向目标地点前进。"
    jump zhaojialou_choice

label zhaojialou_choice:
    n "人潮聚拢到赵家楼附近，队伍内部意见出现分歧。"
    l "惩治国贼，就在今日！"
    c "我们的目的是示威，不是破坏！"

    menu:
        "冲击赵家楼（风险极高）":
            $ action_at_zjl = "attack"
            $ risk += 3
            $ reputation -= 1
            $ media_attention += 2
            $ passion += 1
            # 过激倾向使未来被捕几率上升（在后续结算里通过 risk 与分支体现）
            n "情绪到达顶点，部分人冲向大门，现场迅速失控。"
            n "混乱之中，警力介入，你们不得不撤离。"
            jump aftermath_capitol

        "维持秩序继续游行（较稳妥）":
            $ action_at_zjl = "parade"
            $ risk += 1
            $ reputation += 1
            $ media_attention += 1
            $ insight += 1
            $ fame += 1
            n "你维持队形，继续高呼口号，吸引了媒体与市民围观。"
            jump continue_parade

label continue_parade:
    j "请问你们的诉求是什么？能否对全国同胞说几句？"
    s "我们反对不平等条约，要求惩处卖国之徒，保全国家尊严。"
    $ media_attention += 2
    $ reputation += 1
    $ fame += 1
    n "采访刊发后，引发更广泛讨论。"
    jump movement_spread

label aftermath_capitol:
    n "激烈行动虽吸引目光，但也带来沉重代价。"
    if risk >= 4:
        n "多人被捕，部分同学受伤。"
        $ reputation -= 1
        $ fame -= 1
        $ jailed = True
    else:
        n "在少数人的拉拽下，你们勉强撤出险境。"
        $ fame += 0
    j "社会上出现不同声音，有人支持，也有人谴责过激行为。"
    $ media_attention += 1
    jump movement_spread

label hesitate:
    s "我们需要更成熟的计划，不应做无谓的牺牲。"
    $ insight += 1
    $ fame -= 1
    jump movement_spread

label refuse:
    s "我的职责是读书，政治非我所愿。"
    $ insight += 0
    $ passion -= 1
    $ reputation -= 1
    jump movement_spread

label movement_spread:
    n "运动从北京扩散至全国，学生罢课，工人罢工，商人罢市。"
    # 响应度受社会支持与媒体关注、个人声望调制
    $ city_support += reputation + media_attention + (fame // 2)
    # 若前面选择“迂回”并持续文宣，传播效率额外加成
    if route_taken == "detour":
        $ city_support += 1
    # 若曾被捕，引发同情与关注的同时也压缩组织机动性
    if jailed:
        $ media_attention += 1
        $ reputation -= 1
    n "你收到来自各地的讯息：响应程度取决于你此前的策略与口碑。"
    jump strategy_choice

label strategy_choice:
    n "需要在全国范围内制定下一步策略。"

    menu:
        "街头演讲":
            $ strategy_work = "街头演讲"
            jump speech

        "办报写文章":
            $ strategy_work = "办报写文章"
            jump article

label speech:
    n "你选择站在街头巷尾、闹市茶馆，向市民、工人、商人演讲。"
    n "你慷慨陈词，讲述青岛问题的来龙去脉，听众的眼神从迷茫变为坚定。"
    n "但这也伴随着风险。你看到有人形迹可疑，怀疑是密探靠近，你选择？"

    # 将演讲效果与个人属性绑定
    $ fame += 1 + (1 if passion >= 2 else 0)
    $ reputation += 1
    $ media_attention += 1

    menu:
        "勇敢继续，吸引注意让同伴撤退":
            # 高热情与高声望可减轻负面后果
            if passion + fame >= 4:
                n "你的号召力震慑了对方，同志们顺利撤离。"
                $ risk += 1
                $ reputation += 1
            else:
                n "你为掩护同伴被捕入狱。"
                $ jailed = True
                $ risk += 2
                $ reputation -= 1
            jump resolution

        "机智地转换话题，混入人群":
            n "你见机行事，迅速脱身。"
            $ insight += 1
            $ risk += 0
            jump resolution

label article:
    n "你伏案疾书，在报刊或自办小报上撰写文章。"
    n "你的文章逻辑清晰，既抨击国贼，也阐释“德先生”和“赛先生”的意义。"
    # 文章影响由觉悟和声望加成
    $ media_attention += 1 + (1 if insight >= 2 else 0)
    $ reputation += 1
    $ fame += 1

    n "你通过撰写文章，拥有了一定的影响力，接下来你决定?"
    menu:
        "写煽动性强的檄文，号召立即行动":
            $ wrote_radical = True
            $ passion += 1
            $ media_attention += 1
            $ risk += 1
            # 檄文能拉动支持，但也更易被打压
            $ reputation += 0
            jump resolution

        "写说理深刻的评论，进行思想启蒙":
            $ wrote_commentary = True
            $ insight += 1
            $ media_attention += 1
            $ reputation += 1
            jump resolution

label resolution:
    n "几周后，局势逐渐明朗。"

    # —— 胜利公告 —— 
    n "经过全国上下持续一个多月的巨大压力，胜利的消息终于传来！"
    n "北洋政府被迫释放了所有被捕的学生。"
    n "曹汝霖、章宗祥、陆宗舆三人被免职！"
    n "中国代表最终拒绝在《巴黎和约》上签字！"
    n "你们成功了！五四运动的直接目标已经实现。北京街头充满了欢呼的人群，你看到无数相识或不相识的人脸上洋溢着喜悦的泪水。"

    if strategy_work:
        n "在这场运动中，你主要参与了[ strategy_work ]工作，为胜利贡献了自己的力量。"

    n "运动渐渐平息，是时候思考未来了。这场经历彻底改变了你。"

    # ======= 画像判定：阈值与新结局 =======
    $ mass_power = reputation + city_support + media_attention

    # 悲剧英雄：阈值更高，强调“热情过盛 + 高风险/鲁莽迹象”
    $ is_tragic = (passion >= 6) and (action_at_zjl == "attack" or jailed or risk >= 5)

    # 革命之路：提高热情阈值，允许“写过檄文且风险承受高”作为次通道
    $ is_revolution = ((passion >= 5 and insight >= 4) or (wrote_radical and passion >= 4 and risk >= 3))

    # 文人斗士：提高声望与觉悟的双高门槛，并偏向写评论者
    $ is_literati = (fame >= 5 and insight >= 5 and (wrote_commentary or strategy_work == "办报写文章"))

    # 新结局1·社会组织者（群众领袖/社会改革者）：
    # 强组织力与号召力，群体动员分高，风险不至于失控
    $ is_organizer = ((fame >= 5 or reputation >= 2) and mass_power >= 8 and risk <= 4)

    # 新结局2·教育先行者（学术/留学/从教）：
    # 高觉悟、低风险取向，偏重理性建设；写评论或走“办报写文章”路径更容易触发
    $ is_academic = (insight >= 5 and risk <= 2 and (wrote_commentary or strategy_work == "办报写文章"))

    # ======= 结局分支 =======
    if is_tragic:
        n "【悲剧英雄】"
        n "你的爱国热情炽烈如火，也因此多次挺身在前。一次行动中，你身受重伤（或不幸牺牲）。"
        n "同学们以你的名字传颂这段历史，人们在惋惜中记住了那份无畏。"
        return

    elif is_revolution and not (is_literati or is_organizer or is_academic):
        n "【革命之路】"
        n "你对国家与人民的热爱与日俱增，思想也在斗争中日益成熟。"
        n "你南下，或远赴法国勤工俭学，最终走上革命道路，成为坚定的共产党人。"
        return

    elif is_literati and not (is_revolution or is_organizer or is_academic):
        n "【文人斗士】"
        n "你把笔当作刀枪，以文字为阵地。"
        n "你成为杰出的作家、记者或学者，在文化战线持续启蒙民众，推动社会变革。"
        return

    elif is_organizer and not (is_revolution or is_literati or is_academic):
        n "【社会组织者】"
        n "你擅长协调各界力量，号召学生、工人、商人形成合力。"
        n "此后你投身工会、社团或公益事业，推进社会改革，成为群众信赖的组织者。"
        return

    elif is_academic and not (is_revolution or is_literati or is_organizer):
        n "【教育先行者】"
        n "你选择在学术与教育中探寻强国之道，或远赴海外研习，或回国从教办学。"
        n "你用知识塑造新一代青年，让启蒙之火持续燃烧。"
        return

    # 同时满足多种画像时的倾向选择
    elif is_revolution or is_literati or is_organizer or is_academic:
        # 三维谁更突出，偏向相应人物画像
        if passion >= max(fame, insight) and is_revolution:
            n "【革命之路】"
            n "你既有思想也敢担当，最终投身革命洪流，成为坚定的共产党人。"
            return
        elif fame >= max(passion, insight):
            if is_organizer:
                n "【社会组织者】"
                n "你以出众的动员与协调能力，持续推动社会改革。"
                return
            else:
                n "【文人斗士】"
                n "你以广泛的社会影响力与深刻的思想，在文化战线持续战斗。"
                return
        else:
            if is_academic:
                n "【教育先行者】"
                n "你将理性与知识化为力量，投身教育与学术建设。"
                return
            else:
                n "【文人斗士】"
                n "你在思想与文化战线继续前行。"
                return

    else:
        n "【未定之途】"
        n "风浪过后，余波仍在。也许你会继续求学，也许你会在下一次风起时做出新的抉择。"
        n "五四的火种，已在你心中点亮。"
        return
