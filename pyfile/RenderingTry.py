from jinja2 import Template, Environment, FileSystemLoader
import json
def rendering(template, parameter, result):
    #テンプレート読み込み
    env = Environment(loader=FileSystemLoader('../templates', encoding='utf8'))
    tmpl = env.get_template(f"{template}")

    # 設定ファイル読み込み
    with open('../result/json/' + parameter, encoding='utf-8') as f:
        params = json.load(f)

    # レンダリングしてhtml出力
    rendered_html = tmpl.render(params)
    try:
        with open(f'mysite/view/{result}', 'w', encoding='utf-8') as f:
            f.write(rendered_html)
    except FileNotFoundError:
        print(f'{result}のhtmlソースの出力に失敗しました')

#テンプレートへの埋め込みテスト
#rendering関数
#第一引数:使うテンプレートファイル名,第二引数:埋め込むデータが格納されているjsonファイル名,第三引数:出力するhtmlの名前