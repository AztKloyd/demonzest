---
id: api-001
courseId: api
title: APIとは何か
description: フロントエンドとバックエンドをつなぐAPIの基本を学びます。
phase: 2
order: 1
level: beginner
estimatedMinutes: 25
tags:
  - api
  - backend
  - beginner
---

# APIとは何か

## 今日学ぶこと

- APIが何をするものか
- エンドポイントとは何か
- リクエストとレスポンスの中身
- JSONの基本

## APIはアプリ同士の窓口

APIは、アプリ同士がやり取りするための窓口です。

フロントエンドはAPIを通してバックエンドにお願いを送ります。

バックエンドはAPIを通して結果を返します。

## エンドポイント

エンドポイントは、APIの具体的な住所です。

たとえばこのアプリでは、ログインAPIは次のような住所です。

```text
POST /api/auth/login
```

`POST` は目的、`/api/auth/login` は場所です。

## JSON

APIではJSONという形式でデータを送ることが多いです。

```json
{
  "email": "admin@example.com",
  "password": "admin-password123"
}
```

JSONは、名前と値のセットでデータを表します。

## 実際の開発では

フロントエンドとバックエンドの間では、「どのAPIに何を送るか」「何が返ってくるか」を決めます。

この約束が曖昧だと、画面とAPIがうまくつながりません。

## まとめ

- APIはアプリ同士がやり取りするための窓口です。
- エンドポイントはAPIの住所です。
- APIではJSONでデータを送ることが多いです。
- APIの約束がはっきりしていると開発しやすくなります。

## Quiz

```quiz
id: api-001-q1
type: fill_blank
question: APIの具体的な住所を ______ と呼びます。
answer: エンドポイント
explanation: エンドポイントはAPIを呼び出すための具体的なURLやパスです。
```

```quiz
id: api-001-q2
type: short_answer
question: フロントエンドがAPIを使う理由を短く説明してください。
sampleAnswer: バックエンドにデータ取得や保存などの処理をお願いするためです。
keywords:
  - バックエンド
  - データ
  - 処理
```
