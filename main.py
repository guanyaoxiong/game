import http.server
import urllib.parse
import json
import os
import time
from urllib.parse import urlparse, parse_qs

from utils.response import json_response, html_response
from utils.json_db import read_json, write_json, get_next_id
from service.auth_service import player_register, partner_register, login, verify_token, logout, get_user_info
from service.recommend_ai import get_home_recommend, get_similar_partners, wish_match, record_behavior
from service.partner_service import get_partner_list, get_partner_detail, update_partner_status, get_partner_revenue, apply_withdraw, update_partner_info
from service.order_service import create_order, get_order_list, update_order_status, add_order_comment, apply_refund, handle_refund as admin_handle_refund
from service.player_service import add_favorite, remove_favorite, get_favorite_list, recharge, get_game_list, get_voice_list
from service.admin_service import audit_partner, get_pending_partners, get_statistics

from template.home_html import get_home_page
from template.partner_html import get_partner_list_page, get_partner_detail_page
from template.auth_html import get_login_page, get_register_page
from template.center_html import get_center_page
from template.wish_html import get_wish_page
from template.admin_html import get_admin_page
from template.workspace_html import get_workspace_page
from template.feedback_html import get_feedback_page
from template.forum_html import get_forum_page, get_post_detail_page
from template.chat_html import get_chat_page

PORT = 8080

GUEST_USER_ID = 999

