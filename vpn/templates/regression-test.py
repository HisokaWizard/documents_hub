# РЕГРЕССИОННЫЙ ТЕСТ HTML-модулей курса VPN
# Запуск: скопировать ВЕСЬ этот файл в code= вызова browser_exec (Hermes).
# Проверяет КАЖДЫЙ NN-*.html в папке vpn/ после любых правок любого модуля.
#
# Что проверяется:
#  1. script_alive        — <script> отработал (hero-фон создан, квиз отрендерился)
#  2. invisible_focus     — нет невидимых фокусируемых элементов (tabindex=0 с opacity~0
#                           у самого элемента ИЛИ у его .node-box/rect-потомка)
#  3. focus_css           — в стилях есть :focus-visible (кастомный фокус вместо системного)
#  4. pkt_selfmotion      — сценные пакеты НЕ двигаются сами без клика (transform до/после 2.2с)
#  5. card_sel_persist    — клик по узлу схемы даёт СТОЙКОЕ выделение карточки (.sel)
#  6. stepnav             — степ-навигация journey-игры делает шаг (счётчик != «шаг 0»)
import os, json, time

# Скрипт рассчитан на запуск ВНУТРИ browser_exec (Hermes): хелперы js/cdp/goto_url/
# wait_for_load пред-импортированы там. Вне browser_exec подставляются заглушки,
# дающие понятную ошибку (и гасящие диагностики редактора).
def _stub(*a, **k):
    raise SystemExit('Запускайте этот файл внутри вызова browser_exec (Hermes) — хелперы js/cdp/goto_url/wait_for_load доступны только там.')

_g = globals()
js = _g.get('js', _stub)
cdp = _g.get('cdp', _stub)
goto_url = _g.get('goto_url', _stub)
wait_for_load = _g.get('wait_for_load', _stub)
capture_screenshot = _g.get('capture_screenshot', _stub)

VPN_DIR = '/Users/hisokawizard/Projects/documents_hub/vpn'

# Можно сузить прогон до конкретных файлов: REGRESSION_ONLY = ['06-protokoly-vpn.html']
REGRESSION_ONLY = _g.get('REGRESSION_ONLY', None)

def J(expr, tries=4):
    # ретрай на обрывах транспорта браузера («no close frame…»): между попытками
    # соединение обычно восстанавливается само
    for t in range(tries):
        try:
            return js(f"(() => {{ return {expr} }})()")
        except Exception as e:
            if t == tries - 1:
                raise
            time.sleep(1.5)
    raise RuntimeError('unreachable')

try:
    cdp('Network.enable')
    cdp('Network.setBlockedURLs', urls=["*fonts.googleapis.com*", "*fonts.gstatic.com*"])
except Exception:
    pass

results = {}
files = sorted(f for f in os.listdir(VPN_DIR) if f[:2].isdigit() and f.endswith('.html'))
if REGRESSION_ONLY:
    files = [f for f in files if f in REGRESSION_ONLY]
