# 御供養 プロジェクトメモ

## 基本情報
- 運営者：カネ（匿名・会社バレNG）
- GitHub：gokuyou-official/gokuyou
- 公開URL：https://gokuyou-official.github.io/gokuyou/
- Twitter：@gokuyou_bot
- GA：G-8990S70XB8

## 完了済み（2026-03-08）
- [x] GitHub リポジトリ作成（gokuyou-official/gokuyou）
- [x] GitHub Pages 自動デプロイ設定（pushで自動反映）
- [x] OGP設定（両ページ）
- [x] Google Analytics設置（G-8990S70XB8）
- [x] sitemap.xml作成
- [x] レスポンシブ対応（PC：左サイドバー＋右コンテンツ、SP：現状維持）
- [x] チャコール（#3d3d3d）差し色導入
- [x] Twitter・LINEシェアボタン追加（全金言カード）
- [x] ジャンル表記統一（Entertainment/Creative/Sports/Study/Business/Others）
- [x] メンバーバッジ統一（挑戦中・諦めた・探し中）
- [x] 最新記事セクション追加（index.html）
- [x] gokuyou_kingen.htmlの読みやすさ改善

## 次にやること（優先度順）
1. 投稿一覧ページ作成（Googleスプレッドシート連携）
2. 第二回インタビューページ追加（インタビュー確定後）
3. カレンダー投稿機能
4. コメント投稿機能
5. OGP画像（サムネイル）追加
6. 「相方からAIに変えてみた」シリーズ（フェーズ3以降）

## 自律的に進めてよいこと
- 上記機能追加の実装
- デザイン改善
- コンテンツページの新規作成

## 技術スタック
- フロントエンド：HTML/CSS/JS（フレームワークなし）
- ホスティング：GitHub Pages
- デプロイ：GitHub Actions（.github/workflows/deploy.yml）
- データ収集：Googleフォーム → スプレッドシート
- 分析：Google Analytics 4

## ファイル構成
- index.html：トップページ
- gokuyou_kingen.html：敗北者の金言ページ
- sitemap.xml
- .github/workflows/deploy.yml：自動デプロイ設定
