import json
import os
import random

DATA_PATH = "data/"

GAME_TAGS = {
    "英雄联盟": ["上单专精", "打野高手", "中单法师", "ADC射手", "辅助守护", "全能选手", "团战指挥", "单带专家", "视野控制", "Gank专家"],
    "王者荣耀": ["打野核心", "射手输出", "法师控制", "坦克抗压", "辅助游走", "边路战士", "全能补位", "节奏带动", "团战核心", "单杀高手"],
    "绝地求生": ["狙击专家", "突击手", "战术指挥", "医疗兵", "侦察兵", "载具高手", "投掷专家", "房区攻防", "野外生存", "决赛圈大师"],
    "CS2": ["狙击手", "步枪手", "冲锋枪", "支援位", "突破手", "自由人", "指挥", "投掷专家", "防守专家", "进攻核心"],
    "原神": ["深渊带打", "探索达人", "剧情向导", "副本攻略", "角色培养", "元素搭配", "圣遗物专家", "武器锻造", "世界Boss", "秘境挑战"],
    "和平精英": ["狙击手", "突击手", "载具高手", "战术指挥", "房区攻防", "野外生存", "决赛圈大师", "团队配合", "单排高手", "四排专家"]
}

SERVICE_TAGS = ["上分神器", "娱乐聊天", "技术教学", "新手指导", "段位冲刺", "通宵陪玩", "周末特供", "语音优先", "视频可选", "耐心陪伴", "幽默风趣", "温柔体贴", "认真负责", "快速响应", "长期合作"]

PERSONALITY_TAGS = ["温柔体贴", "幽默风趣", "耐心细致", "热情开朗", "认真负责", "冷静沉稳", "活泼可爱", "成熟稳重", "善解人意", "积极向上", "细心周到", "专业严谨", "亲和力强", "反应快速", "沟通顺畅"]

TIME_TAGS = ["全天在线", "晚间时段", "通宵接单", "周末特供", "节假日加急", "快速响应", "预约优先", "灵活安排", "固定时段", "随时可约"]

VOICE_TYPES = ["萝莉音", "御姐音", "少年音", "大叔音", "磁性音", "甜美音", "温柔音", "活泼音", "清亮音", "低沉音"]

GAMES = ["英雄联盟", "王者荣耀", "绝地求生", "CS2", "原神", "和平精英"]

LEVELS = {
    "英雄联盟": ["青铜", "白银", "黄金", "铂金", "钻石", "大师", "宗师", "王者"],
    "王者荣耀": ["青铜", "白银", "黄金", "铂金", "钻石", "星耀", "王者", "荣耀王者"],
    "绝地求生": ["新手", "熟练", "精通", "专家", "大师", "前100", "前50", "前10"],
    "CS2": ["新手", "熟练", "精通", "专家", "大师", "传奇", "精英", "职业"],
    "原神": ["新手", "进阶", "熟练", "资深", "大佬", "60级", "满级", "全收集"],
    "和平精英": ["新手", "熟练", "精通", "专家", "大师", "王牌", "战神", "顶尖"]
}

PARTNER_COUNT = 50
PARTNER_START_ID = 22
PARTNER_END_ID = PARTNER_START_ID + PARTNER_COUNT

def get_avatar_url(seed):
    return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}"

def init_all_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    print("[INFO] 开始创建50个陪玩数据样本...")

    init_users()
    init_partners()
    init_tags()
    init_orders()
    init_evaluates()
    init_favorites()
    init_messages()
    init_token_cache()
    init_other_files()

    print("[OK] 所有初始数据已创建完成！")

