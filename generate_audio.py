"""
Pre-generate ElevenLabs audio for all word and sentence translations.
Outputs: audio/uk/words/<key>.mp3, audio/uk/sentences/<n>.mp3
         audio/ko/words/<key>.mp3, audio/ko/sentences/<n>.mp3
Usage: python3 generate_audio.py
"""

import os, re, time
from pathlib import Path
from elevenlabs.client import ElevenLabs

API_KEY = os.getenv("ELEVENLABS_API_KEY") or open(".env").read().split("=",1)[1].strip()
client = ElevenLabs(api_key=API_KEY)

from elevenlabs import VoiceSettings

MODEL = "eleven_multilingual_v2"

# Antoni — warm, natural male. Low stability → high expressiveness for storytelling.
VOICE_UK = "ErXwobaYiN019PkySvjV"
# Daniel — clear British male. Good prosody on Korean formal register.
VOICE_KO = "onwK4e9ZLuTAKqWW03F9"
# Adam — deep, warm, authoritative male. English story narration.
VOICE_EN = "pNInz6obpgDQGcFmaJgB"

SETTINGS_EN = VoiceSettings(
    stability=0.38,
    similarity_boost=0.75,
    style=0.58,
    use_speaker_boost=True
)

SETTINGS = VoiceSettings(
    stability=0.32,          # low = more dynamic inflection
    similarity_boost=0.75,
    style=0.62,              # high style = expressive narration
    use_speaker_boost=True
)

def normalize_key(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def clean_for_tts(text, lang):
    """Strip grammatical tags like (іменник) / (명사) before sending to TTS."""
    text = re.sub(r'\s*\(.*?\)\s*', ' ', text).strip()
    # For words with '/', only read the first variant
    if '/' in text:
        text = text.split('/')[0].strip()
    return text

def generate(text, voice_id, out_path):
    if out_path.exists():
        print(f"  skip  {out_path}")
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=MODEL,
        voice_settings=SETTINGS,
        output_format="mp3_44100_128"
    )
    data = b"".join(audio)
    out_path.write_bytes(data)
    print(f"  wrote {out_path}  ({len(data)} bytes)")
    time.sleep(0.35)  # stay within rate limits

# ── Dictionaries ─────────────────────────────────────────────────────────────

