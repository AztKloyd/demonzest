---
id: ts-001
courseId: typescript
title: TypeScriptとは何か
description: JavaScriptに型を追加するTypeScriptの基本を学びます。
phase: 2
order: 1
level: beginner
estimatedMinutes: 25
tags:
  - typescript
  - frontend
  - beginner
---

# TypeScriptとは何か

## 今日学ぶこと

- TypeScriptが何をする言語なのか
- 型とは何か
- JavaScriptとの違い
- 開発現場でTypeScriptがよく使われる理由

## TypeScriptはJavaScriptに型を足した言語

TypeScriptは、JavaScriptをより安全に書くための言語です。

JavaScriptに「この値は文字列です」「この値は数値です」のような型情報を追加できます。

## 型

型は、値の種類を表します。

```typescript
const userName: string = "Taro";
const age: number = 20;
```

`string` は文字列、`number` は数値です。

## 型があると何が嬉しいか

型があると、間違った使い方を早めに見つけられます。

たとえば数値が必要なところに文字列を渡すと、実行前にエラーとして気づけます。

これは人数が多い開発や、大きいアプリで特に役立ちます。

## JavaScriptとの関係

TypeScriptは最終的にJavaScriptへ変換されて動きます。

つまり、ブラウザが直接TypeScriptを理解するというより、開発時にTypeScriptを書いて、実行時はJavaScriptとして動かすイメージです。

## 実際の開発では

React、Angular、Next.jsなどの現場ではTypeScriptがよく使われます。

型があることで、APIの返り値やコンポーネントのpropsを安全に扱いやすくなります。

## まとめ

- TypeScriptはJavaScriptに型を追加する言語です。
- 型は値の種類を表します。
- 型があるとミスを早く見つけやすくなります。
- TypeScriptは最終的にJavaScriptへ変換されます。

## Quiz

```quiz
id: ts-001-q1
type: fill_blank
question: TypeScriptはJavaScriptに ______ を追加する言語です。
answer: 型
explanation: TypeScriptはJavaScriptに型を追加し、開発時のミスを見つけやすくします。
```

```quiz
id: ts-001-q2
type: short_answer
question: TypeScriptを使うと大きい開発でなぜ役立つか、短く説明してください。
sampleAnswer: 型によって値の使い方のミスを早く見つけられ、複数人でも安全に開発しやすくなるからです。
keywords:
  - 型
  - ミス
  - 安全
```
