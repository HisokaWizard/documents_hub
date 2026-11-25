# СМОУК-ТЕСТ HTML-модулей курса VPN (дополнение к regression-test.py)
# Запуск: скопировать ВЕСЬ этот файл в code= вызова browser_exec (Hermes):
#     exec(open('/Users/hisokawizard/Projects/documents_hub/vpn/templates/module-smoke-test.py').read())
# Проверяет КАЖДЫЙ NN-*.html в папке vpn/. Цель: дешёвый «дымовой» прогон
# интерактива нового/изменённого модуля без написания одноразовых тестов под каждый модуль.
#
# Что проверяется:
#  1. js_errors         — ошибок JS нет: ни при загрузке, ни после клика по всем кнопкам/чипам
#                         (хук window.addEventListener('error') внедряется ДО загрузки документа)
#  2. script_alive      — <script> отработал (hero-фон создан, квиз отрендерился)
#  3. sections_revealed — все .reveal-секции видимы после поэтапной прокрутки
#  4. controls_clicked  — сколько видимых .btn/.chip было кликнуто (должно быть > 0),
#                         страница после этого жива (квиз на месте)
#  5. quiz_answerable   — ответ на первый вопрос квиза засчитывается (.q.answered)
#  6. speech_present    — есть хотя бы одна реплика .speech (игры разговаривают)
#  7. screenshot_nonempty — скриншот страницы непустой (> 10 КБ)
#
# ОТЛИЧИЕ от regression-test.py: регрессия проверяет ИНВАРИАНТЫ курса (пакеты не летают
# сами, focus-visible, стойкие карточки), смоук — ЧТО ИНТЕРАКТИВ ВООБЩЕ РАБОТАЕТ
# и не сыпет ошибками при полном прокликивании.
import os, json, time

# Скрипт рассчитан на запуск ВНУТРИ browser_exec (Hermes): хелперы js/cdp/goto_url/
# wait_for_load пред-импортированы там. Вне browser_exec подставляются заглушки.
def _stub(*a, **k):
    raise SystemExit('Запускайте этот файл внутри вызова browser_exec (Hermes) — хелперы js/cdp/goto_url/wait_for_load доступны только там.')

_g = globals()
js = _g.get('js', _stub)
cdp = _g.get('cdp', _stub)
goto_url = _g.get('goto_url', _stub)
wait_for_load = _g.get('wait_for_load', _stub)
capture_screenshot = _g.get('capture_screenshot', _stub)

VPN_DIR = '/Users/hisokawizard/Projects/documents_hub/vpn'

# Можно сузить прогон до конкретных файлов: SMOKE_ONLY = ['05-shifrovanie-i-kluchi.html']
SMOKE_ONLY = _g.get('SMOKE_ONLY', None)

def J(expr):
    return js(f"(() => {{ return {expr} }})()")

try:
    cdp('Network.enable')
    cdp('Network.setBlockedURLs', urls=["*fonts.googleapis.com*", "*fonts.gstatic.com*"])
except Exception:
    pass
# хук ошибок JS внедряется до любого скрипта документа (переживает навигации)
try:
    cdp('Page.addScriptToEvaluateOnNewDocument', source=(
        "window.__errs=[];"
        "window.addEventListener('error',e=>__errs.push('error: '+e.message));"
        "window.addEventListener('unhandledrejection',e=>__errs.push('rejection: '+e.reason));"
    ))
except Exception:
    pass

results = {}
files = sorted(f for f in os.listdir(VPN_DIR) if f[:2].isdigit() and f.endswith('.html'))
if SMOKE_ONLY:
    files = [f for f in files if f in SMOKE_ONLY]

