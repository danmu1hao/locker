# 出勤汇总システム

このシステムは、従業員の出勤記録を管理し、日別の出勤汇总データを表示するWebアプリケーションです。

## 機能

- ユーザー情報の管理
- アクセスログ（打卡記録）の管理
- 日別出勤汇总データの自動生成
- Webインターフェースでのデータ表示

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. データベースの初期化

```bash
python DB.py
```

これにより、サンプルデータが含まれたデータベースが作成されます。

### 3. APIサーバーの起動

```bash
python api_server.py
```

サーバーは `http://localhost:5000` で起動します。

## 使用方法

### APIエンドポイント

- `GET /api/users` - ユーザー情報を取得
- `GET /api/access_logs` - アクセスログを取得
- `GET /api/attendance_summary` - 出勤汇总データを取得
- `POST /api/update_summary` - 出勤汇总データを更新

### フロントエンド

ブラウザで `index.html` を開いて、出勤汇总データを表示できます。

## データベース構造

### users テーブル
- id: ユーザーID（主キー）
- name: ユーザー名
- role: 役職
- card_id: カードID
- card_name: カード名
- register_date: 登録日

### access_logs テーブル
- id: ログID（主キー）
- user_id: ユーザーID（外部キー）
- timestamp: 打卡時間
- card_id: カードID

### attendance_summary テーブル
- user_id: ユーザーID（複合主キー）
- user_name: ユーザー名
- work_date: 勤務日（複合主キー）
- earliest_time: 最早打卡時間
- latest_time: 最遅打卡時間

## 注意事項

- データベースファイルは `access_control.db` として保存されます
- APIサーバーはポート5000で動作します
- フロントエンドはAPIサーバーが起動している必要があります 