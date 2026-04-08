# キャラクター利用ガイド

## キャラクターの役割

| キャラクター | 役割 | 性格 |
|------------|------|------|
| **ガネーシャ🐘** | 導き手。本質を例え話とユーモアで伝える | 自信満々でズボラ、関西弁、核心を突くアドバイス |
| **ナツキ👩‍💻** | 読者の代弁者。素朴な疑問と鋭いツッコミ | 標準語、積極的に質問、ガネーシャの矛盾を見逃さない |

---

## 🐘 ガネーシャのキャラクター設定（必ず守ること！）

- 一人称：「ワシ」、ナツキ：「お前」
- 自信満々でズボラな性格、ユーモラスに核心を突くアドバイス
- 偉人を「ワシの教え子」と称し、「エジソンくん」「ナポレオンちゃん」のように呼ぶ
  ※テーマに合った様々な偉人を選ぶこと
- おちゃらけと真面目の絶妙なバランス
- 関西弁（〜やで、〜せなアカン、まぁええやんけ）を使用
- 「さすガネーシャや！」と自画自賛多め
- 朝はトイレで「🎵ガネ・ガネ・ガネーシャモーニング🎵」と歌う
- 好物はあんみつ🍨（「教えて欲しかったらお供えもんが必要やな」とせがむ）
- 親友は釈迦、漫才風の掛け合いで「はい、Oh, My God!!」と決めポーズ

---

## 表情の使い分け

### ガネーシャ🐘（6種類）

| 表情 | ファイル名 | 使用シーン |
|-----|----------|----------|
| 標準 | `ganesha.png` | 通常の説明、質問、導入、たとえ話の開始 |
| 得意げ | `ganesha-得意げ.png` | 自画自賛「さすガネーシャや！」、偉人エピソード自慢、知識を披露 |
| 焦り | `ganesha-焦り.png` | ナツキの鋭いツッコミに動揺、嘘がバレそう、想定外の質問 |
| 誤魔化し | `ganesha-誤魔化し.png` | ごまかし・はぐらかし、間違いを指摘されて照れ、話題をそらす |
| ボケをかます | `ganesha-ボケをかます.png` | ボケ・ジョーク、あんみつネタ、偉人の嘘エピソード、ふざけた発言 |
| 決めポーズ | `ganesha-決めポーズ.png` | 「はい、Oh, My God!! 🙏✨」、重要な結論、章の締めくくり |

配分の目安: 標準40〜50%、得意げ15%、ボケをかます15%、焦り10%、誤魔化し10%、決めポーズ5〜10%（締めに1回は必ず使う）

### ナツキ👩‍💻（6種類）

| 表情 | ファイル名 | 使用シーン |
|-----|----------|----------|
| 標準 | `natsuki.png` | 通常の質問、相槌、説明を聞いているとき |
| 笑顔 | `natsuki-笑顔.png` | 理解した瞬間、納得したとき、嬉しいとき |
| 呆れ | `natsuki-呆れ.png` | ガネーシャのボケやふざけへのツッコミ、呆れたとき |
| 疑問 | `natsuki-疑問.png` | 説明が難しくてついていけないとき、「え、どういうこと？」 |
| 感動 | `natsuki-感動.png` | 深く感動したとき、「すごい…！」 |
| 怒る | `natsuki-怒る.png` | 強いツッコミ、ふざけすぎへの反応、「ちゃんと教えてください！」 |

配分の目安: 標準40〜50%、呆れ15%、笑顔15%、疑問10%、感動10%、怒る5〜10%

---

## 対話パターン

### 1. 導入パターン（疑問→答え）

```html
<!-- ガネーシャ: たとえ話で概要説明 -->
<div class="flex items-start gap-3 my-6">
  <img src="images/ganesha.png" class="w-24 h-24 rounded-full border-2 border-gv-ganesha object-cover flex-shrink-0" alt="ガネーシャ">
  <div class="relative bg-white border border-gv-ganesha rounded-xl p-4 shadow-sm max-w-[calc(100%-108px)]" style="box-shadow: 0 1px 3px rgba(245,158,11,0.15)">
    <div class="absolute top-5 -left-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-r-[9px] border-r-gv-ganesha border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -left-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-r-[7px] border-r-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">ええか、「フック」ってのは要するに<strong class="text-gv-secondary font-bold">割り込みポイント</strong>のことや。会社のセキュリティゲートを想像してみ？</p>
  </div>
</div>

<!-- ナツキ: 疑問を投げかける -->
<div class="flex items-start gap-3 my-6 flex-row-reverse">
  <img src="images/natsuki-疑問.png" class="w-20 h-20 rounded-full border-2 border-gv-natsuki object-cover flex-shrink-0" alt="ナツキ">
  <div class="relative bg-white border border-gv-natsuki rounded-xl p-4 shadow-sm max-w-[calc(100%-96px)]" style="box-shadow: 0 1px 3px rgba(129,140,248,0.15)">
    <div class="absolute top-5 -right-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-l-[9px] border-l-gv-natsuki border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -right-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-l-[7px] border-l-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">セキュリティゲート…？プログラムに門番がいるってことですか？</p>
  </div>
</div>
```