for fn in files:
    goto_url('file://' + os.path.join(VPN_DIR, fn))
    wait_for_load()
    cdp('Page.enable'); cdp('Page.reload', ignoreCache=True)
    time.sleep(1.3)
    J("window.__errs = window.__errs || []")

    # поэтапная прокрутка вниз и обратно: scroll-reveal секции обязаны открыться
    total = int(J("document.body.scrollHeight"))
    y = 0
    while y < total:
        J(f"window.scrollTo(0, {y})")
        time.sleep(0.18)
        y += 380
    J(f"window.scrollTo(0, {total})")
    time.sleep(0.4)
    J("window.scrollTo(0, 0)")
    time.sleep(0.3)

    r = {}
    # 2. скрипт жив
    r['script_alive'] = json.loads(J("""JSON.stringify({
      hero: document.getElementById('hero-bg') ? document.getElementById('hero-bg').children.length : -1,
      quiz: document.getElementById('quizBox') ? document.querySelectorAll('#quizBox .q').length : -1
    })"""))

    # 3. reveal-секции видимы (checkOpacity учитывает opacity предков)
    r['sections_revealed'] = J("""(() => {
      const rs = [...document.querySelectorAll('.reveal')];
      const hidden = rs.filter(el => !el.checkVisibility({checkOpacity:true}));
      return rs.length + '/' + (rs.length - hidden.length);
    })()""")

    # 4. кликаем все видимые кнопки и чипы (авто-режимы стартуют — это ок,
    #    они не блокируют; после прокликивания страница обязана остаться живой)
    r['controls_clicked'] = J("""(() => {
      const els = [...document.querySelectorAll('.btn, .chip')].filter(el =>
        el.checkVisibility({checkOpacity:true}) && !el.disabled);
      els.forEach(el => el.dispatchEvent(new MouseEvent('click', {bubbles:true})));
      return els.length;
    })()""")
    time.sleep(2.0)
    r['alive_after_clicks'] = J("document.querySelectorAll('#quizBox .q').length")

    # 5. квиз отвечает
    r['quiz_answerable'] = J("""(() => {
      const inp = document.querySelector('#quizBox .q label input');
      if (!inp) return 'no-input';
      inp.click();
      return document.querySelectorAll('#quizBox .q.answered').length >= 1 ? 'OK' : 'FAIL';
    })()""")

    # 6. реплики игр
    r['speech_present'] = J("document.querySelectorAll('.speech').length")

    # 1. ошибки JS за всё время (загрузка + прокликивание)
    r['js_errors'] = json.loads(J("JSON.stringify((window.__errs||[]).slice(0,10))"))

    # 7. скриншот непустой
    try:
        shot = capture_screenshot()
        r['screenshot_nonempty'] = 'OK' if shot and os.path.getsize(shot) > 10*1024 else f'TOO SMALL: {shot}'
    except Exception as e:
        r['screenshot_nonempty'] = f'ERROR: {e}'

    results[fn] = r

print(json.dumps(results, ensure_ascii=False, indent=1))
fails = []
warns = []
for fn, r in results.items():
    if r['js_errors']: fails.append(f"{fn}: JS errors {r['js_errors']}")
    if not r['script_alive']['quiz'] > 0: fails.append(f"{fn}: quiz dead")
    if r['script_alive']['hero'] == 0: fails.append(f"{fn}: hero dead")
    a, b = str(r['sections_revealed']).split('/')
    if a != b: fails.append(f"{fn}: sections revealed {r['sections_revealed']}")
    if not r['controls_clicked']: fails.append(f"{fn}: no clickable controls")
    if not r['alive_after_clicks']: fails.append(f"{fn}: dead after clicks")
    if r['quiz_answerable'] != 'OK': fails.append(f"{fn}: quiz {r['quiz_answerable']}")
    if not r['speech_present']: warns.append(f"{fn}: no speech strips (модуль старше конвенции?)")
    if r['screenshot_nonempty'] != 'OK': fails.append(f"{fn}: screenshot {r['screenshot_nonempty']}")
print("\n=== ИТОГ:", "ALL PASS ✅" if not fails else "FAILURES ❌ " + "; ".join(fails))
if warns:
    print("=== ПРЕДУПРЕЖДЕНИЯ ⚠️ " + "; ".join(warns))
