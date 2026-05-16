"""
Генерація схеми взаємодії для LMS (Publisher–Broker–Subscriber)
Запуск: python3 generate_diagram.py
Результат: integration_diagram.png
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(18, 11))
ax.set_xlim(0, 18)
ax.set_ylim(0, 11)
ax.axis('off')
fig.patch.set_facecolor('#F8F9FA')

# ── Кольорова палітра ────────────────────────────────────────────
C_PUB   = '#2196F3'   # синій — видавці
C_BROKER= '#FF9800'   # помаранчевий — брокер
C_SUB   = '#4CAF50'   # зелений — підписники
C_CHAN  = '#9C27B0'   # фіолетовий — канали
C_TEXT  = '#FFFFFF'
C_TITLE = '#212121'
C_BG    = '#F8F9FA'

def draw_box(ax, x, y, w, h, color, label, sublabel='', fontsize=10):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.08",
                         linewidth=2, edgecolor='white',
                         facecolor=color, zorder=3)
    ax.add_patch(box)
    ax.text(x, y + (0.18 if sublabel else 0), label,
            ha='center', va='center', fontsize=fontsize,
            color=C_TEXT, fontweight='bold', zorder=4)
    if sublabel:
        ax.text(x, y - 0.28, sublabel,
                ha='center', va='center', fontsize=7.5,
                color='#EEEEEE', zorder=4, style='italic')

def draw_arrow(ax, x1, y1, x2, y2, color='#555555', label='', lw=1.8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, connectionstyle='arc3,rad=0.0'),
                zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.18, label, ha='center', va='bottom',
                fontsize=7, color=color, fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor=color, alpha=0.85), zorder=5)

# ══════════════════════════════════════════════════════════════════
# Заголовок
# ══════════════════════════════════════════════════════════════════
ax.text(9, 10.4, 'LMS — Схема подійно-орієнтованої взаємодії',
        ha='center', va='center', fontsize=15, fontweight='bold', color=C_TITLE)
ax.text(9, 9.95, 'Publisher → Apache Kafka Broker → Subscriber',
        ha='center', va='center', fontsize=10, color='#555555')

# ══════════════════════════════════════════════════════════════════
# ВИДАВЦІ (ліва колонка)
# ══════════════════════════════════════════════════════════════════
ax.text(2.5, 9.4, 'ВИДАВЦІ', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_PUB)

publishers = [
    (2.5, 7.9, 'Enrollment\nService',  'видавець'),
    (2.5, 5.9, 'Progress\nService',    'видавець'),
    (2.5, 3.9, 'Certificate\nService', 'видавець'),
]
for x, y, lbl, sub in publishers:
    draw_box(ax, x, y, 3.2, 1.1, C_PUB, lbl, sub, fontsize=9)

# ══════════════════════════════════════════════════════════════════
# БРОКЕР + КАНАЛИ (центр)
# ══════════════════════════════════════════════════════════════════
ax.text(9, 9.4, 'БРОКЕР ПОВІДОМЛЕНЬ', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_BROKER)

# Фон брокера
broker_bg = FancyBboxPatch((6.2, 2.6), 5.6, 7.0,
                           boxstyle="round,pad=0.15",
                           linewidth=2.5, edgecolor=C_BROKER,
                           facecolor='#FFF8E1', zorder=1)
ax.add_patch(broker_bg)
ax.text(9, 9.1, 'Apache Kafka', ha='center', va='center',
        fontsize=10, color=C_BROKER, fontweight='bold')

# Канали всередині брокера
channels = [
    (9, 7.9, 'lms.student.enrolled',   'topic | partitions: 6 | replicas: 3'),
    (9, 5.9, 'lms.lesson.completed',   'topic | partitions: 6 | replicas: 3'),
    (9, 3.9, 'lms.certificate.issued', 'topic | partitions: 3 | replicas: 3'),
]
for x, y, lbl, sub in channels:
    draw_box(ax, x, y, 4.8, 1.0, C_CHAN, lbl, sub, fontsize=8)

ax.text(9, 2.85, 'Kafka Cluster — SASL/SCRAM-SHA-256', ha='center',
        va='center', fontsize=7.5, color='#795548', style='italic')

# ══════════════════════════════════════════════════════════════════
# ПІДПИСНИКИ (права колонка)
# ══════════════════════════════════════════════════════════════════
ax.text(15.5, 9.4, 'ПІДПИСНИКИ', ha='center', va='center',
        fontsize=11, fontweight='bold', color=C_SUB)

subscribers = [
    (15.5, 8.4, 'Notification\nService',  'підписник'),
    (15.5, 6.7, 'Progress\nService',      'підписник'),
    (15.5, 5.0, 'Certificate\nService',   'підписник'),
    (15.5, 3.3, 'Analytics\nService',     'підписник'),
]
for x, y, lbl, sub in subscribers:
    draw_box(ax, x, y, 3.2, 1.1, C_SUB, lbl, sub, fontsize=9)

# ══════════════════════════════════════════════════════════════════
# СТРІЛКИ: Видавці → Канали
# ══════════════════════════════════════════════════════════════════
# Enrollment Service → lms.student.enrolled
draw_arrow(ax, 4.1, 7.9, 6.6, 7.9, color=C_PUB, label='publish')
# Progress Service → lms.lesson.completed
draw_arrow(ax, 4.1, 5.9, 6.6, 5.9, color=C_PUB, label='publish')
# Certificate Service → lms.certificate.issued
draw_arrow(ax, 4.1, 3.9, 6.6, 3.9, color=C_PUB, label='publish')

# ══════════════════════════════════════════════════════════════════
# СТРІЛКИ: Канали → Підписники
# ══════════════════════════════════════════════════════════════════
# lms.student.enrolled → Notification Service
draw_arrow(ax, 11.4, 7.9, 13.9, 8.4, color=C_CHAN, label='subscribe')
# lms.student.enrolled → Progress Service
draw_arrow(ax, 11.4, 7.75, 13.9, 6.7, color=C_CHAN)
# lms.student.enrolled → Analytics Service
draw_arrow(ax, 11.4, 7.6, 13.9, 3.5, color=C_CHAN)

# lms.lesson.completed → Certificate Service
draw_arrow(ax, 11.4, 5.9, 13.9, 5.0, color=C_CHAN, label='subscribe')
# lms.lesson.completed → Analytics Service
draw_arrow(ax, 11.4, 5.75, 13.9, 3.3, color=C_CHAN)

# lms.certificate.issued → Notification Service
draw_arrow(ax, 11.4, 3.9, 13.9, 8.1, color=C_CHAN, label='subscribe')
# lms.certificate.issued → Analytics Service
draw_arrow(ax, 11.4, 3.75, 13.9, 3.15, color=C_CHAN)

# ══════════════════════════════════════════════════════════════════
# Легенда
# ══════════════════════════════════════════════════════════════════
legend_items = [
    mpatches.Patch(facecolor=C_PUB,    label='Видавець (Publisher)'),
    mpatches.Patch(facecolor=C_CHAN,   label='Канал Kafka (Topic)'),
    mpatches.Patch(facecolor=C_SUB,    label='Підписник (Subscriber)'),
    mpatches.Patch(facecolor=C_BROKER, label='Брокер (Apache Kafka)'),
]
ax.legend(handles=legend_items, loc='lower left',
          bbox_to_anchor=(0.01, 0.01), fontsize=8.5,
          framealpha=0.95, edgecolor='#CCCCCC')

# ══════════════════════════════════════════════════════════════════
# Підпис подій поруч зі стрілками (канали)
# ══════════════════════════════════════════════════════════════════
ax.text(5.35, 8.12, 'StudentEnrolled', fontsize=7, color='#555555',
        ha='center', style='italic')
ax.text(5.35, 6.12, 'LessonCompleted', fontsize=7, color='#555555',
        ha='center', style='italic')
ax.text(5.35, 4.12, 'CertificateIssued', fontsize=7, color='#555555',
        ha='center', style='italic')

plt.tight_layout()
plt.savefig('/Users/adamgolota/Documents/projects/ml/pr6/integration_diagram.png',
            dpi=180, bbox_inches='tight', facecolor=C_BG)
print("Діаграму збережено: integration_diagram.png")