WORDS_UK = {
    "welcome": "ласкаво просимо (вигук)",
    "to": "до (прийменник)",
    "the": "цей / ця (артикль)",
    "prairies": "прерії (іменник)",
    "i": "я (займенник)",
    "farm": "фермерую (дієслово)",
    "out": "десь / назовні (прислівник)",
    "near": "біля (прийменник)",
    "kindersley": "Кіндерслі (назва міста)",
    "saskatchewan": "Саскачеван (назва провінції)",
    "when": "коли (сполучник)",
    "you": "ви / ти (займенник)",
    "look": "дивитеся (дієслово)",
    "around": "навколо (прислівник)",
    "here": "тут (прислівник)",
    "sky": "небо (іменник)",
    "is": "є (дієслово)",
    "so": "таке / так (прислівник)",
    "big": "велике (прикметник)",
    "it": "воно / це (займенник)",
    "feels": "здається / відчувається (дієслово)",
    "like": "ніби / як (сполучник)",
    "might": "може (модальне дієслово)",
    "swallow": "проковтнути (дієслово)",
    "whole": "цілком / ціле (прислівник / прикметник)",
    "some": "деякі (займенник)",
    "folks": "люди (іменник)",
    "think": "думають (дієслово)",
    "there": "там / тут (прислівник)",
    "not": "не (частка)",
    "much": "багато (займенник)",
    "going": "відбувається (дієприкметник)",
    "on": "на (прийменник)",
    "just": "просто (прислівник)",
    "flat": "плоска / рівнинна (прикметник)",
    "land": "земля (іменник)",
    "and": "і / та (сполучник)",
    "wheat": "пшениця (іменник)",
    "that": "те / що (займенник)",
    "old": "старе (прикметник)",
    "comedy": "комедійне (прикметник)",
    "show": "шоу (іменник)",
    "about": "про (прийменник)",
    "gas": "газова / бензо- (прикметник)",
    "station": "заправка / станція (іменник)",
    "in": "в / у (прийменник)",
    "middle": "середина (іменник)",
    "of": "з (прийменник)",
    "nowhere": "ніде / глушина (іменник)",
    "but": "але (сполучник)",
    "they": "вони (займенник)",
    "are": "є (дієслово)",
    "missing": "пропускають (дієприкметник)",
    "best": "найкращі (прикметник)",
    "parts": "частини (іменник)",
    "farming": "фермерство (іменник)",
    "hard": "важка (прикметник)",
    "work": "праця (іменник)",
    "wake": "прокидаєтеся (дієслово)",
    "up": "вгору (прислівник)",
    "before": "до / перед (прийменник)",
    "sun": "сонце (іменник)",
    "go": "йдете (дієслово)",
    "bed": "ліжко / спати (іменник)",
    "long": "довго (прислівник)",
    "after": "після (прийменник)",
    "mosquitoes": "комарі (іменник)",
    "come": "приходять / з'являються (дієслово)",
    "spring": "весна (іменник)",
    "race": "гонка (іменник)",
    "against": "проти (прийменник)",
    "clock": "годинник (іменник)",
    "we": "ми (займенник)",
    "drive": "водимо (дієслово)",
    "tractors": "трактори (іменник)",
    "size": "розмір (іменник)",
    "small": "маленьких (прикметник)",
    "houses": "будинків (іменник)",
    "planting": "саджаючи / сіючи (дієприкметник)",
    "canola": "канола / ріпак (іменник)",
    "barley": "ячмінь (іменник)",
    "until": "поки (сполучник)",
    "our": "наші (займенник)",
    "eyes": "очі (іменник)",
    "blur": "розмиваються (дієслово)",
    "worry": "хвилюємося (дієслово)",
    "rain": "дощ (іменник)",
    "frost": "мороз (іменник)",
    "fix": "лагодимо (дієслово)",
    "broken": "зламані (прикметник)",
    "machinery": "техніка (іменник)",
    "with": "з (прийменник)",
    "whatever": "чим завгодно (займенник)",
    "have": "маємо / повинен (дієслово)",
    "red": "Ред (власна назва)",
    "green": "Грін (власна назва)",
    "always": "завжди (прислівник)",
    "said": "казав (дієслово)",
    "television": "телебачення (іменник)",
    "am": "є (дієслово)",
    "man": "чоловік (іменник)",
    "can": "можу (модальне дієслово)",
    "change": "змінитися (дієслово)",
    "if": "якщо (сполучник)",
    "guess": "мабуть / гадаю (дієслово)",
    "mostly": "переважно (прислівник)",
    "means": "означає (дієслово)",
    "learning": "навчання (іменник)",
    "how": "як (прислівник)",
    "rebuild": "перебрати / відновити (дієслово)",
    "diesel": "дизельний (прикметник)",
    "engine": "двигун (іменник)",
    "dark": "темрява (іменник)",
    "joy": "радість (іменник)",
    "quiet": "тихі (прикметник)",
    "moments": "моменти (іменник)",
    "nothing": "нічого (займенник)",
    "smell": "запах (іменник)",
    "earth": "земля (іменник)",
    "summer": "літня (прикметник)",
    "storm": "гроза / буря (іменник)",
    "sit": "сидіти (дієслово)",
    "porch": "ґанок (іменник)",
    "watch": "спостерігати (дієслово)",
    "lightning": "блискавка (іменник)",
    "dance": "танцює (дієслово)",
    "across": "через (прийменник)",
    "horizon": "горизонт (іменник)",
    "fifty": "п'ятдесят (числівник)",
    "miles": "миль (іменник)",
    "away": "далеко (прислівник)",
    "fall": "осінь (іменник)",
    "harvest": "урожай (іменник)",
    "done": "завершено (дієприкметник)",
    "town": "місто / містечко (іменник)",
    "gets": "збирається (дієслово)",
    "together": "разом (прислівник)",
    "for": "для / на (прийменник)",
    "supper": "вечеря (іменник)",
    "community": "громадський (прикметник)",
    "hall": "зал (іменник)",
    "share": "ділимося (дієслово)",
    "pies": "пироги (іменник)",
    "stories": "історії (іменник)",
    "laugh": "сміємося (дієслово)",
    "ribs": "ребра (іменник)",
    "hurt": "болять (дієслово)",
    "winter": "зима (іменник)",
    "cold": "холодна (прикметник)",
    "sure": "звичайно (прислівник)",
    "snow": "сніг (іменник)",
    "piles": "нагромаджується (дієслово)",
    "windows": "вікна (іменник)",
    "wind": "вітер (іменник)",
    "howls": "виє (дієслово)",
    "lonely": "самотній (прикметник)",
    "coyote": "койот (іменник)",
    "more": "більше (прислівник)",
    "time": "час (іменник)",
    "hockey": "хокей (іменник)",
    "frozen": "замерзлий (прикметник)",
    "pond": "ставок (іменник)",
    "drinking": "пиття (дієприслівник)",
    "hot": "гаряча (прикметник)",
    "coffee": "кава (іменник)",
    "by": "біля (прийменник)",
    "wood": "дров'яна (прикметник)",
    "stove": "піч (іменник)",
    "learn": "вчитеся (дієслово)",
    "rely": "покладатися (дієслово)",
    "your": "ваші (займенник)",
    "neighbours": "сусіди (іменник)",
    "truck": "вантажівка (іменник)",
    "stuck": "застрягає (дієприкметник)",
    "three": "троє (числівник)",
    "people": "люди (іменник)",
    "will": "будуть (допоміжне дієслово)",
    "stop": "зупиняться (дієслово)",
    "pull": "витягнути (дієслово)",
    "even": "навіть (прислівник)",
    "ask": "просити (дієслово)",
    "life": "життя (іменник)",
    "toil": "тяжка праця (іменник)",
    "outweighs": "переважає (дієслово)",
    "sweat": "піт (іменник)",
    "keep": "тримайте (дієслово)",
    "stick": "ключка (іменник)",
    "ice": "лід (іменник)",
    "this": "ця (займенник)",
    "most": "найбільш (прислівник)",
    "beautiful": "прекрасне (прикметник)",
    "place": "місце (іменник)",
}

