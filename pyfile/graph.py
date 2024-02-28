import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class graph:
    def __init__(self):
        pass

    def radar_chart_layout(self, dd: dict, theta: list, save_name: str,
                        showlegend=True, polar_bgcolor='rgba(0, 0, 0, 0)',
                        radialaxis_visible=True, radialaxis_showline=True,
                        radialaxis_showgrid=True, radialaxis_size=None,
                        radialaxis_gridcolor='black', angularaxis_size=None,
                        angularaxis_linecolor='black',
                        angularaxis_gridcolor='black',
                        gridshape='circular',
                        paper_bgcolor='rgb(255, 255, 255)',):

        plot = []
        print(dd)

        for label, r in dd.items():
            d = go.Scatterpolar(
                r=r,
                theta=theta,
                name=label,
                fill='toself',
            )
            plot.append(d)

        layout = go.Layout(
            template='none',  # テンプレートをオフに
            title='結果(%)',  # レーダーチャートのグラフ全体のタイトル
            showlegend=showlegend,  # 凡例を表示するか否か
            polar=dict(
                bgcolor=polar_bgcolor,  # レーダーチャートの背景色
                radialaxis=dict(  # 軸目盛関係
                    range=(0, 100),
                    visible=radialaxis_visible,  # 目盛、目盛線、グリッドを表示するか否か
                    showline=radialaxis_showline,  # 目盛線を表示するか否か
                    showgrid=radialaxis_showgrid,  # グリッドを表示するか否か
                    tickfont=dict(
                        size=radialaxis_size,  # 目盛のフォントサイズ
                    ),
                    gridcolor=radialaxis_gridcolor,  # グリッドの色を黒に
                ),
                angularaxis=dict(  # レーダーチャートの各項目関係
                    tickfont=dict(
                        size=angularaxis_size,  # 項目のフォントサイズ
                    ),
                    linecolor=angularaxis_linecolor,  # チャート部分の枠線の色
                    gridcolor=angularaxis_gridcolor,  # 各項目から中心に向かう線の色

                ),
                # circularで円形、linearで多角形のレーダーチャート
                gridshape=gridshape,
            ),
            paper_bgcolor=paper_bgcolor,  # グラフ全体の背景色
        )
        fig = go.Figure(data=plot, layout=layout)
        return fig

    def bar_graph_layout(self, df, idx):
        # 各列ごとに "〇", "×", "?" の割合を計算
        proportion_df_list = []
        for i in range(1, 67):
            column_name = f"skill{i}"
            counts = df[column_name].value_counts(normalize=True) * 100
            proportion_df = pd.DataFrame({
                'Response': counts.index,
                'Proportion(%)': counts.values,
                'Question': column_name
            })
            proportion_df_list.append(proportion_df)

        # 結果を結合
        proportion_df = pd.concat(proportion_df_list, ignore_index=True)

        # Response列を"〇", "×", "?"の順にソート
        response_order = ['yes', 'no', 'unknown']
        proportion_df['Response'] = pd.Categorical(proportion_df['Response'], categories=response_order, ordered=True)

        # ソート
        proportion_df = proportion_df.sort_values(by=['Question', 'Response']).reset_index(drop=True)

        # すべての質問と応答が含まれるデータフレームを作成
        all_combinations = pd.DataFrame([(q, r) for q in proportion_df['Question'].unique() for r in response_order], columns=['Question', 'Response'])

        # マージして欠損値を0で埋める
        proportion_df = pd.merge(all_combinations, proportion_df, on=['Question', 'Response'], how='left').fillna(0)

        # プロット
        fig = px.bar(
            proportion_df[proportion_df["Question"]==f"skill{idx}"],
            x='Proportion(%)',
            y='Question',
            color='Response',
            barmode='stack',
            orientation='h',
            labels={'Proportion(%)': 'Proportion (%)'},
            text=proportion_df[proportion_df["Question"]==f"skill{idx}"]['Response'],
            color_discrete_map={'yes': '#00CC96', 'no': '#EF553B', 'unknown': '#7F7F7F'}  # カテゴリごとの色を指定
        )


        fig.update_traces(
                        hovertemplate='%{text}: %{x:0.2f}%',
                        # texttemplate='<b>%{text}: %{x:0.2f}%',
                        # textposition='auto',
                        orientation='h',
                        
                        )
        fig.update_layout(title=dict(text=f"<b>Q{idx}",                            
                                    y=0.85,
                                    ),
                        legend=dict(orientation='h',
                                    xanchor='right',
                                    x=1,
                                    yanchor='bottom',
                                    y=0.92,
                                    title=""
                                    ),
                        width=800, 
                        height=200,
                        plot_bgcolor='white',
                        margin=dict(b=0),
                        # uniformtext_minsize=18,  # テキストの最小サイズを大きくする
                        # uniformtext_mode='hide',  # テキストが重なる場合は非表示にする
                        )
        # テキストを消す
        # fig.update_traces(text=[])
        fig.update_xaxes(linecolor='black', linewidth=1)
        fig.update_xaxes(ticks='inside', tickcolor='black', tickwidth=1, ticklen=5, title=dict(text='<b>回答割合 (%)', font=dict(size=16)))
        fig.update_yaxes(showgrid=False, showticklabels=False, title="")

        return fig