import streamlit as st
import matplotlib.pyplot as plt
import os

st.title('段ボール切断サイズ計算アプリ')

# ユーザー入力
card_height = st.number_input('段ボールの高さ', min_value=1)
card_width = st.number_input('段ボールの幅', min_value=1)
prod_width = st.number_input('商品の幅', min_value=1)
prod_depth = st.number_input('商品の奥行き', min_value=1)
prod_height = st.number_input('商品の高さ', min_value=1)

if st.button('計算'):
    try:
        if prod_height + prod_width > card_width:
            st.error("商品サイズの高さ＋幅が段ボールサイズの幅を超えています。")
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

            # 保存して表示
            output_path = 'output.png'
            plt.savefig(output_path)
            plt.close()

            st.success("計算完了")
            st.image(output_path)
    except ValueError:
        st.error("すべてのフィールドに正しい数値を入力してください。")
