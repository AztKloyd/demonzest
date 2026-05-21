---
id: js-001
courseId: javascript
title: JavaScriptとは何か
description: ブラウザで動くプログラミング言語としてのJavaScriptを学びます。
phase: 2
order: 1
level: beginner
estimatedMinutes: 25
tags:
  - javascript
  - frontend
  - beginner
---

# JavaScriptとは何か

## 今日学ぶこと

- JavaScriptがどこで使われるか
- HTML、CSS、JavaScriptの役割
- 変数と関数の基本
- 現場でJavaScriptが重要な理由

## JavaScriptは画面を動かす言語

JavaScriptは、Webページに動きをつけるためによく使われるプログラミング言語です。

ボタンを押したらメニューを開く、入力内容をチェックする、APIからデータを取得する、という処理に使われます。

## HTML、CSS、JavaScript

Web画面は主に3つの技術で作られます。

- HTML: 画面の構造を作る
- CSS: 見た目を整える
- JavaScript: 動きを作る

たとえばログイン画面なら、入力欄はHTML、色や余白はCSS、ログインボタンを押した後の処理はJavaScriptです。

## 変数

変数は、値に名前をつけて保存する箱のようなものです。

```javascript
const userName = "Taro";
```

この例では、`userName` という名前で `"Taro"` を保存しています。

## 関数

関数は、処理に名前をつけて再利用できるようにしたものです。

```javascript
function greet(name) {
  return "Hello, " + name;
}
```

関数を使うと、同じ処理を何度も書かずに済みます。

## 実際の開発では

ReactやAngularなどのフロントエンドフレームワークも、JavaScriptやTypeScriptを使って動きます。

そのため、フレームワークを学ぶ前にJavaScriptの基本を知っておくと理解が速くなります。

## まとめ

- JavaScriptはWeb画面に動きをつける言語です。
- HTMLは構造、CSSは見た目、JavaScriptは動きを担当します。
- 変数は値を保存する名前付きの箱です。
- 関数は処理を再利用するためのまとまりです。

## Quiz

```quiz
id: js-001-q1
type: fill_blank
question: Web画面で動きを担当することが多い言語は ______ です。
answer: JavaScript
explanation: JavaScriptはボタン操作やAPI通信など、画面の動きを作るためによく使われます。
```

```quiz
id: js-001-q2
type: code_output
question: 次のコードの結果は何ですか。 const count = 2 + 3;
answer: 5
explanation: 2 + 3 の計算結果は 5 です。
```