WORDS_KO = {
    "welcome": "환영합니다 (감탄사)",
    "to": "~에 (전치사)",
    "the": "그 / 이 (관사)",
    "prairies": "초원 (명사)",
    "i": "나 / 저 (대명사)",
    "farm": "농사짓다 (동사)",
    "out": "밖에 (부사)",
    "near": "근처에 (전치사)",
    "kindersley": "킨더슬리 (지명)",
    "saskatchewan": "서스캐처원 (주 이름)",
    "when": "~할 때 (접속사)",
    "you": "당신 / 너 (대명사)",
    "look": "보다 (동사)",
    "around": "주위를 (부사)",
    "here": "여기 (부사)",
    "sky": "하늘 (명사)",
    "is": "이다 / 있다 (동사)",
    "so": "그렇게 / 매우 (부사)",
    "big": "큰 (형용사)",
    "it": "그것 (대명사)",
    "feels": "느껴진다 (동사)",
    "like": "~처럼 (접속사)",
    "might": "~할지도 모른다 (조동사)",
    "swallow": "삼키다 (동사)",
    "whole": "전체 / 완전히 (형용사 / 부사)",
    "some": "일부 / 몇몇 (대명사)",
    "folks": "사람들 (명사)",
    "think": "생각하다 (동사)",
    "there": "거기 / 그곳 (부사)",
    "not": "아니다 (부정사)",
    "much": "많이 (대명사)",
    "going": "일어나다 (분사)",
    "on": "~위에 (전치사)",
    "just": "그냥 / 단지 (부사)",
    "flat": "평평한 (형용사)",
    "land": "땅 (명사)",
    "and": "그리고 / 와 (접속사)",
    "wheat": "밀 (명사)",
    "that": "저 / 그 (대명사)",
    "old": "오래된 (형용사)",
    "comedy": "코미디 (형용사)",
    "show": "쇼 (명사)",
    "about": "~에 대한 (전치사)",
    "gas": "가스 / 주유 (형용사)",
    "station": "주유소 / 역 (명사)",
    "in": "안에 (전치사)",
    "middle": "중간 (명사)",
    "of": "~의 (전치사)",
    "nowhere": "아무데도 없는 곳 (명사)",
    "but": "하지만 (접속사)",
    "they": "그들 (대명사)",
    "are": "이다 / 있다 (동사)",
    "missing": "놓치다 (분사)",
    "best": "최고의 (형용사)",
    "parts": "부분들 (명사)",
    "farming": "농사 / 농업 (명사)",
    "hard": "힘든 (형용사)",
    "work": "일 (명사)",
    "wake": "일어나다 (동사)",
    "up": "위로 (부사)",
    "before": "~전에 (전치사)",
    "sun": "태양 (명사)",
    "go": "가다 (동사)",
    "bed": "침대 / 자다 (명사)",
    "long": "오래 (부사)",
    "after": "~후에 (전치사)",
    "mosquitoes": "모기들 (명사)",
    "come": "오다 / 나타나다 (동사)",
    "spring": "봄 (명사)",
    "race": "경주 (명사)",
    "against": "~에 맞서 (전치사)",
    "clock": "시계 (명사)",
    "we": "우리 (대명사)",
    "drive": "운전하다 (동사)",
    "tractors": "트랙터들 (명사)",
    "size": "크기 (명사)",
    "small": "작은 (형용사)",
    "houses": "집들 (명사)",
    "planting": "심으며 (분사)",
    "canola": "카놀라 / 유채 (명사)",
    "barley": "보리 (명사)",
    "until": "~까지 (접속사)",
    "our": "우리의 (대명사)",
    "eyes": "눈들 (명사)",
    "blur": "흐려지다 (동사)",
    "worry": "걱정하다 (동사)",
    "rain": "비 (명사)",
    "frost": "서리 / 추위 (명사)",
    "fix": "수리하다 (동사)",
    "broken": "고장난 (형용사)",
    "machinery": "기계류 (명사)",
    "with": "~으로 / 함께 (전치사)",
    "whatever": "무엇이든지 (대명사)",
    "have": "가지다 / 해야 한다 (동사)",
    "red": "레드 (고유명사)",
    "green": "그린 (고유명사)",
    "always": "항상 (부사)",
    "said": "말했다 (동사)",
    "television": "텔레비전 (명사)",
    "am": "이다 / 있다 (동사)",
    "man": "남자 (명사)",
    "can": "할 수 있다 (조동사)",
    "change": "변하다 (동사)",
    "if": "만약 (접속사)",
    "guess": "아마도 / 추측하다 (동사)",
    "mostly": "주로 (부사)",
    "means": "의미하다 (동사)",
    "learning": "배우는 것 (명사)",
    "how": "어떻게 (부사)",
    "rebuild": "재건하다 / 분해하다 (동사)",
    "diesel": "디젤 (형용사)",
    "engine": "엔진 (명사)",
    "dark": "어둠 (명사)",
    "joy": "기쁨 (명사)",
    "quiet": "조용한 (형용사)",
    "moments": "순간들 (명사)",
    "nothing": "아무것도 없다 (대명사)",
    "smell": "냄새 (명사)",
    "earth": "땅 / 흙 (명사)",
    "summer": "여름 (형용사)",
    "storm": "폭풍 (명사)",
    "sit": "앉다 (동사)",
    "porch": "현관 / 베란다 (명사)",
    "watch": "보다 / 관찰하다 (동사)",
    "lightning": "번개 (명사)",
    "dance": "춤추다 (동사)",
    "across": "~을 가로질러 (전치사)",
    "horizon": "지평선 (명사)",
    "fifty": "오십 (수사)",
    "miles": "마일들 (명사)",
    "away": "멀리 (부사)",
    "fall": "가을 (명사)",
    "harvest": "수확 (명사)",
    "done": "끝난 / 완료된 (분사)",
    "town": "마을 / 도시 (명사)",
    "gets": "모이다 (동사)",
    "together": "함께 (부사)",
    "for": "~을 위해 (전치사)",
    "supper": "저녁 식사 (명사)",
    "community": "공동체의 (형용사)",
    "hall": "홀 (명사)",
    "share": "나누다 (동사)",
    "pies": "파이들 (명사)",
    "stories": "이야기들 (명사)",
    "laugh": "웃다 (동사)",
    "ribs": "갈비뼈들 (명사)",
    "hurt": "아프다 (동사)",
    "winter": "겨울 (명사)",
    "cold": "추운 (형용사)",
    "sure": "물론이지 (부사)",
    "snow": "눈 (명사)",
    "piles": "쌓이다 (동사)",
    "windows": "창문들 (명사)",
    "wind": "바람 (명사)",
    "howls": "울부짖다 (동사)",
    "lonely": "외로운 (형용사)",
    "coyote": "코요테 (명사)",
    "more": "더 많은 (부사)",
    "time": "시간 (명사)",
    "hockey": "하키 (명사)",
    "frozen": "얼어붙은 (형용사)",
    "pond": "연못 (명사)",
    "drinking": "마시는 것 (분사)",
    "hot": "뜨거운 (형용사)",
    "coffee": "커피 (명사)",
    "by": "~옆에 (전치사)",
    "wood": "장작 (형용사)",
    "stove": "난로 (명사)",
    "learn": "배우다 (동사)",
    "rely": "의지하다 (동사)",
    "your": "당신의 (대명사)",
    "neighbours": "이웃들 (명사)",
    "truck": "트럭 (명사)",
    "stuck": "빠지다 (분사)",
    "three": "세 명 (수사)",
    "people": "사람들 (명사)",
    "will": "~할 것이다 (조동사)",
    "stop": "멈추다 (동사)",
    "pull": "끌어내다 (동사)",
    "even": "심지어 (부사)",
    "ask": "부탁하다 (동사)",
    "life": "삶 (명사)",
    "toil": "힘든 노동 (명사)",
    "outweighs": "능가하다 (동사)",
    "sweat": "땀 (명사)",
    "keep": "유지하다 (동사)",
    "stick": "스틱 (명사)",
    "ice": "얼음 (명사)",
    "this": "이 (대명사)",
    "most": "가장 (부사)",
    "beautiful": "아름다운 (형용사)",
    "place": "장소 (명사)",
}

