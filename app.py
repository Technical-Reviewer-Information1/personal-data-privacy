import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image, ImageDraw
import io

st.set_page_config(
    page_title="個人情報とプライバシーを学ぼう",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("個人情報とプライバシーを学ぼう 🔒")
st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

# セクション間のスペーシング
st.markdown("---")

# ステップ1: はじめに
st.header("ステップ1: はじめに - あなたの情報は「カギ」である🔑")
st.subheader("個人情報とプライバシーを探る旅へ")

st.write("""
あなたの名前、写真、今いる場所…。それらはすべて、あなたの生活という「家」に入るための「カギ」のようなものです。

この個人情報というカギを不用意にばらまくと、プライバシーが侵害されたり、トラブルに巻き込まれたりするかもしれません。

さあ、カギを安全に管理する方法を学びに行きましょう！
""")

# プライバシーの重要性を示すインタラクティブな図表
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🏠 **あなたの生活**")
    st.write("家族、友達、学校...")
with col2:
    st.markdown("🔑 **個人情報（カギ）**")
    st.write("名前、写真、位置情報...")
with col3:
    st.markdown("⚠️ **リスク**")
    st.write("プライバシー侵害、トラブル...")

st.markdown("---")

# ステップ2: 個人情報クイズ
st.header("ステップ2: SNSアプリに登録！- どれが「個人情報」？")
st.subheader("架空SNS「フォトフレンド」に登録しよう！")

st.write("以下の項目のうち、「個人情報保護法」で定められた「個人情報」にあたると思うものにチェックを入れてください。")

# チェックボックス
name_check = st.checkbox("氏名：鈴木 一郎")
birth_check = st.checkbox("生年月日：2009年5月10日")
animal_check = st.checkbox("好きな動物：犬")
class_check = st.checkbox("学校のクラスの出席番号：3年1組25番")
stats_check = st.checkbox("国の統計データ：「10代男性のスマホ利用率は95%」")

# 答え合わせボタン
if st.button("答え合わせ"):
    st.subheader("【答えと解説】")
    
    # 正解の可視化
    fig = go.Figure(data=[
        go.Bar(
            name='あなたの回答',
            x=['氏名', '生年月日', '好きな動物', 'クラス出席番号', '統計データ'],
            y=[1 if name_check else 0, 1 if birth_check else 0, 1 if animal_check else 0, 1 if class_check else 0, 1 if stats_check else 0],
            marker_color='lightblue'
        ),
        go.Bar(
            name='正解',
            x=['氏名', '生年月日', '好きな動物', 'クラス出席番号', '統計データ'],
            y=[1, 1, 0, 1, 0],
            marker_color='lightgreen'
        )
    ])
    
    fig.update_layout(
        title="個人情報の判定結果",
        xaxis_title="項目",
        yaxis_title="個人情報か？",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 解説
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ **個人情報にあたるもの**")
        st.write("• **氏名**: 特定の個人を識別できる")
        st.write("• **生年月日**: 特定の個人を識別できる")
        st.write("• **クラスの出席番号**: 学校と組み合わせて個人を特定できる")
    
    with col2:
        st.error("❌ **個人情報にあたらないもの**")
        st.write("• **好きな動物**: これだけでは誰のことか分からない")
        st.write("• **統計データ**: 個人を特定できないように加工されている")

st.markdown("---")

# ステップ3: 写真のリスク
st.header("ステップ3: 写真を投稿！- 見えないリスクを見つけよう")
st.subheader("修学旅行の写真を投稿してみよう！")

st.write("""
楽しかった修学旅行の記念写真！友達との思い出に、SNSに投稿します。
顔にはスタンプで加工したし、これなら安全…だよね？
""")

# 写真の代わりにイメージを表示
st.image("https://via.placeholder.com/600x400/87CEEB/FFFFFF?text=修学旅行の写真%0A(顔にスタンプ加工済み)", 
         caption="修学旅行での記念写真（イメージ）", width=500)

if st.button("この写真にひそむリスクを確認する"):
    st.subheader("🚨 この写真に潜むリスク")
    
    # リスクポイントを可視化
    risks = ['背景の建物', '制服', 'ピースサイン', '位置情報(ジオタグ)']
    risk_levels = [85, 70, 30, 95]
    
    fig = px.bar(
        x=risks, 
        y=risk_levels,
        title="写真から特定される可能性のあるリスク（%）",
        color=risk_levels,
        color_continuous_scale="Reds"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # 詳細解説
    st.warning("🏢 **背景の建物**: 有名な建物から、撮影場所が特定される可能性があります。")
    st.warning("👔 **制服**: 学校の制服から、通っている学校が特定される可能性があります。")
    st.warning("✌️ **ピースサイン**: 指紋が読み取られる、という万が一のリスクも…。")
    st.error("📍 **位置情報（ジオタグ）**: 写真には、撮影場所の位置情報が記録されていることがあり、自宅などがバレる危険性も！")
    
    st.info("""
    **💡 重要なポイント**
    
    一枚の写真には、あなたが思っている以上の情報が含まれています。
    投稿する前に「特定される情報はないかな？」と一呼吸おくことが大切です。
    """)

st.markdown("---")

# ステップ4: 日常シーンでの判断
st.header("ステップ4: これってOK？ - 日常のシーンで判断しよう")
st.subheader("身の回りの「これって大丈夫？」を考えよう")

st.write("個人情報やプライバシーに関する、よくある場面です。適切な行動はどちらでしょう？")

tab1, tab2, tab3 = st.tabs(["SNSの公開設定", "フリマアプリの取引", "お得なメール"])

with tab1:
    st.subheader("📱 SNSの公開設定")
    st.write("**状況**: 親友とのツーショット写真を、自分のSNSアカウントに投稿したい！")
    
    choice1 = st.radio(
        "どうする？",
        ["① 写真を載せる許可を友達に取ってから、友達限定で公開する", "② 許可は取らずに、全世界に公開する"],
        key="sns_choice"
    )
    
    if choice1:
        if "①" in choice1:
            st.success("✅ 正解です！")
        else:
            st.error("❌ 不正解です。")
        
        st.info("""
        **解説**: 答えは①です。
        
        他人の写真も、その人の大切な個人情報です。必ず本人の許可を取りましょう。
        また、非公開設定にしていても、フォロワーがスクリーンショットを撮って拡散する可能性はゼロではありません。
        """)

with tab2:
    st.subheader("📦 フリマアプリの取引")
    st.write("**状況**: フリマアプリで商品が売れた！購入者に商品を発送する必要があります。")
    
    choice2 = st.radio(
        "どうする？",
        ["① 自分の住所や氏名を相手に知らせずに送れる「匿名配送」サービスを利用する", "② やりとりが面倒なので、自分の住所や氏名、電話番号を直接メッセージで送る"],
        key="flea_choice"
    )
    
    if choice2:
        if "①" in choice2:
            st.success("✅ 正解です！")
        else:
            st.error("❌ 不正解です。")
        
        st.info("""
        **解説**: 答えは①です。
        
        便利なサービスの裏側では、事業者があなたの個人情報を適切に管理しています。
        むやみに個人情報を他人に教えるのは避けましょう。
        """)

with tab3:
    st.subheader("📧 お得なメール")
    st.write("**状況**: 「100万円当選！下記URLから個人情報を登録！」というメールが届いた。")
    
    choice3 = st.radio(
        "どうする？",
        ["① こんなチャンスは二度とない！急いで個人情報を登録する", "② 怪しいので、URLはクリックせずにメールごと削除する"],
        key="email_choice"
    )
    
    if choice3:
        if "②" in choice3:
            st.success("✅ 正解です！")
        else:
            st.error("❌ 不正解です。")
        
        st.info("""
        **解説**: 答えは②です。
        
        事業者があなたの許可なく宣伝メールを送ることは、基本的に禁止されています。
        うまい話には裏があると考え、安易に個人情報を渡さないようにしましょう。
        """)

st.markdown("---")

# まとめ
st.header("🎓 まとめ")
st.success("""
**個人情報保護のポイント**

1. **識別できる情報は個人情報**: 名前、生年月日、学校情報など
2. **写真には見えない情報が含まれる**: 位置情報、背景、服装など
3. **他人の許可を必ず取る**: 友達の写真を投稿する前に
4. **便利なサービスを活用**: 匿名配送などの安全な方法を選ぶ
5. **うまい話に注意**: 怪しいメールやサイトは避ける

あなたの個人情報という「カギ」を大切に管理して、安全なデジタルライフを送りましょう！
""")

# インタラクティブな理解度チェック
st.subheader("理解度チェック")
understanding = st.slider("今日の学習で、個人情報保護について理解できましたか？", 0, 100, 50, key="understanding")

if understanding >= 80:
    st.balloons()
    st.success(f"素晴らしい！{understanding}%の理解度です。個人情報保護マスターですね！🏆")
elif understanding >= 60:
    st.success(f"良い理解度です！{understanding}%。さらに意識を高めて実践してみてください。👍")
else:
    st.info(f"理解度{understanding}%。もう一度内容を見直してみてください。📚")