### 2. 驚きパターン（発見の瞬間）

```html
<div class="flex items-start gap-3 my-6 flex-row-reverse">
  <img src="images/natsuki-笑顔.png" class="w-20 h-20 rounded-full border-2 border-gv-natsuki object-cover flex-shrink-0" alt="ナツキ">
  <div class="relative bg-white border border-gv-natsuki rounded-xl p-4 shadow-sm max-w-[calc(100%-96px)]" style="box-shadow: 0 1px 3px rgba(129,140,248,0.15)">
    <div class="absolute top-5 -right-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-l-[9px] border-l-gv-natsuki border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -right-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-l-[7px] border-l-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">あ、そういうことか！つまりAIが何かする前に「ちょっと待って！」って止められるんですね！</p>
  </div>
</div>
```

### 3. ツッコミパターン（矛盾の指摘）

```html
<div class="flex items-start gap-3 my-6 flex-row-reverse">
  <img src="images/natsuki-呆れ.png" class="w-20 h-20 rounded-full border-2 border-gv-natsuki object-cover flex-shrink-0" alt="ナツキ">
  <div class="relative bg-white border border-gv-natsuki rounded-xl p-4 shadow-sm max-w-[calc(100%-96px)]" style="box-shadow: 0 1px 3px rgba(129,140,248,0.15)">
    <div class="absolute top-5 -right-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-l-[9px] border-l-gv-natsuki border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -right-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-l-[7px] border-l-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">…それ、さっきの説明と矛盾してません？</p>
  </div>
</div>

<div class="flex items-start gap-3 my-6">
  <img src="images/ganesha-誤魔化し.png" class="w-24 h-24 rounded-full border-2 border-gv-ganesha object-cover flex-shrink-0" alt="ガネーシャ">
  <div class="relative bg-white border border-gv-ganesha rounded-xl p-4 shadow-sm max-w-[calc(100%-108px)]" style="box-shadow: 0 1px 3px rgba(245,158,11,0.15)">
    <div class="absolute top-5 -left-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-r-[9px] border-r-gv-ganesha border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -left-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-r-[7px] border-r-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">い、いや…それはやな…あれや、ワシの教え子のアインシュタインくんも言うてたで、「矛盾は理解の始まり」って！</p>
  </div>
</div>
```

### 4. まとめパターン（決めポーズ）

```html
<div class="flex items-start gap-3 my-6">
  <img src="images/ganesha-決めポーズ.png" class="w-24 h-24 rounded-full border-2 border-gv-ganesha object-cover flex-shrink-0" alt="ガネーシャ">
  <div class="relative bg-white border border-gv-ganesha rounded-xl p-4 shadow-sm max-w-[calc(100%-108px)]" style="box-shadow: 0 1px 3px rgba(245,158,11,0.15)">
    <div class="absolute top-5 -left-[9px] w-0 h-0 border-t-[7px] border-t-transparent border-r-[9px] border-r-gv-ganesha border-b-[7px] border-b-transparent"></div>
    <div class="absolute top-5 -left-[7px] w-0 h-0 border-t-[6px] border-t-transparent border-r-[7px] border-r-white border-b-[6px] border-b-transparent"></div>
    <p class="text-[15px] leading-relaxed text-slate-800">はい、Oh, My God!! 🙏✨</p>
  </div>
</div>
```

---

## セリフの書き方

### ガネーシャの特徴

- **一人称**: 「ワシ」
- **口調**: 関西弁（〜やで、〜せなアカン、まぁええやんけ）
- **説明**: たとえ話を必ず使う
- **偉人ネタ**: 「ワシの教え子のエジソンくんもな…」
- **自画自賛**: 「さすガネーシャや！✨」

```
❌ 悪い例: 「それは違います」「こうしてください」
✅ 良い例: 「あのなぁ、ワシの教え子のエジソンくんもな、最初は同じこと言うてたで」
```

### ナツキの特徴

- **一人称**: 「私」
- **口調**: 標準語、丁寧語
- **質問**: 素朴な疑問を投げかける
- **ツッコミ**: ガネーシャのボケや矛盾を見逃さない

```
❌ 悪い例: 「すごいですね！」「なるほど！」（薄い反応）
✅ 良い例: 「…それ、さっき言ってたことと矛盾してません？」「具体的にはどういうことですか？」
```

---

## 配置ルール

1. **ガネーシャは左配置**: `flex items-start gap-3 my-6`、アバター `w-24 h-24`
2. **ナツキは右配置**: `flex items-start gap-3 my-6 flex-row-reverse`、アバター `w-20 h-20`
3. **太字**: `<strong class="text-gv-secondary font-bold">キーワード</strong>`
4. **1吹き出し最大150文字**（超えるなら分割）
5. **同じキャラの連続発言は3回以内**

---

## 画像パス

HTML内での参照パス:

```html
<!-- デフォルト -->
images/ganesha.png
images/natsuki.png

<!-- バリアント -->
images/ganesha-{バリアント名}.png
images/natsuki-{バリアント名}.png
```

アバター画像の実体:

```
.claude/assets/avatars/ganesha/
.claude/assets/avatars/natsuki/
```
