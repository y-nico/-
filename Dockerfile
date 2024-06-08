# ベースイメージ
FROM python:3.8-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコピー
COPY . .

# ポートの指定
EXPOSE 8501

# アプリケーションの実行
CMD ["streamlit", "run", "app.py"]