# Ordered list — index used as filename for sentences
SENTENCES_UK = [
    ("welcome to the prairies.", "Ласкаво просимо до прерій."),
    ("i farm out near kindersley, saskatchewan.", "Я фермерую неподалік Кіндерслі, Саскачеван."),
    ("when you look around here, the sky is so big it feels like it might swallow you whole.", "Коли ви озираєтесь навколо, небо таке велике, що здається, ніби воно може проковтнути вас цілком."),
    ("some folks think there is not much going on out here.", "Деякі люди думають, що тут мало що відбувається."),
    ("they think it is just flat land and wheat, like that old comedy show about the gas station in the middle of nowhere.", "Вони думають, що це просто рівнинна земля і пшениця, як у тому старому комедійному шоу про заправку посеред нічого."),
    ("but they are missing the best parts.", "Але вони пропускають найкраще."),
    ("farming is hard work.", "Фермерство — це важка праця."),
    ("you wake up before the sun, and you go to bed long after the mosquitoes come out.", "Ви прокидаєтеся до сходу сонця і лягаєте спати довго після того, як з'являються комарі."),
    ("spring is a race against the clock.", "Весна — це гонка з часом."),
    ("we drive tractors the size of small houses, planting canola and barley until our eyes blur.", "Ми водимо трактори розміром з невеликі будинки, сіючи канолу та ячмінь, поки в очах не помутніє."),
    ("we worry about rain, we worry about frost, and we fix broken machinery with whatever we have.", "Ми хвилюємося через дощ, хвилюємося через мороз і лагодимо зламану техніку тим, що є під рукою."),
    ('like red green always said on television, "i am a man, but i can change, if i have to, i guess."', "Як завжди казав Ред Грін по телевізору: «Я чоловік, але я можу змінитися, якщо доведеться, мабуть»."),
    ("out here, changing mostly means learning how to rebuild a diesel engine in the dark.", "Тут зміни переважно означають навчання тому, як перебрати дизельний двигун у темряві."),
    ("but the joy is in the quiet moments.", "Але радість полягає в тихих моментах."),
    ("there is nothing like the smell of the earth after a summer storm.", "Немає нічого кращого за запах землі після літньої грози."),
    ("you can sit on the porch and watch the lightning dance across the horizon fifty miles away.", "Ви можете сидіти на ґанку і дивитися, як блискавка танцює на горизонті за п'ятдесят миль звідси."),
    ("in the fall, when the harvest is done, the whole town gets together for a supper at the community hall.", "Восени, коли зібрано урожай, усе місто збирається на вечерю в громадському залі."),
    ("we share pies, we share stories, and we laugh until our ribs hurt.", "Ми ділимося пирогами, історіями і сміємося так, що аж ребра болять."),
    ("winter is long and cold, sure.", "Зима довга і холодна, звичайно."),
    ("the snow piles up to the windows, and the wind howls like a lonely coyote.", "Сніг намітає аж до вікон, а вітер виє, як самотній койот."),
    ("but that just means more time for hockey on the frozen pond and drinking hot coffee by the wood stove.", "Але це просто означає більше часу для хокею на замерзлому ставку та пиття гарячої кави біля дров'яної печі."),
    ("you learn to rely on your neighbours.", "Ви вчитеся покладатися на своїх сусідів."),
    ("if your truck gets stuck in the snow, three people will stop to pull you out before you even ask.", "Якщо ваша вантажівка застрягне в снігу, троє людей зупиняться, щоб витягнути вас, ще до того, як ви попросите."),
    ("so, it is a life of toil, but the joy outweighs the sweat.", "Отже, це життя в тяжкій праці, але радість переважає піт."),
    ("keep your stick on the ice, work hard, and you will find that this flat land is the most beautiful place on earth.", "Тримай ключку на льоду, працюй наполегливо, і ти зрозумієш, що ця рівнинна земля — найпрекрасніше місце на світі."),
]

