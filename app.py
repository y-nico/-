import matplotlib
matplotlib.use('Agg')  # バックエンドを変更
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        card_height = int(request.form['card_height'])
        card_width = int(request.form['card_width'])
        prod_width = int(request.form['prod_width'])
        prod_depth = int(request.form['prod_depth'])
        prod_height = int(request.form['prod_height'])

        # 商品サイズの高さ + 幅 が段ボールサイズの幅を超える場合のエラーメッセージ
        if prod_height + prod_width > card_width:
            return render_template('result.html', result="商品サイズの高さ＋幅が段ボールサイズの幅を超えています。", prod_width=prod_width, prod_depth=prod_depth, prod_height=prod_height)
        else:
            fig, ax = plt.subplots(figsize=(10, 10))
            plt.xlim(0, card_width)
            plt.ylim(0, card_height)

            # Y軸のティックラベルを反転
            ax.set_yticks(range(0, card_height + 1, 10))
            ax.set_yticklabels([str(card_height - i) for i in range(0, card_height + 1, 10)])

            # 右上を起点とするためのX座標とY座標
            start_x = card_width
            start_y = card_height

            # 指定された順番で線を描く
            lines = [
                # 1
                ((start_x, start_y), (start_x - prod_height - prod_width, start_y)),
                # 2
                ((start_x - prod_height - prod_width, start_y), (start_x - prod_height - prod_width, start_y - prod_height - prod_depth - prod_height - prod_depth)),
                # 3
                ((start_x - prod_height - prod_width, start_y - prod_height - prod_depth - prod_height - prod_depth), (start_x - prod_height - prod_width + prod_width + prod_depth, start_y - prod_height - prod_depth - prod_height - prod_depth)),
                # 4
                ((start_x, start_y), (start_x - prod_height, start_y)),
                # 5
                ((start_x - prod_height, start_y), (start_x - prod_height, start_y - prod_height - prod_depth - prod_height - prod_depth)),
                # 6
                ((start_x, start_y), (start_x, start_y - prod_height)),
                # 7
                ((start_x, start_y - prod_height), (start_x - prod_height - prod_width, start_y - prod_height)),
                # 8
                ((start_x, start_y), (start_x, start_y - prod_height - prod_depth)),
                # 9
                ((start_x, start_y - prod_height - prod_depth), (start_x - prod_height - prod_width, start_y - prod_height - prod_depth)),
                # 10
                ((start_x, start_y), (start_x, start_y - prod_height - prod_depth - prod_height)),
                # 11
                ((start_x, start_y - prod_height - prod_depth - prod_height), (start_x - prod_height - prod_width, start_y - prod_height - prod_depth - prod_height))
            ]

            for line in lines:
                ax.plot(*zip(*line), color='black')

            # 数値を追加する
            ax.text(start_x - prod_height - prod_width / 2, start_y + 5, f'{prod_height + prod_width}', color='red', ha='center')
            ax.text(start_x - prod_height / 2, start_y + 5, f'{prod_height}', color='red', ha='center')
            ax.text(start_x + 5, start_y - prod_height / 2, f'{prod_height}', color='red', va='center')
            ax.text(start_x + 5, start_y - prod_height - prod_depth / 2, f'{prod_height + prod_depth}', color='red', va='center')
            ax.text(start_x + 5, start_y - prod_height - prod_depth - prod_height / 2, f'{prod_height + prod_depth + prod_height}', color='red', va='center')
            ax.text(start_x + 5, start_y - prod_height - prod_depth - prod_height - prod_depth / 2, f'{prod_height + prod_depth + prod_height + prod_depth}', color='red', va='center')

            plt.gca().set_aspect('equal', adjustable='box')

            # 保存してブラウザで表示
            if not os.path.exists('static'):
                os.makedirs('static')
            output_path = os.path.join('static', 'output.png')
            plt.savefig(output_path)
            plt.close()

            return render_template('result.html', result="計算完了", image_file='output.png', prod_width=prod_width, prod_depth=prod_depth, prod_height=prod_height)
    except ValueError:
        return render_template('result.html', result="すべてのフィールドに正しい数値を入力してください。")

if __name__ == '__main__':
    app.run(debug=True)
