---
id: algo-002
title: Even or Odd
difficulty: bronze
level: beginner
order: 2
tags:
  - condition
  - modulo
timeLimitMs: 1000
memoryLimitMb: 128
examples:
  - input: "4"
    output: "Even"
    explanation: "4 は 2 で割り切れるので偶数です。"
  - input: "7"
    output: "Odd"
    explanation: "7 は 2 で割り切れないので奇数です。"
---

# 問題

整数 `N` が与えられます。
`N` が偶数なら `Even`、奇数なら `Odd` と出力してください。

## 入力

1行に整数 `N` が与えられます。

## 出力

偶数なら `Even`、奇数なら `Odd` と出力してください。

## 制約

- `0 <= N <= 1000`

## 考え方

偶数か奇数かを調べるには、`N` を 2 で割った余りを見ます。
余りが 0 なら偶数、そうでなければ奇数です。