SENTENCES_KO = [
    ("welcome to the prairies.", "초원에 오신 것을 환영합니다."),
    ("i farm out near kindersley, saskatchewan.", "저는 서스캐처원주 킨더슬리 근처에서 농사를 짓습니다."),
    ("when you look around here, the sky is so big it feels like it might swallow you whole.", "여기서 주위를 둘러보면, 하늘이 너무 커서 당신을 통째로 삼킬 것 같은 느낌이 듭니다."),
    ("some folks think there is not much going on out here.", "일부 사람들은 이곳에서 별로 일어나는 일이 없다고 생각합니다."),
    ("they think it is just flat land and wheat, like that old comedy show about the gas station in the middle of nowhere.", "그들은 이곳이 그냥 평평한 땅과 밀뿐이라고, 마치 아무데도 없는 곳의 주유소에 대한 옛날 코미디 쇼처럼 생각합니다."),
    ("but they are missing the best parts.", "하지만 그들은 가장 좋은 부분들을 놓치고 있습니다."),
    ("farming is hard work.", "농사는 힘든 일입니다."),
    ("you wake up before the sun, and you go to bed long after the mosquitoes come out.", "해가 뜨기 전에 일어나고, 모기가 나온 후 한참이 지나서야 잠자리에 듭니다."),
    ("spring is a race against the clock.", "봄은 시간과의 싸움입니다."),
    ("we drive tractors the size of small houses, planting canola and barley until our eyes blur.", "우리는 작은 집만한 크기의 트랙터를 몰며, 눈이 흐려질 때까지 카놀라와 보리를 심습니다."),
    ("we worry about rain, we worry about frost, and we fix broken machinery with whatever we have.", "비를 걱정하고, 서리를 걱정하며, 있는 것으로 고장난 기계를 고칩니다."),
    ('like red green always said on television, "i am a man, but i can change, if i have to, i guess."', "레드 그린이 텔레비전에서 항상 말했듯이, 나는 남자지만, 변할 수 있어, 꼭 해야 한다면, 아마도."),
    ("out here, changing mostly means learning how to rebuild a diesel engine in the dark.", "이곳에서 변한다는 것은 주로 어둠 속에서 디젤 엔진을 분해하는 법을 배우는 것을 의미합니다."),
    ("but the joy is in the quiet moments.", "하지만 기쁨은 조용한 순간들 속에 있습니다."),
    ("there is nothing like the smell of the earth after a summer storm.", "여름 폭풍 후 흙 냄새 같은 것은 없습니다."),
    ("you can sit on the porch and watch the lightning dance across the horizon fifty miles away.", "베란다에 앉아 오십 마일 떨어진 지평선 너머로 번개가 춤추는 것을 볼 수 있습니다."),
    ("in the fall, when the harvest is done, the whole town gets together for a supper at the community hall.", "가을에 수확이 끝나면, 온 마을이 공동체 홀에서 저녁 식사를 위해 모입니다."),
    ("we share pies, we share stories, and we laugh until our ribs hurt.", "우리는 파이를 나누고, 이야기를 나누며, 갈비뼈가 아플 때까지 웃습니다."),
    ("winter is long and cold, sure.", "겨울은 길고 춥습니다, 물론이죠."),
    ("the snow piles up to the windows, and the wind howls like a lonely coyote.", "눈은 창문까지 쌓이고, 바람은 외로운 코요테처럼 울부짖습니다."),
    ("but that just means more time for hockey on the frozen pond and drinking hot coffee by the wood stove.", "하지만 그것은 단지 얼어붙은 연못에서 하키를 하고 장작 난로 옆에서 뜨거운 커피를 마실 시간이 더 많아진다는 것을 의미합니다."),
    ("you learn to rely on your neighbours.", "당신은 이웃들에게 의지하는 법을 배웁니다."),
    ("if your truck gets stuck in the snow, three people will stop to pull you out before you even ask.", "트럭이 눈에 빠지면, 당신이 부탁하기도 전에 세 명이 멈춰서 끌어내 줄 것입니다."),
    ("so, it is a life of toil, but the joy outweighs the sweat.", "그래서, 이것은 힘든 노동의 삶이지만, 기쁨이 땀보다 더 큽니다."),
    ("keep your stick on the ice, work hard, and you will find that this flat land is the most beautiful place on earth.", "스틱을 얼음 위에 올려놓고, 열심히 일하면, 이 평평한 땅이 지구에서 가장 아름다운 곳임을 알게 될 것입니다."),
]

