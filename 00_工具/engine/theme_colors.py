# -*- coding: utf-8 -*-
"""课件主题化配色（2026-08-03 教师反馈：各课件配色/形式不得同质化）。

结构必须统一（教学环节/页面契约），但每课视觉必须按本课生活话题（vocab_theme 大类）
注入独立主色系——禁止所有课件共用同一套默认配色。

原理：CORE_CSS 已将主色全部 CSS 变量化（--brand/--accent/--bg-start/--bg-end/...），
本模块按 theme 生成一段 `:root` 变量覆盖 + `.page` 背景覆盖，追加到 CSS_EXTRA 末尾
（后于 CORE_CSS 与设计层 v2），使该课整体换一套主色系。不改 CORE_CSS/底座。

用法：
    from theme_colors import build_theme_css
    css_extra = CSS_EXTRA + build_theme_css(card["vocab"]["theme"])
"""
DEFAULT = {
    "brand": "#E63946", "brand_light": "#FF6B6B",
    "accent": "#FFD700", "accent_light": "#FFE66D",
    "bg_start": "#FFF8F0", "bg_end": "#FFE8D6",
}

THEME_COLORS = {
    "school":         {"brand": "#2563EB", "brand_light": "#60A5FA", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#EFF6FF", "bg_end": "#DBEAFE"},
    "school_things":  {"brand": "#4F46E5", "brand_light": "#818CF8", "accent": "#22C55E", "accent_light": "#4ADE80", "bg_start": "#EEF2FF", "bg_end": "#E0E7FF"},
    "family":         {"brand": "#DB2777", "brand_light": "#F472B6", "accent": "#FBBF24", "accent_light": "#FCD34D", "bg_start": "#FFF1F2", "bg_end": "#FFE4E6"},
    "room":           {"brand": "#7C3AED", "brand_light": "#A78BFA", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#F5F3FF", "bg_end": "#EDE9FE"},
    "food":           {"brand": "#EA580C", "brand_light": "#FB923C", "accent": "#EAB308", "accent_light": "#FACC15", "bg_start": "#FFF7ED", "bg_end": "#FFEDD5"},
    "meals":          {"brand": "#D97706", "brand_light": "#FBBF24", "accent": "#10B981", "accent_light": "#34D399", "bg_start": "#FFFBEB", "bg_end": "#FEF3C7"},
    "past_time":      {"brand": "#0D9488", "brand_light": "#2DD4BF", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#F0FDFA", "bg_end": "#CCFBF1"},
    "places":         {"brand": "#16A34A", "brand_light": "#4ADE80", "accent": "#F97316", "accent_light": "#FB923C", "bg_start": "#F0FDF4", "bg_end": "#DCFCE7"},
    "subjects":       {"brand": "#0891B2", "brand_light": "#22D3EE", "accent": "#8B5CF6", "accent_light": "#A78BFA", "bg_start": "#ECFEFF", "bg_end": "#CFFAFE"},
    "rules":          {"brand": "#0284C7", "brand_light": "#38BDF8", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#F0F9FF", "bg_end": "#E0F2FE"},
    "shopping":       {"brand": "#E11D48", "brand_light": "#FB7185", "accent": "#8B5CF6", "accent_light": "#A78BFA", "bg_start": "#FFF1F2", "bg_end": "#FFE4E6"},
    "price":          {"brand": "#059669", "brand_light": "#34D399", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#ECFDF5", "bg_end": "#D1FAE5"},
    "appearance":     {"brand": "#9333EA", "brand_light": "#C084FC", "accent": "#F43F5E", "accent_light": "#FB7185", "bg_start": "#FAF5FF", "bg_end": "#F3E8FF"},
    "weather":        {"brand": "#0284C7", "brand_light": "#38BDF8", "accent": "#22D3EE", "accent_light": "#67E8F9", "bg_start": "#F0F9FF", "bg_end": "#E0F2FE"},
    "habits":         {"brand": "#10B981", "brand_light": "#34D399", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#ECFDF5", "bg_end": "#D1FAE5"},
    "activities":     {"brand": "#F97316", "brand_light": "#FB923C", "accent": "#3B82F6", "accent_light": "#60A5FA", "bg_start": "#FFF7ED", "bg_end": "#FFEDD5"},
    "description":    {"brand": "#14B8A6", "brand_light": "#2DD4BF", "accent": "#F43F5E", "accent_light": "#FB7185", "bg_start": "#F0FDFA", "bg_end": "#CCFBF1"},
    # 复习/诊断课保持默认红金（阶段测试本色）
    "review":         {"brand": "#E63946", "brand_light": "#FF6B6B", "accent": "#FFD700", "accent_light": "#FFE66D", "bg_start": "#FFF8F0", "bg_end": "#FFE8D6"},
    # 常见扩展话题（覆盖邓/李新主题用，按需增补）
    "life":           {"brand": "#0E7490", "brand_light": "#06B6D4", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#ECFEFF", "bg_end": "#CFFAFE"},
    "travel":         {"brand": "#0F766E", "brand_light": "#14B8A6", "accent": "#F97316", "accent_light": "#FB923C", "bg_start": "#F0FDFA", "bg_end": "#CCFBF1"},
    "health":         {"brand": "#16A34A", "brand_light": "#4ADE80", "accent": "#0EA5E9", "accent_light": "#38BDF8", "bg_start": "#F0FDF4", "bg_end": "#DCFCE7"},
    "study":          {"brand": "#4338CA", "brand_light": "#6366F1", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#EEF2FF", "bg_end": "#E0E7FF"},
    "future":         {"brand": "#7C3AED", "brand_light": "#A78BFA", "accent": "#F59E0B", "accent_light": "#FBBF24", "bg_start": "#F5F3FF", "bg_end": "#EDE9FE"},
}


# 封面 emoji（按话题大类，2026-08-03 教师反馈：封面 emoji 主题化）
THEME_EMOJI = {
    "school": "📚✏️🎒", "school_things": "✏️📏🎒", "family": "👨👩👧🏠",
    "room": "🛏️🚪🪑", "food": "🍎🥛🍚", "meals": "🍚🥪🍎",
    "past_time": "🕰️📖🌙", "places": "🗺️🏫🏞️", "subjects": "📚🔬🎨",
    "rules": "📏🚦📢", "shopping": "🛒💰🧺", "price": "💰🛍️🏷️",
    "appearance": "👀😊💫", "weather": "☀️🌧️❄️", "habits": "⏰🏃🥗",
    "activities": "⚽🎨🎵", "description": "👧🧑🖋️",
    "life": "🌞☕🚶", "travel": "✈️🧳🏝️", "health": "💪🥗❤️",
    "study": "📖✏️💡", "future": "🌟🚀🔮", "review": "📝⭐",
}

# 主题中文名（供课程卡/新词标题/目标卡等由主题驱动文案，2026-08-03 通用化）
THEME_NAME = {
    "school": "学校", "school_things": "学习用品", "family": "家庭",
    "room": "房间", "food": "食物", "meals": "三餐",
    "past_time": "过去时光", "places": "地点", "subjects": "学科",
    "rules": "规则", "shopping": "购物", "price": "价格",
    "appearance": "外貌", "weather": "天气", "habits": "习惯",
    "activities": "活动", "description": "描述",
    "life": "生活", "travel": "旅行", "health": "健康",
    "study": "学习", "future": "未来", "review": "复习",
}


def _triplet(hexcolor):
    h = hexcolor.lstrip("#")
    return "%d,%d,%d" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def build_theme_css(theme):
    """按 vocab_theme 大类生成主题 CSS（含 `/* THEME:xxx */` 标记供 verify 检查）。

    追加到 CSS_EXTRA 末尾即可整体覆盖该课主色系与页面背景；未知主题回退默认红金。
    """
    t = THEME_COLORS.get(theme) or THEME_COLORS["review"]
    brand, bl = t["brand"], t["brand_light"]
    acc, al = t["accent"], t["accent_light"]
    bgs, bge = t["bg_start"], t["bg_end"]
    b_tri = _triplet(brand)
    a_tri = _triplet(acc)
    return (
        "/* THEME:%s */\n"
        ":root{\n"
        "  --brand:%s;--accent:%s;--brand-light:%s;--accent-light:%s;\n"
        "  --bg-start:%s;--bg-end:%s;\n"
        "  --grad-brand:linear-gradient(135deg,%s,%s);\n"
        "  --grad-gold:linear-gradient(135deg,#FFD700,#FF9F1C);\n"
        "  --page-shadow:0 4px 20px rgba(%s,.18);\n"
        "}\n"
        ".page{background:\n"
        "  radial-gradient(1200px 600px at 85%% -10%%,rgba(%s,.22),transparent 60%%),\n"
        "  radial-gradient(900px 500px at -10%% 110%%,rgba(%s,.16),transparent 55%%),\n"
        "  linear-gradient(135deg,var(--bg-start) 0%%,var(--bg-end) 100%%);}\n"
        % (theme, brand, acc, bl, al, bgs, bge, brand, acc, b_tri, a_tri, b_tri)
    )
