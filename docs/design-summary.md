# demonzest Design Summary

## Purpose

`demonzest` is a development-focused learning web application for Korean junior developers working in Japanese development teams.

The main goal is not Japanese language study by itself. The app teaches practical development knowledge first, while exposing learners to simple Japanese expressions commonly used in Japanese engineering workplaces.

## Target Users

- Korean junior engineers already working in Japanese companies.
- Learners who need to understand development work, tickets, code reviews, APIs, databases, and team communication.
- Small-group use, not a large public service.

## Final Tech Stack

- Frontend: Angular
- Backend: FastAPI
- Database: PostgreSQL
- Content: Markdown files
- Authentication: FastAPI-managed login
- UI direction: DevTool-like learning console

## Learning Roadmap

1. Web development overview
2. Git / GitHub
3. JavaScript
4. TypeScript
5. React
6. API
7. SQL / Database
8. Python backend
9. Java / Spring
10. Japanese development practice
11. Certifications / career

## Content Policy

- Japanese only.
- No Korean supplemental explanations.
- Use very simple Japanese.
- Explain hard terms with easier Japanese.
- Each lesson should connect concepts to real development work.

## Content Storage

Lesson content is stored as Markdown files under `content/`.

PostgreSQL stores only user-specific learning data:

- Users
- Progress
- Last viewed position
- Notes
- Quiz attempts
- Quiz answers
- Wrong answers
- Settings

## Lesson Format

Each lesson should use frontmatter and a consistent section structure.

```md
---
id: web-001
courseId: web-basics
title: Webアプリとは何か
description: Webアプリの基本的な仕組みを学びます。
phase: 1
order: 1
level: beginner
estimatedMinutes: 20
tags:
  - web
  - beginner
---

# Webアプリとは何か

## 今日学ぶこと

## まず一言でいうと

## やさしい例え

## 基本の説明

## 実際の開発では

## よく使う言葉

## よくある勘違い

## ミニ演習

## Quiz

## まとめ
```

## Quiz Types

Initial quiz types:

- `fill_blank`
- `code_output`
- `short_answer`

Short answers are not automatically graded at first. The app should show a sample answer so the learner can compare.

## Current Implementation Status

Implemented so far:

- FastAPI app skeleton
- Health check API
- Database health check API
- SQLAlchemy DB session setup
- Alembic setup
- User SQLAlchemy model
- Initial users table migration
- Password hashing helper
- User creation API
- Login API
- JWT access token creation
- Current-user dependency
- `GET /api/me`

Next planned step:

- Restrict user creation to admins.
- Add a safer development seed script for the first admin user.