# ── Generate ──────────────────────────────────────────────────────────────────

def run():
    tasks = []  # (text, voice_id, path)

    # Words
    for en_word, uk_text in WORDS_UK.items():
        key = normalize_key(en_word)
        tasks.append((clean_for_tts(uk_text, 'uk'), VOICE_UK, Path(f"audio/uk/words/{key}.mp3")))
    for en_word, ko_text in WORDS_KO.items():
        key = normalize_key(en_word)
        tasks.append((clean_for_tts(ko_text, 'ko'), VOICE_KO, Path(f"audio/ko/words/{key}.mp3")))

    # UK/KO Sentences
    for idx, (_, uk_text) in enumerate(SENTENCES_UK):
        tasks.append((uk_text, VOICE_UK, Path(f"audio/uk/sentences/{idx}.mp3")))
    for idx, (_, ko_text) in enumerate(SENTENCES_KO):
        tasks.append((ko_text, VOICE_KO, Path(f"audio/ko/sentences/{idx}.mp3")))

    # English words (the word itself, for natural pronunciation)
    for en_word in WORDS_UK.keys():
        key = normalize_key(en_word)
        tasks.append((en_word, VOICE_EN, Path(f"audio/en/words/{key}.mp3"), SETTINGS_EN))

    # English sentences
    for idx, (en_text, _) in enumerate(SENTENCES_UK):
        # Capitalise first letter for natural TTS
        spoken = en_text[0].upper() + en_text[1:]
        tasks.append((spoken, VOICE_EN, Path(f"audio/en/sentences/{idx}.mp3"), SETTINGS_EN))

    # Full English story
    raw_story = (
        "Welcome to the prairies. I farm out near Kindersley, Saskatchewan. "
        "When you look around here, the sky is so big it feels like it might swallow you whole. "
        "Some folks think there is not much going on out here. "
        "They think it is just flat land and wheat, like that old comedy show about the gas station in the middle of nowhere. "
        "But they are missing the best parts.\n\n"
        "Farming is hard work. You wake up before the sun, and you go to bed long after the mosquitoes come out. "
        "Spring is a race against the clock. We drive tractors the size of small houses, planting canola and barley until our eyes blur. "
        "We worry about rain, we worry about frost, and we fix broken machinery with whatever we have. "
        "Like Red Green always said on television, \"I am a man, but I can change, if I have to, I guess.\" "
        "Out here, changing mostly means learning how to rebuild a diesel engine in the dark.\n\n"
        "But the joy is in the quiet moments. There is nothing like the smell of the earth after a summer storm. "
        "You can sit on the porch and watch the lightning dance across the horizon fifty miles away. "
        "In the fall, when the harvest is done, the whole town gets together for a supper at the community hall. "
        "We share pies, we share stories, and we laugh until our ribs hurt.\n\n"
        "Winter is long and cold, sure. The snow piles up to the windows, and the wind howls like a lonely coyote. "
        "But that just means more time for hockey on the frozen pond and drinking hot coffee by the wood stove. "
        "You learn to rely on your neighbours. "
        "If your truck gets stuck in the snow, three people will stop to pull you out before you even ask.\n\n"
        "So, it is a life of toil, but the joy outweighs the sweat. "
        "Keep your stick on the ice, work hard, and you will find that this flat land is the most beautiful place on earth."
    )
    tasks.append((raw_story, VOICE_EN, Path("audio/en/story.mp3"), SETTINGS_EN))

    total = len(tasks)
    skipped = sum(1 for t in tasks if t[2].exists())
    print(f"Total: {total}  |  Already generated: {skipped}  |  To generate: {total - skipped}\n")

    for i, t in enumerate(tasks):
        text, voice_id, path = t[0], t[1], t[2]
        settings = t[3] if len(t) > 3 else SETTINGS
        print(f"[{i+1}/{total}] {path.name[:28]:28s}  \"{text[:40]}\"")
        if path.exists():
            print(f"  skip  {path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        audio = client.text_to_speech.convert(
            voice_id=voice_id, text=text, model_id=MODEL,
            voice_settings=settings, output_format="mp3_44100_128"
        )
        data = b"".join(audio)
        path.write_bytes(data)
        print(f"  wrote {path}  ({len(data)} bytes)")
        import time; time.sleep(0.35)

    print("\n✅ Done.")

if __name__ == "__main__":
    run()
