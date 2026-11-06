#!/usr/bin/env python3
"""Render GitHub's public contribution calendar as two animated SVG images."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import random
import re
import sys
from urllib.request import Request, urlopen

USER = 'Longfellow1'
OUT = Path(__file__).resolve().parents[1] / 'assets'
PALETTES = {
    'light': ('#eff2f5', '#aceebb', '#4ac26b', '#2da44e', '#116329', '#656d76'),
    'dark': ('#151b23', '#033a16', '#196c2e', '#2ea043', '#56d364', '#9198a1'),
}


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells, self.months = [], []
        self.in_head = self.in_month = False
        self.column = 0
        self.total = None
        self.in_heading = False
        self.heading = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h2' and a.get('id') == 'js-contribution-activity-description':
            self.in_heading = True
        if tag == 'thead':
            self.in_head = True
        if self.in_head and tag == 'td':
            self.span = int(a.get('colspan', '1'))
            self.month_cell = 'ContributionCalendar-label' in a.get('class', '')
        if self.in_head and tag == 'span' and a.get('aria-hidden') == 'true' and self.month_cell:
            self.in_month = True
        match = re.fullmatch(r'contribution-day-component-(\d+)-(\d+)', a.get('id', ''))
        if tag == 'td' and match and 'data-date' in a and 'data-level' in a:
            self.cells.append((int(match[2]), int(match[1]), int(a['data-level']), a['data-date']))

    def handle_endtag(self, tag):
        if tag == 'h2' and self.in_heading:
            self.total = ' '.join(''.join(self.heading).split())
            self.in_heading = False
        if tag == 'span':
            self.in_month = False
        if self.in_head and tag == 'td':
            if self.month_cell:
                self.column += self.span
            self.month_cell = False
        if tag == 'thead':
            self.in_head = False

    def handle_data(self, data):
        if self.in_heading:
            self.heading.append(data)
        if self.in_month and data.strip():
            self.months.append((self.column, data.strip()))


def svg(calendar, palette):
    empty, *rest = palette
    colors, text_color = [empty] + rest[:4], rest[4]
    border = '#1f2328' if empty == '#eff2f5' else '#010409'
    width = 29 + (max(x for x, _, _, _ in calendar.cells) + 1) * 15 + 4
    # Each square has its own randomly selected period and phase. The composed
    # motion has a long repeat period, but is not mathematically infinite.
    rng = random.SystemRandom()
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="184" viewBox="0 0 {width} 184" role="img" aria-labelledby="title">',
             f'<title id="title">{escape(calendar.total)}. Animated contribution calendar.</title>',
             '<style>text{font:12px -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif} '
             '@keyframes hop{0%,90%,100%{transform:translateY(0)} 93%{transform:translateY(-3px)} 96%{transform:translateY(0)}} '
             '@media(prefers-reduced-motion:reduce){.active{animation:none!important}}</style>',
             f'<g fill="{text_color}">',
             f'<text x="0" y="15" style="font-size:14px">{escape(calendar.total)}</text>']
    for col, month in calendar.months:
        parts.append(f'<text x="{29 + col * 15}" y="38">{escape(month)}</text>')
    for row, name in ((1, 'Mon'), (3, 'Wed'), (5, 'Fri')):
        parts.append(f'<text x="0" y="{56 + row * 15 + 9}">{name}</text>')
    parts.append('</g>')
    for x, y, level, date in calendar.cells:
        if not 0 <= level <= 4:
            raise ValueError('Invalid contribution level')
        attrs = ''
        if level:
            duration = rng.randrange(7001, 19000)
            delay = rng.randrange(duration)
            attrs = f' class="active" style="animation:hop {duration}ms -{delay}ms infinite ease-in-out"'
        parts.append(f'<rect x="{29+x*15}" y="{56+y*15}" width="11" height="11" rx="2" fill="{colors[level]}" stroke="{border}" stroke-opacity="0.05" stroke-width="1"{attrs}><title>{escape(date)}</title></rect>')
    legend = width - 112
    parts.append(f'<g fill="{text_color}"><text x="{legend-32}" y="181">Less</text><text x="{legend+78}" y="181">More</text></g>')
    for level, color in enumerate(colors):
        parts.append(f'<rect x="{legend+level*15}" y="171" width="11" height="11" rx="2" fill="{color}" stroke="{border}" stroke-opacity="0.05"/>')
    return '\n'.join(parts + ['</svg>', ''])


def main():
    url = f'https://github.com/users/{USER}/contributions'
    request = Request(url, headers={'User-Agent': 'profile-contribution-reactor/1.0'})
    with urlopen(request, timeout=30) as response:
        page = response.read().decode('utf-8')
    calendar = Calendar()
    calendar.feed(page)
    if not calendar.total or not calendar.months or not 350 <= len(calendar.cells) <= 371:
        raise ValueError('GitHub calendar format changed; refusing to overwrite generated files')
    OUT.mkdir(exist_ok=True)
    for theme, palette in PALETTES.items():
        (OUT / f'contribution-reactor-{theme}.svg').write_text(svg(calendar, palette), encoding='utf-8')
    print(f'Generated {len(calendar.cells)} days; {calendar.total}')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(f'Could not update contribution graph: {error}', file=sys.stderr)
        raise SystemExit(1)
