import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(1, 1, figsize=(18, 13))
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

def box(ax, x, y, w, h, text, color='#FFFFFF', edge='#333333', fontsize=9, bold=False):
    rect = FancyBboxPatch((x, y), w, h,
                           boxstyle="round,pad=0.1",
                           facecolor=color, edgecolor=edge, linewidth=1.5, zorder=3)
    ax.add_patch(rect)
    weight = 'bold' if bold else 'normal'
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=fontsize, wrap=True, weight=weight,
            multialignment='center', zorder=4, color='#1A1A1A')

def arrow(ax, x1, y1, x2, y2, label='', color='#555555', label_offset=(0.15, 0)):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.8), zorder=2)
    if label:
        mx, my = (x1+x2)/2 + label_offset[0], (y1+y2)/2 + label_offset[1]
        ax.text(mx, my, label, fontsize=7.5, color='#444444', zorder=5)

# --- Title ---
ax.text(9, 12.5, 'Архітектура системи виявлення фейкових оголошень',
        ha='center', va='center', fontsize=14, weight='bold', color='#1A1A2E')
ax.text(9, 12.1, 'Платформа продажу та оренди житла | MuleSoft Anypoint Platform',
        ha='center', va='center', fontsize=9, color='#555555')

# --- Row 1: Client ---
box(ax, 7.5, 10.8, 3, 0.9, 'Веб / Мобільний\nклієнт', color='#D0E8FF', edge='#2980B9', fontsize=9, bold=True)
arrow(ax, 9, 10.8, 9, 10.2, 'POST /listings')

# --- Row 2: API Gateway ---
box(ax, 6.2, 9.3, 5.6, 0.85,
    'MuleSoft API Gateway\n(валідація, автентифікація, rate limiting)',
    color='#E8F4FD', edge='#2980B9', fontsize=8.5, bold=True)
arrow(ax, 9, 9.3, 9, 8.65, 'Publish')

# --- Row 3: Anypoint MQ — listing.new ---
box(ax, 5.2, 7.75, 7.6, 0.85,
    'Anypoint MQ  |  listing.new\n(надійна асинхронна черга нових оголошень)',
    color='#FFF3CD', edge='#F39C12', fontsize=8.5, bold=True)

# Object Store — IN_QUEUE (right side)
box(ax, 13.5, 7.95, 4, 0.7, 'Object Store\nСтан: "IN_QUEUE"', color='#FDECEA', edge='#C0392B', fontsize=8)
ax.annotate('', xy=(13.5, 8.25), xytext=(12.8, 8.18),
            arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.5), zorder=2)
ax.text(12.5, 8.4, 'Запис стану', fontsize=7, color='#C0392B')

arrow(ax, 9, 7.75, 9, 7.1, 'Consume')

# --- Row 4: ML Worker ---
box(ax, 5.2, 5.9, 7.6, 1.1,
    'ML Classification Worker  (MuleSoft Flow)\n'
    '1. Зчитати дані оголошення з черги\n'
    '2. GET репутація користувача з БД    \n3. Викликати ML-модель (HTTP)    \n'
    '4. Отримати verdict + confidence    \n5. Оновити Object Store → "CLASSIFIED"',
    color='#EBF5EB', edge='#27AE60', fontsize=8)

# Object Store — CLASSIFIED (right side)
box(ax, 13.5, 5.95, 4, 0.7, 'Object Store\nСтан: "CLASSIFIED"', color='#FDECEA', edge='#C0392B', fontsize=8)
ax.annotate('', xy=(13.5, 6.25), xytext=(12.8, 6.25),
            arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.5), zorder=2)

arrow(ax, 9, 5.9, 9, 5.25, '')

# --- Decision point ---
box(ax, 7.0, 4.4, 4, 0.8,
    'Оцінка confidence + verdict\nМодель повертає рішення',
    color='#F0EBF8', edge='#8E44AD', fontsize=8.5, bold=True)

# --- Left branch: BLOCK ---
arrow(ax, 7.0, 4.8, 3.2, 4.2, '')
ax.text(4.5, 4.6, 'confidence > 0.85\nverdict = FAKE', fontsize=7.5, color='#C0392B', ha='center')
box(ax, 1.0, 3.1, 4.3, 1.0,
    'Автоблокування\nСтатус → BLOCKED у БД\nСповіщення користувача',
    color='#FDECEA', edge='#E74C3C', fontsize=8, bold=True)

# --- Middle branch: Anypoint MQ listing.review ---
arrow(ax, 9, 4.4, 9, 3.75, '')
ax.text(9.15, 4.1, 'confidence\n0.4–0.85', fontsize=7.5, color='#E67E22', ha='left')
box(ax, 6.5, 2.8, 5.0, 0.85,
    'Anypoint MQ  |  listing.review\n(черга для ручної модерації)',
    color='#FFF3CD', edge='#F39C12', fontsize=8, bold=True)
arrow(ax, 9, 2.8, 9, 2.2, '')
box(ax, 7.0, 1.3, 4.0, 0.85,
    'Оператор модерації\n→ BLOCK або PUBLISH',
    color='#FEF9E7', edge='#E67E22', fontsize=8.5, bold=True)

# --- Right branch: PUBLISH ---
arrow(ax, 11.0, 4.8, 14.5, 4.2, '')
ax.text(13.2, 4.65, 'confidence < 0.4\nverdict = LEGIT', fontsize=7.5, color='#27AE60', ha='center')
box(ax, 12.5, 3.1, 4.3, 1.0,
    'Автопублікація\nСтатус → PUBLISHED у БД\nДоступне для користувачів',
    color='#EBF5EB', edge='#27AE60', fontsize=8, bold=True)

# --- Legend ---
legend_items = [
    (mpatches.Patch(color='#D0E8FF', ec='#2980B9'), 'Клієнт / API / БД'),
    (mpatches.Patch(color='#FFF3CD', ec='#F39C12'), 'Anypoint MQ (listing.new / listing.review)'),
    (mpatches.Patch(color='#EBF5EB', ec='#27AE60'), 'ML Worker / Публікація'),
    (mpatches.Patch(color='#FDECEA', ec='#C0392B'), 'Object Store (стан процесу)'),
    (mpatches.Patch(color='#F0EBF8', ec='#8E44AD'), 'Рішення моделі'),
]
ax.legend(handles=[h for h, _ in legend_items],
          labels=[l for _, l in legend_items],
          loc='lower left', fontsize=8, framealpha=0.9,
          title='Легенда', title_fontsize=8.5)

plt.tight_layout()
plt.savefig('/Users/adamgolota/Documents/projects/ml/pr7/architecture_diagram.png',
            dpi=180, bbox_inches='tight', facecolor='#F8F9FA')
print("Diagram saved.")
