#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate A3 booklet and A0 presentation boards for Open Jing-Zhang submission.

Dependencies:
    pip install matplotlib

Usage:
    python generate_pdfs.py
"""
import json
import os
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# ---------- paths ----------
BASE = Path(__file__).resolve().parent.parent  # open-jing-zhang root
DRAWINGS = BASE / 'drawings'
ASSETS_FIGURES = BASE / 'assets' / 'figures'
GEOMETRY = BASE / 'geometry'

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

COLORS = {
    'rust': '#8B4513', 'terminal': '#00FF41', 'commit': '#DE2910',
    'trunk': '#1A1A2E', 'white': '#F5F5F5', 'fork': '#FF69B4',
    'main': '#00CED1', 'release': '#FFD700', 'green': '#2E8B57',
    'road': '#555555', 'gray': '#2D2D3D', 'border': '#3A3A4A',
}

# ============================================================
#  HELPERS
# ============================================================

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def new_page(figsize=(17.0, 11.7)):  # A3 landscape in inches
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return fig, ax

def add_title(ax, text, y=0.95, fontsize=20):
    ax.text(0.5, y, text, transform=ax.transAxes, ha='center', va='top',
            fontsize=fontsize, fontweight='bold', color='#1A1A2E',
            fontfamily='sans-serif')

def add_subtitle(ax, text, y=0.90, fontsize=11):
    ax.text(0.5, y, text, transform=ax.transAxes, ha='center', va='top',
            fontsize=fontsize, color='#666', fontfamily='sans-serif')

def add_footer(ax, text='开源京张 · Open Jing-Zhang — 百年京张 AI 创新带城市设计开源征集方案'):
    ax.text(0.5, 0.02, text, transform=ax.transAxes, ha='center', va='bottom',
            fontsize=8, color='#999')

def embed_image(ax, img_path, extent=(0.02, 0.48, 0.08, 0.85)):
    """Embed a PNG figure into the page."""
    if not img_path.exists():
        ax.text(0.25, 0.5, f'[Image not found]\n{img_path.name}',
                transform=ax.transAxes, ha='center', va='center', color='red')
        return
    img = plt.imread(str(img_path))
    ax.imshow(img, extent=extent, aspect='auto', zorder=0,
              transform=ax.transAxes)

def text_block(ax, x, y, lines, fontsize=9, lineheight=1.6, width=0.45):
    """Render a block of text lines."""
    text = '\n'.join(lines)
    ax.text(x, y, text, transform=ax.transAxes, ha='left', va='top',
            fontsize=fontsize, color='#333', fontfamily='sans-serif',
            linespacing=lineheight, wrap=True,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                      edgecolor='#DDD', alpha=0.9))

# ============================================================
#  A3 BOOKLET
# ============================================================

def generate_a3_booklet():
    """Generate a multi-page A3 booklet PDF."""
    out_path = DRAWINGS / 'a3-booklet.pdf'
    metrics = load_json(BASE / 'metrics.json')
    compliance = load_json(BASE / 'compliance_matrix.json')

    with PdfPages(str(out_path)) as pdf:

        # ---- Cover page ----
        fig, ax = new_page()
        ax.text(0.5, 0.65, '开源京张', transform=ax.transAxes, ha='center',
                va='center', fontsize=48, fontweight='bold', color='#1A1A2E',
                fontfamily='sans-serif')
        ax.text(0.5, 0.55, 'Open Jing-Zhang', transform=ax.transAxes,
                ha='center', va='center', fontsize=28, color='#8B4513',
                fontfamily='monospace')
        ax.text(0.5, 0.45, '世界上第一座用 git 建造的城市',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=18, color='#555', fontfamily='sans-serif')
        ax.text(0.5, 0.35, '百年京张 AI 创新带城市设计开源征集方案',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=14, color='#888', fontfamily='sans-serif')
        ax.text(0.5, 0.20, 'Agent: Open Jing-Zhang Agent · Model: claude-fable-5',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=10, color='#AAA', fontfamily='monospace')
        ax.text(0.5, 0.15, '2026-08-07 · COMMUNITY-DISPLAY-ONLY',
                transform=ax.transAxes, ha='center', va='center',
                fontsize=10, color='#AAA', fontfamily='monospace')
        # Decorative line
        ax.axhline(y=0.40, xmin=0.2, xmax=0.8, color='#00FF41', linewidth=2)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 1: Site Overview ----
        fig, ax = new_page()
        add_title(ax, '统筹研究范围与总体设计范围')
        add_subtitle(ax, '三层范围工作框架 · 基于 provisional 粗略替代边界')
        embed_image(ax, ASSETS_FIGURES / 'site-overview.png',
                    extent=(0.02, 0.48, 0.08, 0.85))
        text_block(ax, 0.52, 0.82, [
            '统筹研究范围：43.6 km2',
            '总体设计范围：11.4 km2',
            '重点区域范围：368.4 ha',
            '',
            '三处重点区域（自北向南）：',
            '  众智园 AI 自主创新加速区（Fork 区）：192.1 ha',
            '  北京 AI 原点社区（Main 区）：104.3 ha',
            '  大钟寺 AI 产业聚集区（Release 区）：72.0 ha',
            '',
            '空间结构：一轴·三区·两翼·多节点',
            '  一轴：开源铁道（Open Rail）',
            '  三区：Fork → Main → Release',
            '  两翼：CI 翼（中关村）+ CD 翼（小月河）',
        ], fontsize=10)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 2: Land Use ----
        fig, ax = new_page()
        add_title(ax, '用地布局结构')
        add_subtitle(ax, '总体设计范围用地分区 · 控规指标为 unknown')
        embed_image(ax, ASSETS_FIGURES / 'land-use-structure.png',
                    extent=(0.02, 0.48, 0.08, 0.85))
        text_block(ax, 0.52, 0.82, [
            '用地分区（概念性方案）：',
            '',
            'LU-001  新型产业用地 M0    Fork 区',
            'LU-002  科研教育用地 A2    Fork-Main 过渡区',
            'LU-003  商务设施用地 B29   Main 区',
            'LU-004  商业设施用地 B1    Main-Release 过渡区',
            'LU-005  商业设施用地 B1    Release 区',
            'LU-006  交通设施用地 S1    南端',
            '',
            '注意：',
            '· 所有用地分区基于 provisional 粗略替代边界',
            '· 容积率、建筑高度等控规指标标记为 unknown',
            '· 不构成控规调整建议',
        ], fontsize=10)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 3: Key Areas ----
        fig, ax = new_page()
        add_title(ax, '三处重点区域与公共空间节点')
        add_subtitle(ax, 'Fork 区 · Main 区 · Release 区 · 朝圣地标')
        embed_image(ax, ASSETS_FIGURES / 'key-areas.png',
                    extent=(0.02, 0.48, 0.08, 0.85))
        text_block(ax, 0.52, 0.82, [
            '三处重点区域：',
            '',
            'Fork 区（众智园）：',
            '  AI 全栈自主创新 · 算力中心 · 开源社区',
            '  地标：First Commit 纪念碑',
            '',
            'Main 区（AI 原点社区）：',
            '  世界级 AI 创新生态 · 开源主干',
            '  地标：开源之墙（Wall of Contributors）',
            '',
            'Release 区（大钟寺）：',
            '  智能原生消费商务 · 产品发布',
            '  地标：Fork 广场',
            '',
            '公共空间节点：',
            '  PS-001 First Commit 纪念碑',
            '  PS-002 开源之墙',
            '  PS-003 Fork 广场',
            '  PS-004 Pull Request 长廊',
            '  PS-005 README Wall',
        ], fontsize=10)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 4: Mobility & Blue-Green ----
        fig, ax = new_page()
        add_title(ax, '交通慢行与蓝绿公共空间复合系统')
        add_subtitle(ax, '道路系统 · 慢行网络 · 蓝绿廊道 · 约束条件')
        embed_image(ax, ASSETS_FIGURES / 'mobility-bluegreen.png',
                    extent=(0.02, 0.48, 0.08, 0.85))
        text_block(ax, 0.52, 0.82, [
            '交通系统：',
            '· 道路骨架：京藏高速、北五环、学院路、西直门外大街',
            '· 轨道站点：13号线五道口站、知春路站一体化',
            '· 慢行系统：三级网络（主干-次干-支路）',
            '· 东西缝合：下穿通道+立体步行系统',
            '',
            '蓝绿空间：',
            '· 开源铁道主轴绿带',
            '· 小月河蓝绿廊道（CD 翼场景部署走廊）',
            '',
            '城市风貌：',
            '· 材料：耐候钢 × 玻璃 × 混凝土',
            '· 色彩：铁锈棕 + 终端绿 + 协作白',
            '· 屋顶：光伏一体化，线性语言',
            '· 体量：沿主轴由低到高过渡',
        ], fontsize=10)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 5: Metrics ----
        fig, ax = new_page()
        add_title(ax, '核心指标复算与证据链')
        add_subtitle(ax, '已知指标来自官方公告 · unknown 指标待控规条件确认')
        embed_image(ax, ASSETS_FIGURES / 'metrics-evidence.png',
                    extent=(0.02, 0.48, 0.08, 0.85))
        text_block(ax, 0.52, 0.82, [
            '面积指标（已知）：',
            '· 统筹研究范围：43.6 km2',
            '· 总体设计范围：11.4 km2',
            '· 重点区域：368.4 ha',
            '· Fork 区：192.1 ha · Main 区：104.3 ha · Release 区：72.0 ha',
            '',
            '控规指标（unknown）：',
            '· 容积率：待确认',
            '· 建筑高度：待确认',
            '· 建筑密度：待确认',
            '· 绿地率：待确认',
            '',
            '概念指标（已设计）：',
            '· 场景卡：12 张（4张产业测试验证）',
            '· 用户画像：5 类',
            '· 朝圣地标：3 个',
            '· 年度活动：5 类',
        ], fontsize=10)
        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 6: Compliance Matrix ----
        fig, ax = new_page()
        add_title(ax, '合规矩阵 · Agent 任务覆盖')
        add_subtitle(ax, '覆盖 agent_taskbook.json 全部 6 项任务 + 公告 1.3-1.5 要求')

        # Draw compliance table
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        entries = compliance.get('entries', [])
        y_start = 0.82
        row_h = 0.065
        col_x = [0.05, 0.15, 0.35, 0.50, 0.85]

        # Header
        headers = ['编号', '任务名称', '状态', '核心产出']
        for i, h in enumerate(headers):
            ax.text(col_x[i], y_start, h, fontsize=10, fontweight='bold',
                    color='#1A1A2E', va='top')
        ax.axhline(y=y_start - 0.02, xmin=0.03, xmax=0.97, color='#DDD', linewidth=1)

        for idx, entry in enumerate(entries):
            y = y_start - (idx + 1) * row_h
            if y < 0.08:
                break
            ax.text(col_x[0], y, entry.get('requirement_id', ''), fontsize=9,
                    color='#1A1A2E', va='top', fontfamily='monospace')
            ax.text(col_x[1], y, entry.get('title_zh', '')[:16], fontsize=9,
                    color='#333', va='top')
            status = entry.get('status', '')
            color = '#00FF41' if status in ('covered', 'fully_addressed') else '#DE2910'
            ax.text(col_x[2], y, status, fontsize=9, color=color, va='top',
                    fontfamily='monospace')
            outputs = ', '.join(entry.get('key_outputs', [])[:3])
            ax.text(col_x[3], y, outputs[:50], fontsize=8, color='#555', va='top')

        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 7: Scenario Cards Summary ----
        fig, ax = new_page()
        add_title(ax, 'AI 场景卡一览（12 张）')
        add_subtitle(ax, '其中 4 张为产业测试验证场景（[*]）')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        scenarios = [
            ('01', 'AI 辅助开源代码审查', '[*]', 'Main区', '开源开发者'),
            ('02', '自动驾驶测试走廊', '[*]', 'Fork区', 'AI研究者'),
            ('03', 'AI 辅助建筑能耗优化', '[*]', '全带', '物业方'),
            ('04', '开源城市数据沙盒', '[*]', 'Main区', '数据科学家'),
            ('05', 'AI 导购与推荐', '', 'Release区', '消费者'),
            ('06', '智能餐饮', '', 'Release区', '餐饮经营者'),
            ('07', 'AI 辅助医疗站', '', 'CD翼', '城市居民'),
            ('08', '智慧教育空间', '', 'Fork/Main区', '学生'),
            ('09', 'AI 文化体验', '', '铁道沿线', '国际访客'),
            ('10', '智能交通信号优化', '', '全带', '交通参与者'),
            ('11', 'AI 公共空间管理', '', '全带', '使用者'),
            ('12', 'Agent 协作演示中心', '', 'Main区', 'AI研究者'),
        ]

        col_w = 0.30
        row_h_s = 0.065
        for i, (num, name, star, loc, audience) in enumerate(scenarios):
            col = i // 6
            row = i % 6
            x = 0.05 + col * col_w
            y = 0.80 - row * row_h_s
            label = f'{num} {name} {star}'
            ax.text(x, y, label, fontsize=10, color='#1A1A2E', va='top',
                    fontweight='bold' if star else 'normal')
            ax.text(x, y - 0.025, f'位置: {loc}  |  服务: {audience}',
                    fontsize=8, color='#888', va='top')

        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Page 8: Phasing ----
        fig, ax = new_page()
        add_title(ax, '分期计划 · 2026-2036')
        add_subtitle(ax, '近期 → 中期 → 远期')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        phases = [
            ('2026-2028', '近期', '开源基础设施与社区启动', [
                '开源铁道主轴贯通',
                'First Commit 纪念碑建设',
                'AI 原点社区开源平台上线',
                '首届 Fork-a-Thon 黑客马拉松',
            ]),
            ('2028-2031', '中期', '三区联动与场景部署', [
                'Fork 区自主创新载体建成',
                'Release 区商业场景落地',
                'CD 翼 AI 场景全面部署',
                '开源之墙建设',
            ]),
            ('2031-2036', '远期', '全球开源城市标杆', [
                '开源京张品牌全球影响力',
                '年度峰会常态化',
                'Agent 参与城市治理制度化',
            ]),
        ]

        for i, (years, phase, title, items) in enumerate(phases):
            x = 0.05 + i * 0.32
            ax.text(x, 0.80, f'{years} {phase}', fontsize=14, fontweight='bold',
                    color='#1A1A2E', va='top')
            ax.text(x, 0.75, title, fontsize=11, color='#8B4513', va='top')
            for j, item in enumerate(items):
                ax.text(x + 0.02, 0.70 - j * 0.05, f'· {item}', fontsize=9,
                        color='#555', va='top')

        add_footer(ax)
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

    print(f'[OK] A3 booklet saved to {out_path}')


# ============================================================
#  A0 BOARDS
# ============================================================

def generate_a0_boards():
    """Generate A0 presentation boards (simplified for print)."""
    out_path = DRAWINGS / 'a0-boards.pdf'

    with PdfPages(str(out_path)) as pdf:

        # ---- Board 1: Overview + Spatial Structure ----
        fig = plt.figure(figsize=(33.1, 46.8))  # A0 portrait in inches
        fig.patch.set_facecolor('#FAFAFA')

        # Title area
        fig.text(0.5, 0.97, '开源京张 — 世界上第一座用 git 建造的城市',
                 ha='center', fontsize=36, fontweight='bold', color='#1A1A2E')
        fig.text(0.5, 0.955, 'Open Jing-Zhang — The First City Built with git',
                 ha='center', fontsize=20, color='#8B4513', fontfamily='monospace')
        fig.text(0.5, 0.94, '百年京张 AI 创新带城市设计开源征集方案',
                 ha='center', fontsize=16, color='#888')

        # Site overview image
        img_path = ASSETS_FIGURES / 'site-overview.png'
        if img_path.exists():
            img = plt.imread(str(img_path))
            ax_img = fig.add_axes([0.02, 0.50, 0.45, 0.42])
            ax_img.imshow(img)
            ax_img.set_xticks([])
            ax_img.set_yticks([])
            ax_img.set_title('统筹研究范围与总体设计范围', fontsize=14, color='#1A1A2E')

        # Key areas image
        img_path2 = ASSETS_FIGURES / 'key-areas.png'
        if img_path2.exists():
            img2 = plt.imread(str(img_path2))
            ax_img2 = fig.add_axes([0.50, 0.50, 0.48, 0.42])
            ax_img2.imshow(img2)
            ax_img2.set_xticks([])
            ax_img2.set_yticks([])
            ax_img2.set_title('三处重点区域与公共空间节点', fontsize=14, color='#1A1A2E')

        # Text summary
        summary_text = """
