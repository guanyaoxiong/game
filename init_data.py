import json
import os
import random
import time

DATA_PATH = "data/"

# 标签库定义
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

def init_all_data():
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
    
    print("[INFO] 开始创建50个数据样本...")
    
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
    users = [
        {
            "user_id": 1,
            "username": "admin",
            "password": "admin123",
            "phone": "18888888888",
            "balance": 0.0,
            "role": "admin",
            "status": "active",
            "create_time": "2024-01-01 10:00:00"
        }
    ]
    
    # 创建20个玩家
    player_names = [
        "游戏达人小明", "电竞少女小红", "硬核玩家老王", "休闲玩家小李", "上分狂人阿强",
        "娱乐玩家小美", "新手玩家小张", "资深玩家老刘", "周末玩家小周", "通宵玩家小赵",
        "技术流玩家阿杰", "聊天型玩家小雪", "上分型玩家小刚", "娱乐型玩家小芳", "全能玩家小吴",
        "LOL玩家小陈", "王者玩家小林", "吃鸡玩家小黄", "原神玩家小徐", "CS玩家小马"
    ]
    
    for i, name in enumerate(player_names, start=2):
        users.append({
            "user_id": i,
            "username": name,
            "password": "123456",
            "phone": f"1380013{str(i).zfill(4)}",
            "balance": random.randint(100, 1000),
            "role": "player",
            "status": "active",
            "create_time": f"2024-01-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })
    
    # 创建30个陪玩师
    partner_names = [
        "王者大神阿强", "甜美声线小雪", "LOL职业选手", "温柔御姐小月", "吃鸡高手阿龙",
        "元气少女小樱", "技术流阿杰", "萝莉音小萌", "大叔音老张", "磁性音阿文",
        "打野王者小虎", "辅助天使小丽", "中单法师小云", "ADC射手小风", "上单战士小雷",
        "全能选手小星", "聊天达人小柔", "上分神器小霸", "新手导师小师", "娱乐陪玩小乐",
        "通宵达人小夜", "周末特供小周", "快速响应小快", "耐心陪伴小温", "幽默风趣小趣",
        "原神大佬小神", "CS高手小枪", "和平精英小和", "绝地求生小绝", "多游戏全能小全"
    ]
    
    for i, name in enumerate(partner_names, start=22):
        users.append({
            "user_id": i,
            "username": name,
            "password": "123456",
            "phone": f"1390013{str(i).zfill(4)}",
            "balance": 0.0,
            "role": "partner",
            "status": "active",
            "create_time": f"2024-01-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })
    
    with open(os.path.join(DATA_PATH, "user.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
    print(f"[OK] 用户数据已创建 ({len(users)}个用户: 1管理员 + 20玩家 + 30陪玩)")

def init_partners():
    partners = []
    partner_ids = range(22, 52)  # 30个陪玩师
    
    for i, partner_id in enumerate(partner_ids):
        game = random.choice(GAMES)
        level = random.choice(LEVELS[game])
        voice = random.choice(VOICE_TYPES)
        price = random.randint(30, 150)
        
        # 选择游戏相关标签
        game_tags = random.sample(GAME_TAGS[game], min(3, len(GAME_TAGS[game])))
        # 选择服务标签
        service_tags = random.sample(SERVICE_TAGS, min(2, len(SERVICE_TAGS)))
        # 选择性格标签
        personality_tags = random.sample(PERSONALITY_TAGS, min(2, len(PERSONALITY_TAGS)))
        # 选择时间标签
        time_tags = random.sample(TIME_TAGS, min(1, len(TIME_TAGS)))
        
        all_tags = game_tags + service_tags + personality_tags + time_tags
        
        good_rate = random.uniform(0.85, 0.99)
        order_count = random.randint(50, 500)
        hour_count = random.randint(100, 2000)
        
        status = random.choice(["online", "online", "online", "offline"])  # 75%在线
        audit_status = "pass"
        
        # 生成个人介绍
        intro_templates = [
            f"{game}{level}段位，擅长{','.join(game_tags[:2])}，性格{personality_tags[0]}，欢迎预约～",
            f"专业{game}陪玩，{level}水平，{service_tags[0]}，{personality_tags[0]}，期待和你一起玩！",
            f"{voice}声线，{game}高手，{game_tags[0]}，{service_tags[0]}，快来找我吧～",
            f"{game}{level}，{','.join(all_tags[:3])}，{personality_tags[0]}，保证服务质量！",
            f"{time_tags[0]}，{game}专精，{level}段位，{personality_tags[0]}，带你轻松上分！"
        ]
        introduction = random.choice(intro_templates)
        
        partners.append({
            "partner_id": partner_id,
            "user_id": partner_id,
            "game": game,
            "level": level,
            "price": price,
            "voice": voice,
            "status": status,
            "audit_status": audit_status,
            "good_rate": good_rate,
            "order_count": order_count,
            "hour_count": hour_count,
            "similar_ids": random.sample([p for p in partner_ids if p != partner_id], min(5, 29)),
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
    
    # 为20个玩家创建画像
    for i in range(2, 22):
        game = random.choice(GAMES)
        budget = random.randint(40, 120)
        voice_type = random.choice(["不限"] + VOICE_TYPES[:5])
        
        tags.append({
            "user_id": i,
            "game": game,
            "budget": budget,
            "voice_type": voice_type,
            "history": random.sample(range(22, 52), min(5, 30)),
            "preferences": random.sample(SERVICE_TAGS[:10], min(3, 10)),
            "update_time": f"2024-06-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
        })
    
    with open(os.path.join(DATA_PATH, "tag.json"), "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=2)
    print(f"[OK] 用户画像标签已创建 ({len(tags)}个)")

def init_orders():
    orders = []
    order_id = 1
    
    # 创建大量历史订单
    for _ in range(100):
        player_id = random.randint(2, 21)
        partner_id = random.randint(22, 51)
        hours = random.randint(1, 5)
        
        partner_data = None
        for p in json.load(open(os.path.join(DATA_PATH, "partner.json"), "r", encoding="utf-8")):
            if p["partner_id"] == partner_id:
                partner_data = p
                break
        
        if partner_data:
            total_price = hours * partner_data["price"]
            game = partner_data["game"]
            
            # 90%的订单已完成
            if random.random() < 0.9:
                status = random.choice(["rated", "completed"])
                create_time = f"2024-{random.randint(1,5):02d}-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
                pay_time = create_time
                start_time = create_time
                end_time = create_time
                rating = random.randint(4, 5) if status == "rated" else 0
                comment = random.choice([
                    "技术很厉害，带我轻松上分！",
                    "声音好听，聊天很开心～",
                    "耐心指导，学到了很多技巧！",
                    "服务态度很好，下次还会来！",
                    "专业靠谱，强烈推荐！",
                    "幽默风趣，游戏体验极佳！",
                    "温柔体贴，很满意这次服务！",
                    "反应快速，配合默契！",
                    ""
                ]) if status == "rated" else ""
            else:
                status = random.choice(["paid", "in_progress"])
                create_time = f"2024-06-{random.randint(1,28):02d} {random.randint(8,22):02d}:{random.randint(0,59):02d}:00"
                pay_time = create_time if status == "paid" else None
                start_time = create_time if status == "in_progress" else None
                end_time = None
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
                "pay_time": pay_time,
                "start_time": start_time,
                "end_time": end_time,
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
    
    # 每个玩家收藏2-5个陪玩
    for player_id in range(2, 22):
        favorite_count = random.randint(2, 5)
        favorite_partners = random.sample(range(22, 52), favorite_count)
        
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
        {
            "id": 1,
            "type": "system",
            "title": "平台上线公告",
            "content": "AI智能陪玩推荐平台正式上线！快来体验智能匹配功能吧～",
            "create_time": "2024-01-01 10:00:00"
        },
        {
            "id": 2,
            "type": "system",
            "title": "新年活动",
            "content": "新年充值优惠活动：充值满100送20，快来参与吧！",
            "create_time": "2024-01-20 12:00:00"
        },
        {
            "id": 3,
            "type": "system",
            "title": "陪玩招募",
            "content": "招募优质陪玩师！高收入、灵活时间，欢迎入驻～",
            "create_time": "2024-02-01 09:00:00"
        },
        {
            "id": 4,
            "type": "system",
            "title": "AI推荐升级",
            "content": "AI推荐算法升级完成，匹配更精准，快来体验！",
            "create_time": "2024-03-15 14:00:00"
        }
    ]
    
    with open(os.path.join(DATA_PATH, "message.json"), "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
    print("[OK] 消息数据已创建")

def init_token_cache():
    with open(os.path.join(DATA_PATH, "token_cache.json"), "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    print("[OK] Token缓存已创建")

def init_other_files():
    other_files = ["recharge.json", "withdraw.json", "complaint.json"]
    for file_name in other_files:
        with open(os.path.join(DATA_PATH, file_name), "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    print("[OK] 其他数据文件已创建")

if __name__ == "__main__":
    init_all_data()