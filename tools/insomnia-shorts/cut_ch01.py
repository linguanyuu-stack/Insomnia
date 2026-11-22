"""Cut the user's ch01 narration (one take, with stray "Bethany"/"Jack" from the TTS tool) into beat clips.

Segments were found with sherpa-onnx (whisper-small + paraformer-zh) on books/insomnia-shorts/audio-src/ch01-raw.wav.
Each stray word lies in a pause of its own or at a segment's head (cut at the silence after it), so every kept
segment is cut alone and the stray words between them never enter a clip. Marks inside a segment are placed by
character proportion; every clip is levelled to -14 LUFS.

    python3 tools/insomnia-shorts/cut_ch01.py
"""
import json, re, subprocess
from pathlib import Path

RAW = "books/insomnia-shorts/audio-src/ch01-raw.wav"
OUT = Path("site/insomnia-shorts/ch01/audio/zh-TW"); OUT.mkdir(parents=True, exist_ok=True)
PAD = .12
# beat: list of (start, end, text with [[marks]]); "|" splits a segment's text into caption lines
B = {
 "hook":  [(1.32, 2.72, "你身體裡有一支錶，"), (3.18, 5.60, "[[slow]]每天都會慢十分鐘。")],
 "claim": [(6.34, 7.82, "這不是養生說法，"), (8.12, 9.74, "是拿過[[nobel]]諾貝爾獎的科學。")],
 "mimosa":[(12.58, 13.54, "[[year]]1729 年，"), (13.84, 16.00, "天文學家[[dm]]德梅朗把一盆[[plant]]含羞草，"), (16.30, 17.48, "[[shut]]關進不透光的櫃子。")],
 "dark":  [(19.78, 23.74, "看不到太陽，|葉子照樣[[open]]白天張開、|[[close]]晚上合起。")],
 "plant": [(25.12, 26.10, "植物身體裡，"), (26.54, 27.58, "[[clock]]有自己的時鐘。")],
 "cave":  [(28.20, 29.42, "[[year]]1938 年，"), (29.70, 33.28, "睡眠研究之父[[k]]克萊特曼，|[[cave]]搬進美國猛瑪洞的地底，"), (33.60, 34.42, "[[month]]住了一個多月。")],
 "drift": [(36.34, 37.96, "沒有陽光、沒有時鐘，"), (38.46, 40.44, "[[sleep]]人照樣規律地睡和醒，"), (41.14, 43.20, "[[drift]]只是每天往後飄一點。")],
 "period":[(44.82, 46.32, "後來[[harvard]]哈佛團隊量到："), (46.66, 48.06, "人體時鐘一圈，"), (48.30, 51.12, "平均大約[[count]]二十四小時又十分鐘。")],
 "flies": [(52.50, 53.48, "時鐘藏在哪？"), (53.92, 54.92, "答案來自[[fly]]果蠅。"), (55.36, 59.58, "有的突變果蠅，|一天只有[[f19]]十九小時，|有的長達[[f28]]二十八小時。")],
 "gene":  [(61.34, 62.88, "壞掉的都是[[gene]]同一個基因，"), (63.22, 63.74, "[[per]]period。"), (64.52, 66.52, "解開它怎麼計時的[[three]]三位科學家，"), (66.88, 68.90, "拿下 [[prize]]2017 年諾貝爾獎。")],
 "scn":   [(70.24, 72.10, "人體幾乎[[cells]]每個細胞都有時鐘，"), (72.90, 75.60, "[[boss]]總指揮在視神經交叉的正上方，"), (75.92, 77.38, "叫[[scn]]視交叉上核。")],
 "light": [(78.58, 81.90, "它用[[eye]]眼睛看到的光，|幫全身[[sync]]對時。")],
 "sun":   [(82.56, 86.04, "所以早上那道[[sun]]陽光，|就是每天幫你的錶[[set]]對時。"), (86.42, 88.66, "少了它，|錶就[[lag]]一天一天慢下去。")],
 "next":  [(89.36, 89.98, "下一集："), (90.58, 92.76, "[[next]]為什麼晚上會想睡？")],
}
MARK = re.compile(r"\[\[(\w+)\]\]")


def weight(s):
    """Spoken weight: a CJK character or a digit (read one by one in Chinese) is 1, a Latin letter about a third."""
    n = 0
    for ch in MARK.sub("", s):
        if ch.isdigit() or '一' <= ch <= '鿿': n += 1
        elif ch.isalpha(): n += .35
    return n


def main():
    tim = {}
    for beat, segs in B.items():
        k = len(segs)
        chains = ";".join(f"[s{i}]atrim={max(0, s - PAD):.3f}:{e + PAD:.3f},asetpts=PTS-STARTPTS[a{i}]" for i, (s, e, _) in enumerate(segs))
        flt = (f"[0]asplit={k}" + "".join(f"[s{i}]" for i in range(k)) + ";" + chains + ";" +
               "".join(f"[a{i}]" for i in range(k)) + f"concat=n={k}:v=0:a=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[o]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", RAW, "-filter_complex", flt, "-map", "[o]", "-ac", "1",
                        "-b:a", "128k", str(OUT / f"{beat}.mp3")], check=True, stdin=subprocess.DEVNULL)
        marks, cues, off = {}, [], 0.0
        for s, e, txt in segs:
            a, b = max(0, s - PAD), e + PAD
            total, done = weight(txt) or 1, 0
            for line in txt.split("|"):
                cues.append([round(off + (s - a) + (e - s) * done / total, 2), MARK.sub("", line).rstrip("，。：、").strip()])
                lw = 0
                for p in re.split(r"(\[\[\w+\]\])", line):
                    m = MARK.fullmatch(p)
                    if m: marks[m.group(1)] = round(off + (s - a) + (e - s) * (done + lw) / total, 2)
                    else: lw += weight(p)
                done += lw
            off += b - a
        dur = float(subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(OUT / f"{beat}.mp3")], capture_output=True, text=True).stdout)
        tim[beat] = {"dur": round(dur, 2), "marks": marks, "cues": cues}
    # the series card is wordless: a silent clip of two seconds
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2", "-b:a", "64k",
                    str(OUT / "card.mp3")], check=True, stdin=subprocess.DEVNULL)
    tim["card"] = {"dur": 2.0, "marks": {}, "cues": []}
    (OUT / "timings.js").write_text("window.TIMINGS = " + json.dumps(tim, ensure_ascii=False, indent=1) + ";\n")
    print({k: v["dur"] for k, v in tim.items()}, "total", round(sum(v["dur"] for v in tim.values()), 1))


if __name__ == "__main__":
    main()