核心概念：以开源协作精神重新诠释京张铁路百年自主创新史，提出「开源京张」品牌体系，
将 43.6 平方公里创新带设计为 Git 分支模型驱动的城市级开源项目。

空间结构：一轴·三区·两翼·多节点
  一轴：开源铁道（Open Rail）—— 京张铁路遗址公园贯穿南北的文化轴线
  三区：Fork 区（众智园 192ha）→ Main 区（原点社区 104ha）→ Release 区（大钟寺 72ha）
  两翼：CI 翼（中关村科技服务翼）+ CD 翼（小月河场景赋能翼）

三次开源叙事：
  1909 京张铁路通车 → 中国工程史上第一次「技术开源」
  1980s 中关村创业潮 → 中国创新的「代码开源」
  2026 本次征集 → 世界第一次「城市开源」

核心指标：统筹研究 43.6km2 | 总体设计 11.4km2 | 重点区域 368.4ha
场景卡 12 张 | 用户画像 5 类 | 朝圣地标 3 个 | 年度活动 5 类
        """
        fig.text(0.05, 0.46, summary_text.strip(), fontsize=12, color='#333',
                 va='top', fontfamily='sans-serif', linespacing=1.8,
                 bbox=dict(boxstyle='round,pad=1', facecolor='white',
                           edgecolor='#DDD'))

        fig.text(0.5, 0.01,
                 'Agent: Open Jing-Zhang Agent · 2026-08-07 · COMMUNITY-DISPLAY-ONLY',
                 ha='center', fontsize=10, color='#AAA')

        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

        # ---- Board 2: Land Use + Mobility ----
        fig = plt.figure(figsize=(33.1, 46.8))
        fig.patch.set_facecolor('#FAFAFA')

        fig.text(0.5, 0.97, '用地布局与交通蓝绿系统', ha='center',
                 fontsize=30, fontweight='bold', color='#1A1A2E')

        # Land use
        img_lu = ASSETS_FIGURES / 'land-use-structure.png'
        if img_lu.exists():
            img_lu_data = plt.imread(str(img_lu))
            ax_lu = fig.add_axes([0.02, 0.50, 0.45, 0.42])
            ax_lu.imshow(img_lu_data)
            ax_lu.set_xticks([])
            ax_lu.set_yticks([])
            ax_lu.set_title('用地布局结构', fontsize=14, color='#1A1A2E')

        # Mobility
        img_mob = ASSETS_FIGURES / 'mobility-bluegreen.png'
        if img_mob.exists():
            img_mob_data = plt.imread(str(img_mob))
            ax_mob = fig.add_axes([0.50, 0.50, 0.48, 0.42])
            ax_mob.imshow(img_mob_data)
            ax_mob.set_xticks([])
            ax_mob.set_yticks([])
            ax_mob.set_title('交通慢行与蓝绿公共空间', fontsize=14, color='#1A1A2E')

        # Metrics
        img_met = ASSETS_FIGURES / 'metrics-evidence.png'
        if img_met.exists():
            img_met_data = plt.imread(str(img_met))
            ax_met = fig.add_axes([0.15, 0.03, 0.70, 0.42])
            ax_met.imshow(img_met_data)
            ax_met.set_xticks([])
            ax_met.set_yticks([])
            ax_met.set_title('核心指标复算与证据链', fontsize=14, color='#1A1A2E')

        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close()

    print(f'[OK] A0 boards saved to {out_path}')


# ============================================================
#  HASH UPDATE
# ============================================================

def update_manifest_hashes():
    """Compute SHA256 for all files listed in manifest.json and update hashes."""
    manifest_path = BASE / 'manifest.json'
    manifest = load_json(manifest_path)

    for entry in manifest.get('files', []):
        file_path = BASE / entry['path']
        if file_path.exists():
            sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
            entry['hash'] = sha
        else:
            entry['hash'] = 'file_missing'

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f'[OK] manifest.json hashes updated ({len(manifest["files"])} files)')


# ============================================================
#  MAIN
# ============================================================

if __name__ == '__main__':
    os.makedirs(DRAWINGS, exist_ok=True)
    generate_a3_booklet()
    generate_a0_boards()
    update_manifest_hashes()
    print('\n[DONE] All PDFs generated and manifest updated!')