def get_or_create_guest_user():
    users = read_json("user.json")
    guest_exists = any(u["user_id"] == GUEST_USER_ID for u in users)
    if not guest_exists:
        guest_user = {
            "user_id": GUEST_USER_ID,
            "username": "游客",
            "password": "",
            "phone": "00000000000",
            "balance": 10000.0,
            "role": "player",
            "status": "active",
            "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=guest",
            "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        users.append(guest_user)
        write_json("user.json", users)

        tags = read_json("tag.json")
        tags.append({
            "user_id": GUEST_USER_ID,
            "game": "英雄联盟",
            "budget": 80,
            "voice_type": "不限",
            "history": [],
            "preferences": [],
            "update_time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        write_json("tag.json", tags)
    return GUEST_USER_ID

def get_token_from_request(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization'].replace('Bearer ', '')
    return None

def get_user_id_from_token_or_guest(request):
    token = get_token_from_request(request)
    if token:
        user_data = verify_token(token)
        if user_data:
            return user_data["user_id"], user_data["user_type"]
    guest_id = get_or_create_guest_user()
    return guest_id, "player"

def handle_route(method, path, query_params, body, request):
    if path == '/':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)
        recommend_list = get_home_recommend(user_id) if user_type == "player" else []
        hot_partners = get_partner_list(sort_by="good_rate")[:6]
        return html_response(get_home_page(user_info, recommend_list, hot_partners))

    elif path == '/login':
        return html_response(get_login_page())

    elif path == '/register':
        return html_response(get_register_page())

    elif path == '/partners':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        game = query_params.get('game', [''])[0]
        voice = query_params.get('voice', [''])[0]
        price_min = query_params.get('price_min', [''])[0]
        price_max = query_params.get('price_max', [''])[0]
        sort_by = query_params.get('sort', ['match'])[0]

        price_min = float(price_min) if price_min else None
        price_max = float(price_max) if price_max else None

        partners = get_partner_list(game=game or None, voice=voice or None,
                                   price_min=price_min, price_max=price_max, sort_by=sort_by)
        games = get_game_list()
        voices = get_voice_list()

        return html_response(get_partner_list_page(user_info, partners, games, voices))

    elif path.startswith('/partner/'):
        try:
            partner_id = int(path.split('/')[-1])
        except:
            return json_response(400, "无效的陪玩ID")

        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)
        favorites = get_favorite_list(user_id)
        is_favorite = any(f["partner_id"] == partner_id for f in favorites)

        partner = get_partner_detail(partner_id)
        if not partner:
            return html_response("<h1>陪玩不存在</h1>")

        similar_partners = get_similar_partners(partner_id)

        if user_type == "player":
            record_behavior(user_id, partner_id, "view")

        return html_response(get_partner_detail_page(user_info, partner, similar_partners, is_favorite))

    elif path == '/center':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        orders = get_order_list(user_id, user_type)
        favorites = []
        revenue = None

        if user_type == "player":
            favorites = get_favorite_list(user_id)
        else:
            revenue = get_partner_revenue(user_id)

        return html_response(get_center_page(user_info, orders, favorites, revenue))

    elif path == '/wish':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        game = query_params.get('game', [''])[0]
        budget_min = query_params.get('budget_min', ['0'])[0]
        budget_max = query_params.get('budget_max', ['9999'])[0]
        voice = query_params.get('voice', ['不限'])[0]

        results = []
        if game:
            budget_min = float(budget_min)
            budget_max = float(budget_max)
            results = wish_match(user_id, game, budget_min, budget_max, voice)

        games = get_game_list()
        voices_list = [v for v in get_voice_list()]

        return html_response(get_wish_page(user_info, games, voices_list, results))

    elif path == '/partner/workspace':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        if user_type != "partner":
            partner_info = get_partner_detail(user_id)
            if not partner_info:
                partner_info = {"partner_id": user_id, "game": "英雄联盟", "level": "钻石", "price": 50, "voice": "磁性音", "status": "online", "good_rate": 0.95, "order_count": 0, "hour_count": 0, "introduction": "游客陪玩师"}
        else:
            partner_info = get_partner_detail(user_id)

        orders = get_order_list(user_id, "partner")

        return html_response(get_workspace_page(user_info, partner_info, orders))

    elif path == '/admin':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        statistics = get_statistics()
        pending_partners = get_pending_partners()
        pending_refunds = []

        return html_response(get_admin_page(statistics, pending_partners, pending_refunds))

    elif path == '/feedback':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        feedback_list = []
        feedbacks = read_json("feedback.json")
        for fb in feedbacks:
            if fb.get("user_id") == user_id:
                feedback_list.append(fb)

        return html_response(get_feedback_page(user_info, feedback_list))

    elif path == '/chat':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        chat_id = query_params.get('id', [''])[0]
        
        try:
            chats = read_json("chat_sessions.json")
        except:
            chats = []
        
        chat_list = []
        for chat in chats:
            if chat.get("user_id") == user_id or chat.get("partner_id") == user_id:
                target_id = chat["partner_id"] if chat["user_id"] == user_id else chat["user_id"]
                users = read_json("user.json")
                
                partner_name = "未知用户"
                partner_avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed=unknown"
                for u in users:
                    if u["user_id"] == target_id:
                        partner_name = u["username"]
                        partner_avatar = u.get("avatar", f"https://api.dicebear.com/7.x/avataaars/svg?seed={partner_name}")
                        break
                
                partners = read_json("partner.json")
                partner_data = None
                for p in partners:
                    if p["user_id"] == target_id:
                        partner_data = p
                        break
                
                chat_list.append({
                    "id": chat["id"],
                    "name": partner_name,
                    "avatar": partner_avatar,
                    "last_message": chat.get("last_message", "暂无消息"),
                    "last_time": chat.get("last_time", ""),
                    "unread_count": chat.get("unread_count", 0),
                    "partner_id": chat.get("partner_id", ""),
                    "game": partner_data["game"] if partner_data else ""
                })
        
        current_chat = None
        messages = []
        if chat_id:
            for c in chat_list:
                if c["id"] == int(chat_id):
                    current_chat = c
                    break
            if current_chat:
                try:
                    chat_messages = read_json("chat_messages.json")
                    messages = [m for m in chat_messages if m.get("chat_id") == int(chat_id)]
                except:
                    messages = []
        
        return html_response(get_chat_page(user_info, chat_list, current_chat, messages))

    elif path == '/forum':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        category = query_params.get('category', [''])[0]
        posts = read_json("forum_posts.json")
        
        if category:
            posts = [p for p in posts if p.get("category") == category]
        
        categories = ["游戏攻略", "组队开黑", "陪玩评价", "平台建议", "闲聊灌水"]
        
        return html_response(get_forum_page(user_info, posts, categories))

    elif path.startswith('/forum/post/'):
        try:
            post_id = int(path.split('/')[-1])
        except:
            return html_response("<h1>帖子不存在</h1>")

        user_id, user_type = get_user_id_from_token_or_guest(request)
        user_info = get_user_info(user_id)

        posts = read_json("forum_posts.json")
        post = None
        for p in posts:
            if p["id"] == post_id:
                post = p
                break

        if not post:
            return html_response("<h1>帖子不存在</h1>")

        comments = read_json("forum_comments.json")
        post_comments = [c for c in comments if c.get("post_id") == post_id]

        return html_response(get_post_detail_page(user_info, post, post_comments))

    elif path == '/api/v1/forum/post':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            posts = read_json("forum_posts.json")
            
            users = read_json("user.json")
            user_info = next((u for u in users if u["user_id"] == user_id), {"username": "游客", "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=guest"})
            
            new_post = {
                "id": len(posts) + 1,
                "user_id": user_id,
                "author": user_info["username"],
                "avatar": user_info.get("avatar", f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_info['username']}"),
                "title": data["title"],
                "category": data["category"],
                "content": data["content"],
                "views": 0,
                "replies": 0,
                "likes": 0,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            posts.append(new_post)
            write_json("forum_posts.json", posts)
            return json_response(200, "发表成功")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/forum/comment':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            comments = read_json("forum_comments.json")
            
            users = read_json("user.json")
            user_info = next((u for u in users if u["user_id"] == user_id), {"username": "游客", "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=guest"})
            
            new_comment = {
                "id": len(comments) + 1,
                "post_id": data["post_id"],
                "user_id": user_id,
                "author": user_info["username"],
                "avatar": user_info.get("avatar", f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_info['username']}"),
                "content": data["content"],
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            comments.append(new_comment)
            write_json("forum_comments.json", comments)

            posts = read_json("forum_posts.json")
            for p in posts:
                if p["id"] == data["post_id"]:
                    p["replies"] += 1
                    break
            write_json("forum_posts.json", posts)
            
            return json_response(200, "评论成功")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/chat/messages':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        chat_id = query_params.get('id', [''])[0]
        if not chat_id:
            return json_response(400, "缺少聊天ID")
        try:
            chat_messages = read_json("chat_messages.json")
            messages = [m for m in chat_messages if m.get("chat_id") == int(chat_id)]
            
            for m in messages:
                m["is_self"] = m["sender_id"] == user_id
            
            return json_response(200, "success", messages)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/chat/message':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            chat_id = data["chat_id"]
            content = data["content"]
            
            chat_messages = read_json("chat_messages.json")
            new_message = {
                "id": len(chat_messages) + 1,
                "chat_id": chat_id,
                "sender_id": user_id,
                "content": content,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            chat_messages.append(new_message)
            write_json("chat_messages.json", chat_messages)
            
            chat_sessions = read_json("chat_sessions.json")
            for chat in chat_sessions:
                if chat["id"] == chat_id:
                    chat["last_message"] = content
                    chat["last_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    if chat["user_id"] != user_id:
                        chat["unread_count"] = chat.get("unread_count", 0) + 1
                    break
            write_json("chat_sessions.json", chat_sessions)
            
            return json_response(200, "发送成功")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/chat/start':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            partner_id = data["partner_id"]
            
            chat_sessions = read_json("chat_sessions.json")
            existing_chat = None
            for chat in chat_sessions:
                if (chat["user_id"] == user_id and chat["partner_id"] == partner_id) or \
                   (chat["user_id"] == partner_id and chat["partner_id"] == user_id):
                    existing_chat = chat
                    break
            
            if existing_chat:
                return json_response(200, "success", {"chat_id": existing_chat["id"]})
            
            new_chat = {
                "id": len(chat_sessions) + 1,
                "user_id": user_id,
                "partner_id": partner_id,
                "last_message": "",
                "last_time": "",
                "unread_count": 0
            }
            chat_sessions.append(new_chat)
            write_json("chat_sessions.json", chat_sessions)
            
            return json_response(200, "success", {"chat_id": new_chat["id"]})
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/player/register':
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            success, msg = player_register(data['username'], data['password'], data['phone'])
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/partner/register':
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            success, msg = partner_register(data['username'], data['password'], data['phone'],
                                         data['game'], data['level'], data['price'], data['voice'])
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/login':
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)
            success, msg, result = login(data['username'], data['password'])
            if success:
                return json_response(200, msg, result)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/logout':
        if method != 'POST':
            return json_response(405, "方法不允许")
        token = get_token_from_request(request)
        if token:
            logout(token)
        return json_response(200, "退出成功")

    elif path == '/api/v1/recommend/home':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        result = get_home_recommend(user_id)
        return json_response(200, "success", result)

    elif path == '/api/v1/recommend/wish':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            result = wish_match(user_id, data["game"], data["budget_min"],
                              data["budget_max"], data["voice"])
            return json_response(200, "success", result)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/order/create':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        try:
            data = json.loads(body)
            success, msg, order_id = create_order(user_id, data["partner_id"],
                                                data["hours"], data["game"], data["total_price"])
            if success:
                return json_response(200, msg, {"order_id": order_id})
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/order/update':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success = update_order_status(data["order_id"], data["status"])
            if success:
                return json_response(200, "操作成功")
            return json_response(400, "操作失败")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/order/comment':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        try:
            data = json.loads(body)
            success = add_order_comment(data["order_id"], data["comment"], data["rating"])
            if success:
                return json_response(200, "评价成功")
            return json_response(400, "评价失败")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/order/refund':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        try:
            data = json.loads(body)
            success, msg = apply_refund(data["order_id"], data["reason"])
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/player/favorite':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        try:
            data = json.loads(body)
            favorites = get_favorite_list(user_id)
            is_favorited = any(f["partner_id"] == data["partner_id"] for f in favorites)

            if is_favorited:
                success, msg = remove_favorite(user_id, data["partner_id"])
            else:
                success, msg = add_favorite(user_id, data["partner_id"])

            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/player/recharge':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if user_type != "player":
            return json_response(403, "无权限")
        try:
            data = json.loads(body)
            success, msg = recharge(user_id, data["amount"])
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/partner/status':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success = update_partner_status(user_id, data["status"])
            if success:
                return json_response(200, "状态更新成功")
            return json_response(400, "更新失败")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/partner/withdraw':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success, msg = apply_withdraw(user_id, data["amount"])
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/partner/edit':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success = update_partner_info(user_id, data.get("game"), data.get("level"),
                                        data.get("price"), data.get("voice"), data.get("introduction"))
            if success:
                return json_response(200, "修改成功")
            return json_response(400, "修改失败")
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/admin/audit':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success, msg = audit_partner(data["partner_id"], data["pass"], "")
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/admin/refund':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        try:
            data = json.loads(body)
            success, msg = admin_handle_refund(data["order_id"], data["agree"], "")
            if success:
                return json_response(200, msg)
            return json_response(400, msg)
        except Exception as e:
            return json_response(400, str(e))

    elif path == '/api/v1/feedback/submit':
        user_id, user_type = get_user_id_from_token_or_guest(request)
        if method != 'POST':
            return json_response(405, "方法不允许")
        try:
            data = json.loads(body)

            feedbacks = read_json("feedback.json")
            new_feedback = {
                "id": len(feedbacks) + 1,
                "user_id": user_id,
                "type": data.get("type", "其他问题"),
                "content": data.get("content", ""),
                "order_id": data.get("order_id", 0),
                "contact": data.get("contact", ""),
                "status": "pending",
                "reply": "",
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            feedbacks.append(new_feedback)
            write_json("feedback.json", feedbacks)

            return json_response(200, "反馈提交成功！")
        except Exception as e:
            return json_response(400, str(e))

    else:
        return json_response(404, "页面不存在")

class GamePlaymateHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def handle_request(self, method):
        parsed = urlparse(self.path)
        path = parsed.path
        query_params = parse_qs(parsed.query)

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ''

        try:
            response = handle_route(method, path, query_params, body, self)

            self.send_response(200)
            if path.startswith('/api/'):
                self.send_header('Content-Type', 'application/json; charset=utf-8')
            else:
                self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            self.wfile.write(response)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json_response(500, str(e)))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

if __name__ == '__main__':
    get_or_create_guest_user()

    feedbacks = read_json("feedback.json")
    if not feedbacks:
        write_json("feedback.json", [])

    server = http.server.HTTPServer(('0.0.0.0', PORT), GamePlaymateHandler)
    print("[OK] AI陪玩推荐平台启动成功！")
    print(f"[INFO] 访问地址: http://localhost:{PORT}")
    print("[INFO] 游客模式已启用，无需登录即可使用全部功能！")
    print("[INFO] 管理员账号: admin/admin123")
    print("[INFO] 新增功能：问题反馈页面")
    server.serve_forever()