for fn in files:
    goto_url('file://' + os.path.join(VPN_DIR, fn))
    wait_for_load()
    cdp('Page.enable'); cdp('Page.reload', ignoreCache=True)
    time.sleep(1.3)
    # прокрутить всю страницу ступенями, чтобы scroll-reveal секции стали видимыми
    # (один прыжок в низ не триггерит IntersectionObserver у средних секций!)
    total = int(J("document.body.scrollHeight"))
    y = 0
    while y < total:
        J(f"window.scrollTo(0, {y})")
        time.sleep(0.22)
        y += 380
    J(f"window.scrollTo(0, {total})")
    time.sleep(0.5)
    J("window.scrollTo(0, 0)")
    time.sleep(0.3)
    r = {}

    # 1. скрипт жив
    r['script_alive'] = json.loads(J("""JSON.stringify({
      hero: document.getElementById('hero-bg') ? document.getElementById('hero-bg').children.length : -1,
      quiz: document.getElementById('quizBox') ? document.querySelectorAll('#quizBox .q').length : -1
    })"""))

    # 2. невидимые фокусируемые (checkVisibility учитывает opacity предков)
    r['invisible_focus'] = json.loads(J("""JSON.stringify([...document.querySelectorAll('[tabindex="0"]')].filter(el => {
      const opts = {checkOpacity: true, checkVisibilityCSS: true};
      if (!el.checkVisibility(opts)) return true;
      const box = el.querySelector('.node-box, rect');
      if (box && !box.checkVisibility(opts)) return true;
      return false;
    }).map(el => el.id || el.getAttribute('aria-label') || el.tagName))"""))

    # 3. focus-visible стили
    r['focus_css'] = J("""[...document.querySelectorAll('style')].some(s => s.textContent.includes('focus-visible'))""")

    # 4. пакеты не летают сами
    pkt_ids = "['packetG','cityPkt','hijackPkt','natPkt','tlsPkt','routePkt','racePkt','hsPkt','archPkt','mitmPkt']"
    t1 = J(f"""(() => {{
      const el = {pkt_ids}.map(i => document.getElementById(i)).find(Boolean);
      return el ? el.id + '|' + el.getAttribute('transform') : 'none';
    }})()""")
    time.sleep(2.2)
    t2 = J(f"""(() => {{
      const el = {pkt_ids}.map(i => document.getElementById(i)).find(Boolean);
      return el ? el.id + '|' + el.getAttribute('transform') : 'none';
    }})()""")
    r['pkt_selfmotion'] = 'OK' if t1 == t2 else f'MOVED: {t1} -> {t2}'

    # 5. клик узла → стойкая карточка (берём узел, у которого ЕСТЬ карточка)
    node = J("""(() => {
      const g = [...document.querySelectorAll('.node-g')].find(el => {
        if (el.getAttribute('tabindex') !== '0' || el.classList.contains('hidden-node')) return false;
        const n = el.dataset.node;
        return !!document.querySelector(`.vcard[data-for="${n}"], .icard[data-for="${n}"]`);
      });
      if (!g) return 'no-node';
      g.dispatchEvent(new MouseEvent('click', {bubbles:true}));
      return g.dataset.node || 'node';
    })()""")
    time.sleep(1.6)  # дольше flash-анимации: sel обязан остаться
    sel_count = J("document.querySelectorAll('.vcard.sel, .icard.sel').length")
    r['card_sel_persist'] = f"{node}: sel={sel_count}" + (" OK" if (node == 'no-node' or sel_count >= 1) else " FAIL")

    # 6. степ-навигация
    has_step = J("['cityNext','hijackNext','tripNext','hsNext','raceNext','archNext','mitmNext'].some(i => document.getElementById(i))")
    if has_step:
        J("""(() => { const nx = ['cityNext','hijackNext','tripNext','hsNext','raceNext','archNext','mitmNext'].map(i=>document.getElementById(i)).find(Boolean); nx.click(); return 1; })()""")
        time.sleep(1.8)
        counter = J("(() => { const c = ['cityStep','hijackStep','tripStep','hsStep','raceStep','archStep','mitmStep'].map(i=>document.getElementById(i)).find(Boolean); return c ? c.textContent : ''; })()")
        r['stepnav'] = counter + (" OK" if counter and 'шаг 0' not in counter else " FAIL")
    else:
        r['stepnav'] = 'n/a'

    results[fn] = r

print(json.dumps(results, ensure_ascii=False, indent=1))
fails = []
for fn, r in results.items():
    if not r['script_alive']['quiz'] > 0: fails.append(f"{fn}: quiz dead")
    if r['script_alive']['hero'] == 0: fails.append(f"{fn}: hero dead")
    if r['invisible_focus']: fails.append(f"{fn}: invisible focusables {r['invisible_focus']}")
    if not r['focus_css']: fails.append(f"{fn}: no focus-visible css")
    if r['pkt_selfmotion'] != 'OK': fails.append(f"{fn}: {r['pkt_selfmotion']}")
    if 'FAIL' in str(r['card_sel_persist']): fails.append(f"{fn}: card sel {r['card_sel_persist']}")
    if 'FAIL' in str(r['stepnav']): fails.append(f"{fn}: stepnav {r['stepnav']}")
print("\n=== ИТОГ:", "ALL PASS ✅" if not fails else "FAILURES ❌ " + "; ".join(fails))