def init_users():
    users = [{
        "user_id": 1,
        "username": "admin",
        "password": "admin123",
        "phone": "18888888888",
        "balance": 0.0,
        "role": "admin",
        "status": "active",
        "avatar": get_avatar_url("admin"),
        "create_time": "2024-01-01 10:00:00"
    }]

    player_names = ["游戏达人小明", "电竞少女小红", "硬核玩家老王", "休闲玩家小李", "上分狂人阿强", "娱乐玩家小美", "新手玩家小张", "资深玩家老刘", "周末玩家小周", "通宵玩家小赵", "技术流玩家阿杰", "聊天型玩家小雪", "上分型玩家小刚", "娱乐型玩家小芳", "全能玩家小吴", "LOL玩家小陈", "王者玩家小林", "吃鸡玩家小黄", "原神玩家小徐", "CS玩家小马"]

    for i, name in enumerate(player_names, start=2):
        users.append({
            "user_id": i,
            "username": name,
            "password": "123456",
            "phone": f"1380013{str(i).zfill(4)}",
            "balance": random.randint(100, 1000),
            "role": "player",
            "status": "active",
            "avatar": get_avatar_url(name),
            "create_time": f"2024-01-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })

    partner_names = [
        "王者大神阿强", "甜美声线小雪", "LOL职业选手", "温柔御姐小月", "吃鸡高手阿龙",
        "元气少女小樱", "技术流阿杰", "萝莉音小萌", "大叔音老张", "磁性音阿文",
        "打野王者小虎", "辅助天使小丽", "中单法师小云", "ADC射手小风", "上单战士小雷",
        "全能选手小星", "聊天达人小柔", "上分神器小霸", "新手导师小师", "娱乐陪玩小乐",
        "通宵达人小夜", "周末特供小周", "快速响应小快", "耐心陪伴小温", "幽默风趣小趣",
        "原神大佬小神", "CS高手小枪", "和平精英小和", "绝地求生小绝", "多游戏全能小全",
        "野区霸主小强", "下路战神小丽", "中路法王小中", "上路抗压小上", "游走辅助小辅",
        "狙神降临小狙", "突击之王小突", "战术大师小战", "载具达人小载", "医疗天使小医",
        "元素大师小元", "深渊征服者小深", "探索先锋小探", "副本专家小副", "圣遗物猎手小圣",
        "钢枪王小龙", "苟分大师小苟", "运营高手小运", "天命圈小王子", "海岛霸主小海"
    ]

    for i, name in enumerate(partner_names, start=PARTNER_START_ID):
        users.append({
            "user_id": i,
            "username": name,
            "password": "123456",
            "phone": f"1390013{str(i).zfill(4)}",
            "balance": 0.0,
            "role": "partner",
            "status": "active",
            "avatar": get_avatar_url(name),
            "create_time": f"2024-01-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })

    with open(os.path.join(DATA_PATH, "user.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"[OK] 用户数据已创建 ({len(users)}个用户: 1管理员 + 20玩家 + {PARTNER_COUNT}陪玩)")

def init_partners():
    partners = []
    partner_ids = range(PARTNER_START_ID, PARTNER_END_ID)

    for partner_id in partner_ids:
        game = random.choice(GAMES)
        level = random.choice(LEVELS[game])
        voice = random.choice(VOICE_TYPES)
        price = random.randint(30, 150)

        game_tags = random.sample(GAME_TAGS[game], min(3, len(GAME_TAGS[game])))
        service_tags = random.sample(SERVICE_TAGS, min(2, len(SERVICE_TAGS)))
        personality_tags = random.sample(PERSONALITY_TAGS, min(2, len(PERSONALITY_TAGS)))
        time_tags = random.sample(TIME_TAGS, min(1, len(TIME_TAGS)))

        all_tags = game_tags + service_tags + personality_tags + time_tags

        good_rate = random.uniform(0.85, 0.99)
        order_count = random.randint(50, 500)
        hour_count = random.randint(100, 2000)
        status = "online"

        intro_templates = [f"{game}{level}段位，擅长{','.join(game_tags[:2])}，性格{personality_tags[0]}，欢迎预约～", f"专业{game}陪玩，{level}水平，{service_tags[0]}，{personality_tags[0]}，期待和你一起玩！", f"{voice}声线，{game}高手，{game_tags[0]}，{service_tags[0]}，快来找我吧～", f"{game}{level}，{','.join(all_tags[:3])}，{personality_tags[0]}，保证服务质量！", f"{time_tags[0]}，{game}专精，{level}段位，{personality_tags[0]}，带你轻松上分！"]
        introduction = random.choice(intro_templates)

        partners.append({
            "partner_id": partner_id,
            "user_id": partner_id,
            "game": game,
            "level": level,
            "price": price,
            "voice": voice,
            "status": status,
            "audit_status": "pass",
            "good_rate": good_rate,
            "order_count": order_count,
            "hour_count": hour_count,
            "avatar": get_avatar_url(f"partner{partner_id}"),
            "similar_ids": random.sample([p for p in partner_ids if p != partner_id], min(5, PARTNER_COUNT-1)),
            "introduction": introduction,
            "tags": all_tags,
            "game_tags": game_tags,
            "service_tags": service_tags,
            "personality_tags": personality_tags,
            "time_tags": time_tags,
            "create_time": f"2024-01-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })

    with open(os.path.join(DATA_PATH, "partner.json"), "w", encoding="utf-8") as f:
        json.dump(partners, f, ensure_ascii=False, indent=2)
    print(f"[OK] 陪玩数据已创建 ({len(partners)}个陪玩师)")

def init_tags():
    tags = []
    for i in range(2, 22):
        game = random.choice(GAMES)
        budget = random.randint(40, 120)
        voice_type = random.choice(["不限"] + VOICE_TYPES[:5])
        tags.append({
            "user_id": i,
            "game": game,
            "budget": budget,
            "voice_type": voice_type,
            "history": random.sample(range(PARTNER_START_ID, PARTNER_END_ID), min(5, PARTNER_COUNT)),
            "preferences": random.sample(SERVICE_TAGS[:10], min(3, 10)),
            "update_time": f"2024-06-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })

    with open(os.path.join(DATA_PATH, "tag.json"), "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    print(f"[OK] 用户画像标签已创建 ({len(tags)}个)")

def init_orders():
    orders = []
    order_id = 1
    partners_data = json.load(open(os.path.join(DATA_PATH, "partner.json"), "r", encoding="utf-8"))

    for _ in range(150):
        player_id = random.randint(2, 21)
        partner_id = random.randint(PARTNER_START_ID, PARTNER_END_ID - 1)
        hours = random.randint(1, 5)

        partner_data = None
        for p in partners_data:
            if p["partner_id"] == partner_id:
                partner_data = p
                break

        if partner_data:
            total_price = hours * partner_data["price"]
            game = partner_data["game"]

            if random.random() < 0.9:
                status = random.choice(["rated", "completed"])
                create_time = f"2024-{random.randint(1,5):02d}-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
                rating = random.randint(4, 5) if status == "rated" else 0
                comment = random.choice(["技术很厉害，带我轻松上分！", "声音好听，聊天很开心～", "耐心指导，学到了很多技巧！", "服务态度很好，下次还会来！", "专业靠谱，强烈推荐！", "幽默风趣，游戏体验极佳！", "温柔体贴，很满意这次服务！", "反应快速，配合默契！", ""]) if status == "rated" else ""
            else:
                status = random.choice(["paid", "in_progress"])
                create_time = f"2024-06-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
                rating = 0
                comment = ""

            orders.append({
                "order_id": order_id,
                "player_id": player_id,
                "partner_id": partner_id,
                "hours": hours,
                "game": game,
                "total_price": total_price,
                "status": status,
                "create_time": create_time,
                "pay_time": create_time,
                "start_time": create_time,
                "end_time": create_time,
                "comment": comment,
                "rating": rating
            })
            order_id += 1

    with open(os.path.join(DATA_PATH, "order.json"), "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)
    print(f"[OK] 订单数据已创建 ({len(orders)}个订单)")

def init_evaluates():
    evaluates = []
    evaluate_id = 1
    orders = json.load(open(os.path.join(DATA_PATH, "order.json"), "r", encoding="utf-8"))
    users = json.load(open(os.path.join(DATA_PATH, "user.json"), "r", encoding="utf-8"))

    for o in orders:
        if o["status"] == "rated" and o["rating"] > 0:
            player_name = None
            for u in users:
                if u["user_id"] == o["player_id"]:
                    player_name = u["username"]
                    break

            if player_name:
                evaluates.append({
                    "id": evaluate_id,
                    "order_id": o["order_id"],
                    "player_id": o["player_id"],
                    "partner_id": o["partner_id"],
                    "username": player_name,
                    "rating": o["rating"],
                    "content": o["comment"],
                    "create_time": o["create_time"]
                })
                evaluate_id += 1

    with open(os.path.join(DATA_PATH, "evaluate.json"), "w", encoding="utf-8") as f:
        json.dump(evaluates, f, ensure_ascii=False, indent=2)
    print(f"[OK] 评价数据已创建 ({len(evaluates)}条)")

def init_favorites():
    favorites = []
    favorite_id = 1

    for player_id in range(2, 22):
        favorite_count = random.randint(3, 8)
        favorite_partners = random.sample(range(PARTNER_START_ID, PARTNER_END_ID), min(favorite_count, PARTNER_COUNT))

        for partner_id in favorite_partners:
            favorites.append({
                "id": favorite_id,
                "user_id": player_id,
                "partner_id": partner_id,
                "create_time": f"2024-{random.randint(1,5):02d}-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
            })
            favorite_id += 1

    with open(os.path.join(DATA_PATH, "favorite.json"), "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)
    print(f"[OK] 收藏数据已创建 ({len(favorites)}条)")

def init_messages():
    messages = [
        {"id": 1, "type": "system", "title": "平台上线公告", "content": "AI智能陪玩推荐平台正式上线！快来体验智能匹配功能吧～", "create_time": "2024-01-01 10:00:00"},
        {"id": 2, "type": "system", "title": "新年活动", "content": "新年充值优惠活动：充值满100送20，快来参与吧！", "create_time": "2024-01-20 12:00:00"},
        {"id": 3, "type": "system", "title": "陪玩招募", "content": "招募优质陪玩师！高收入、灵活时间，欢迎入驻～", "create_time": "2024-02-01 09:00:00"},
        {"id": 4, "type": "system", "title": "AI推荐升级", "content": "AI推荐算法升级完成，匹配更精准，快来体验！", "create_time": "2024-03-15 14:00:00"}
    ]

    with open(os.path.join(DATA_PATH, "message.json"), "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("[OK] 消息数据已创建")

def init_token_cache():
    with open(os.path.join(DATA_PATH, "token_cache.json"), "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("[OK] Token缓存已创建")

def init_other_files():
    other_files = ["recharge.json", "withdraw.json", "complaint.json", "feedback.json", "forum_posts.json", "forum_comments.json", "chat_sessions.json", "chat_messages.json"]
    for file_name in other_files:
        with open(os.path.join(DATA_PATH, file_name), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    print("[OK] 其他数据文件已创建")

def init_forum_data():
    posts = [
        {
            "id": 1,
            "user_id": 2,
            "author": "游戏达人小明",
            "avatar": get_avatar_url("游戏达人小明"),
            "title": "英雄联盟上分攻略：如何成为野区霸主",
            "category": "游戏攻略",
            "content": "大家好，今天给大家分享一下我在英雄联盟中的打野心得。\n\n首先，选择适合版本的英雄很重要。当前版本强势的打野英雄有：\n1. 盲僧 - 前期节奏之王\n2. 赵信 - 野区霸主\n3. 莉莉娅 - 团战利器\n\n其次，刷野路线也很关键。蓝开还是红开取决于队友和对方打野位置。\n\n最重要的是，多观察小地图，及时支援队友，掌握好龙和先锋的时间点。\n\n希望这些技巧能帮助大家早日上王者！",
            "views": 1256,
            "replies": 45,
            "likes": 189,
            "create_time": "2024-06-20 14:30:00"
        },
        {
            "id": 2,
            "user_id": 3,
            "author": "电竞少女小红",
            "avatar": get_avatar_url("电竞少女小红"),
            "title": "周末组队开黑！寻找靠谱队友",
            "category": "组队开黑",
            "content": "周末无聊，想找几个队友一起玩英雄联盟或者王者荣耀！\n\n本人段位：英雄联盟钻石，王者荣耀星耀\n擅长位置：中单、ADC\n在线时间：周六周日全天\n\n希望找到技术不错、心态好的队友，一起上分！\n有意向的小伙伴可以私信我或者在评论区留言～",
            "views": 892,
            "replies": 32,
            "likes": 67,
            "create_time": "2024-06-21 10:15:00"
        },
        {
            "id": 3,
            "user_id": 5,
            "author": "上分狂人阿强",
            "avatar": get_avatar_url("上分狂人阿强"),
            "title": "陪玩体验分享：王者大神阿强真的很强！",
            "category": "陪玩评价",
            "content": "昨天找了王者大神阿强陪玩，体验真的超级棒！\n\n首先，他的技术确实没得说，各种秀操作，带我轻松上分。\n其次，沟通能力很强，会耐心指导我如何走位、如何打团。\n最重要的是，态度很好，没有任何不耐烦，还会讲笑话活跃气氛。\n\n价格也很合理，性价比超高！强烈推荐给大家！\n打5星好评！",
            "views": 1567,
            "replies": 56,
            "likes": 234,
            "create_time": "2024-06-22 16:45:00"
        },
        {
            "id": 4,
            "user_id": 7,
            "author": "新手玩家小张",
            "avatar": get_avatar_url("新手玩家小张"),
            "title": "建议平台增加新手指导专区",
            "category": "平台建议",
            "content": "作为一个游戏新手，我觉得平台可以考虑增加一个新手指导专区。\n\n理由如下：\n1. 新手玩家很多，但是不知道如何选择陪玩\n2. 缺少入门教学内容\n3. 新手容易被坑，需要更多保护\n\n建议：\n- 增加新手专用陪玩分类\n- 提供游戏入门指南\n- 设置新手保护机制\n\n希望平台越办越好！",
            "views": 678,
            "replies": 28,
            "likes": 98,
            "create_time": "2024-06-23 09:20:00"
        },
        {
            "id": 5,
            "user_id": 9,
            "author": "周末玩家小周",
            "avatar": get_avatar_url("周末玩家小周"),
            "title": "闲聊：大家平时都喜欢玩什么游戏？",
            "category": "闲聊灌水",
            "content": "无聊来水一贴，大家平时都喜欢玩什么游戏呢？\n\n我先来：\n- 英雄联盟（主玩）\n- 王者荣耀（偶尔玩）\n- 原神（佛系玩）\n\n最近想入坑CS2，有没有大佬带带？\n大家也来分享一下自己喜欢的游戏吧～",
            "views": 1123,
            "replies": 89,
            "likes": 156,
            "create_time": "2024-06-24 20:30:00"
        },
        {
            "id": 6,
            "user_id": 11,
            "author": "技术流玩家阿杰",
            "avatar": get_avatar_url("技术流玩家阿杰"),
            "title": "CS2进阶技巧：如何提高枪法命中率",
            "category": "游戏攻略",
            "content": "分享一些CS2提高枪法的技巧：\n\n1. 练习瞄准：每天坚持aimbotz练习30分钟\n2. 预瞄：熟悉地图，提前瞄准常见点位\n3. 急停：射击前一定要急停\n4. 压枪：不同枪械有不同的压枪方式\n5. 反应速度：多打死亡竞赛提升反应\n\n建议每天练习，坚持一个月必有提升！\n附上我的灵敏度设置供大家参考：\n鼠标灵敏度：1.5\nDPI：800\n\n祝大家早日成为爆头大师！",
            "views": 2345,
            "replies": 78,
            "likes": 345,
            "create_time": "2024-06-25 15:00:00"
        },
        {
            "id": 7,
            "user_id": 13,
            "author": "上分型玩家小刚",
            "avatar": get_avatar_url("上分型玩家小刚"),
            "title": "原神深渊通关攻略：配队思路分享",
            "category": "游戏攻略",
            "content": "给大家分享一下原神深渊通关的配队思路：\n\n热门配队：\n1. 神鹤万心 - 永冻队天花板\n2. 激化队 - 低成本高输出\n3. 胡行钟夜 - 老牌强势队\n4. 雷国 - 简单暴力\n\n关键要点：\n- 元素反应很重要\n- 练度够了再打\n- 多看攻略学习手法\n\n祝大家早日满星深渊！",
            "views": 1876,
            "replies": 67,
            "likes": 267,
            "create_time": "2024-06-26 11:30:00"
        },
        {
            "id": 8,
            "user_id": 15,
            "author": "全能玩家小吴",
            "avatar": get_avatar_url("全能玩家小吴"),
            "title": "和平精英钢枪技巧：如何成为淘汰王",
            "category": "游戏攻略",
            "content": "分享和平精英钢枪技巧：\n\n1. 落点选择：选资源丰富但人相对少的地方\n2. 枪械选择：M416配M249是最佳组合\n3. 身法技巧：拜佛枪法、闪身枪、提前枪\n4. 听声辨位：戴耳机很重要\n5. 载具运用：学会开车打架\n\n最重要的还是多练，熟能生巧！\n祝大家每局都能吃鸡！",
            "views": 1456,
            "replies": 54,
            "likes": 198,
            "create_time": "2024-06-27 13:45:00"
        },
        {
            "id": 9,
            "user_id": 17,
            "author": "王者玩家小林",
            "avatar": get_avatar_url("王者玩家小林"),
            "title": "王者荣耀新版本更新解读",
            "category": "游戏攻略",
            "content": "新版本更新了很多内容，给大家解读一下：\n\n英雄调整：\n- 李白增强：大招伤害提高\n- 韩信削弱：前期攻速降低\n- 貂蝉调整：二技能CD优化\n\n装备改动：\n- 新装备上架\n- 部分装备属性调整\n\n地图变化：\n- 野区刷新时间调整\n- 防御塔机制优化\n\n建议大家多打匹配适应新版本，祝大家早日上王者！",
            "views": 987,
            "replies": 43,
            "likes": 123,
            "create_time": "2024-06-28 09:00:00"
        },
        {
            "id": 10,
            "user_id": 19,
            "author": "吃鸡玩家小黄",
            "avatar": get_avatar_url("吃鸡玩家小黄"),
            "title": "绝地求生新手入门指南",
            "category": "游戏攻略",
            "content": "给新手玩家的绝地求生入门指南：\n\n1. 跳伞技巧：学会控制落点\n2. 搜物资：优先捡武器和护甲\n3. 跑毒：提前规划路线\n4. 战斗：利用地形优势\n5. 决赛圈：保持耐心\n\n常用按键：\n- WASD移动\n- 鼠标右键开镜\n- R换弹\n- F捡东西\n\n新手建议先从第三人称开始，熟悉后再尝试第一人称。\n祝大家早日吃鸡！",
            "views": 2134,
            "replies": 89,
            "likes": 312,
            "create_time": "2024-06-28 17:20:00"
        }
    ]

    comments = [
        {"id": 1, "post_id": 1, "user_id": 3, "author": "电竞少女小红", "avatar": get_avatar_url("电竞少女小红"), "content": "学到了！谢谢分享！", "create_time": "2024-06-20 15:00:00"},
        {"id": 2, "post_id": 1, "user_id": 5, "author": "上分狂人阿强", "avatar": get_avatar_url("上分狂人阿强"), "content": "盲僧玩家来报道，确实很实用！", "create_time": "2024-06-20 15:30:00"},
        {"id": 3, "post_id": 2, "user_id": 7, "author": "新手玩家小张", "avatar": get_avatar_url("新手玩家小张"), "content": "带我一个！我玩辅助", "create_time": "2024-06-21 11:00:00"},
        {"id": 4, "post_id": 3, "user_id": 9, "author": "周末玩家小周", "avatar": get_avatar_url("周末玩家小周"), "content": "我也找过他，确实很不错！", "create_time": "2024-06-22 17:00:00"},
        {"id": 5, "post_id": 5, "user_id": 11, "author": "技术流玩家阿杰", "avatar": get_avatar_url("技术流玩家阿杰"), "content": "CS2欢迎你！", "create_time": "2024-06-24 21:00:00"},
        {"id": 6, "post_id": 5, "user_id": 13, "author": "上分型玩家小刚", "avatar": get_avatar_url("上分型玩家小刚"), "content": "原神玩家+1", "create_time": "2024-06-24 21:30:00"},
        {"id": 7, "post_id": 6, "user_id": 15, "author": "全能玩家小吴", "avatar": get_avatar_url("全能玩家小吴"), "content": "灵敏度设置很有用，谢谢！", "create_time": "2024-06-25 16:00:00"},
        {"id": 8, "post_id": 7, "user_id": 17, "author": "王者玩家小林", "avatar": get_avatar_url("王者玩家小林"), "content": "神鹤万心永远滴神！", "create_time": "2024-06-26 12:00:00"},
        {"id": 9, "post_id": 8, "user_id": 19, "author": "吃鸡玩家小黄", "avatar": get_avatar_url("吃鸡玩家小黄"), "content": "M416确实好用！", "create_time": "2024-06-27 14:30:00"},
        {"id": 10, "post_id": 10, "user_id": 2, "author": "游戏达人小明", "avatar": get_avatar_url("游戏达人小明"), "content": "新手必备！收藏了", "create_time": "2024-06-28 18:00:00"}
    ]

    with open(os.path.join(DATA_PATH, "forum_posts.json"), "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"[OK] 论坛帖子数据已创建 ({len(posts)}条)")

    with open(os.path.join(DATA_PATH, "forum_comments.json"), "w", encoding="utf-8") as f:
        json.dump(comments, f, ensure_ascii=False, indent=2)
    print(f"[OK] 论坛评论数据已创建 ({len(comments)}条)")

def init_chat_data():
    chat_sessions = [
        {"id": 1, "user_id": 2, "partner_id": 22, "last_message": "你好！请问现在可以预约吗？", "last_time": "2024-06-28 19:30:00", "unread_count": 1},
        {"id": 2, "user_id": 2, "partner_id": 25, "last_message": "好的，明天晚上8点见！", "last_time": "2024-06-28 18:45:00", "unread_count": 0},
        {"id": 3, "user_id": 3, "partner_id": 28, "last_message": "感谢你的陪伴，下次还找你！", "last_time": "2024-06-27 22:15:00", "unread_count": 0},
        {"id": 4, "user_id": 5, "partner_id": 30, "last_message": "收到，马上上线！", "last_time": "2024-06-28 20:00:00", "unread_count": 2},
        {"id": 5, "user_id": 7, "partner_id": 35, "last_message": "今天玩得很开心！", "last_time": "2024-06-26 23:30:00", "unread_count": 0},
        {"id": 6, "user_id": 4, "partner_id": 32, "last_message": "没问题，随时可以开始", "last_time": "2024-06-28 15:20:00", "unread_count": 1},
        {"id": 7, "user_id": 6, "partner_id": 38, "last_message": "好的，我这就上线", "last_time": "2024-06-28 17:45:00", "unread_count": 0},
        {"id": 8, "user_id": 8, "partner_id": 40, "last_message": "期待和你一起玩！", "last_time": "2024-06-27 14:30:00", "unread_count": 0},
        {"id": 9, "user_id": 9, "partner_id": 42, "last_message": "可以的，价格不变", "last_time": "2024-06-28 12:10:00", "unread_count": 3},
        {"id": 10, "user_id": 10, "partner_id": 45, "last_message": "非常满意这次服务！", "last_time": "2024-06-26 20:00:00", "unread_count": 0},
        {"id": 11, "user_id": 2, "partner_id": 48, "last_message": "加个好友吧！", "last_time": "2024-06-28 21:00:00", "unread_count": 1},
        {"id": 12, "user_id": 3, "partner_id": 50, "last_message": "明天继续！", "last_time": "2024-06-27 23:50:00", "unread_count": 0}
    ]

    chat_messages = [
        {"id": 1, "chat_id": 1, "sender_id": 2, "content": "你好！请问现在可以预约吗？", "time": "2024-06-28 19:30:00"},
        {"id": 2, "chat_id": 1, "sender_id": 22, "content": "可以的，请问你想玩什么游戏？", "time": "2024-06-28 19:31:00"},
        {"id": 3, "chat_id": 1, "sender_id": 22, "content": "我现在在线，可以马上开始", "time": "2024-06-28 19:32:00"},
        {"id": 4, "chat_id": 2, "sender_id": 2, "content": "明天晚上8点有空吗？", "time": "2024-06-28 18:40:00"},
        {"id": 5, "chat_id": 2, "sender_id": 25, "content": "好的，明天晚上8点见！", "time": "2024-06-28 18:45:00"},
        {"id": 6, "chat_id": 3, "sender_id": 3, "content": "今天辛苦了！", "time": "2024-06-27 22:10:00"},
        {"id": 7, "chat_id": 3, "sender_id": 28, "content": "不客气，玩得开心！", "time": "2024-06-27 22:12:00"},
        {"id": 8, "chat_id": 3, "sender_id": 3, "content": "感谢你的陪伴，下次还找你！", "time": "2024-06-27 22:15:00"},
        {"id": 9, "chat_id": 4, "sender_id": 5, "content": "在吗？想找你陪玩", "time": "2024-06-28 19:55:00"},
        {"id": 10, "chat_id": 4, "sender_id": 30, "content": "在的，什么游戏？", "time": "2024-06-28 19:56:00"},
        {"id": 11, "chat_id": 4, "sender_id": 5, "content": "王者荣耀，上星耀", "time": "2024-06-28 19:58:00"},
        {"id": 12, "chat_id": 4, "sender_id": 30, "content": "收到，马上上线！", "time": "2024-06-28 20:00:00"},
        {"id": 13, "chat_id": 5, "sender_id": 7, "content": "今天玩得很开心！", "time": "2024-06-26 23:30:00"},
        {"id": 14, "chat_id": 5, "sender_id": 35, "content": "谢谢，期待下次合作！", "time": "2024-06-26 23:35:00"},
        {"id": 15, "chat_id": 6, "sender_id": 4, "content": "你好，想约个陪玩", "time": "2024-06-28 15:15:00"},
        {"id": 16, "chat_id": 6, "sender_id": 32, "content": "没问题，随时可以开始", "time": "2024-06-28 15:20:00"},
        {"id": 17, "chat_id": 7, "sender_id": 6, "content": "现在有空吗？", "time": "2024-06-28 17:40:00"},
        {"id": 18, "chat_id": 7, "sender_id": 38, "content": "好的，我这就上线", "time": "2024-06-28 17:45:00"},
        {"id": 19, "chat_id": 8, "sender_id": 8, "content": "周末一起玩？", "time": "2024-06-27 14:25:00"},
        {"id": 20, "chat_id": 8, "sender_id": 40, "content": "期待和你一起玩！", "time": "2024-06-27 14:30:00"},
        {"id": 21, "chat_id": 9, "sender_id": 9, "content": "可以便宜一点吗？", "time": "2024-06-28 12:05:00"},
        {"id": 22, "chat_id": 9, "sender_id": 42, "content": "可以的，价格不变", "time": "2024-06-28 12:10:00"},
        {"id": 23, "chat_id": 9, "sender_id": 42, "content": "现在在线吗？", "time": "2024-06-28 12:15:00"},
        {"id": 24, "chat_id": 9, "sender_id": 42, "content": "我准备好了", "time": "2024-06-28 12:20:00"},
        {"id": 25, "chat_id": 10, "sender_id": 10, "content": "非常满意这次服务！", "time": "2024-06-26 20:00:00"},
        {"id": 26, "chat_id": 10, "sender_id": 45, "content": "感谢好评！", "time": "2024-06-26 20:05:00"},
        {"id": 27, "chat_id": 11, "sender_id": 2, "content": "加个好友吧！", "time": "2024-06-28 21:00:00"},
        {"id": 28, "chat_id": 11, "sender_id": 48, "content": "好的，游戏里加你", "time": "2024-06-28 21:05:00"},
        {"id": 29, "chat_id": 12, "sender_id": 3, "content": "今天玩得很愉快", "time": "2024-06-27 23:45:00"},
        {"id": 30, "chat_id": 12, "sender_id": 50, "content": "明天继续！", "time": "2024-06-27 23:50:00"}
    ]

    with open(os.path.join(DATA_PATH, "chat_sessions.json"), "w", encoding="utf-8") as f:
        json.dump(chat_sessions, f, ensure_ascii=False, indent=2)
    print(f"[OK] 聊天会话数据已创建 ({len(chat_sessions)}条)")

    with open(os.path.join(DATA_PATH, "chat_messages.json"), "w", encoding="utf-8") as f:
        json.dump(chat_messages, f, ensure_ascii=False, indent=2)
    print(f"[OK] 聊天消息数据已创建 ({len(chat_messages)}条)")

if __name__ == "__main__":
    init_all_data()
    init_forum_data()
    init_chat_data()