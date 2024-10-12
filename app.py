import os
import streamlit as st
import google.generativeai as genai
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

# GitHub SecretsからAPIキーを取得
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# `GOOGLE_API_KEY`がNoneかどうかをチェック
if GOOGLE_API_KEY is None:
    st.error("GOOGLE_API_KEY is not set. Please check your GitHub Secrets and Streamlit Cloud settings.")
else:
    st.success("GOOGLE_API_KEY is successfully set!")

# ChatGoogleGenerativeAIを初期化
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, top_p=0.85)

def get_response(user_input):
    prompt = f"""
    このスレッドではしりとりをします。全ての質問に対しては以下のルールに厳格に従って答えてください。
    1. あなたは、「しりとりBOT」です。
    2. これは、漢字を使ったしりとりをおこなうゲームです。
    3. 高校生のレベルの日本語で答えてください。応答は漢字です。
    4. しりとりの単語は「」で括ってください。
    5. しりとりのルールは以下です。
      ・あなたは、ユーザーの単語を受けて、しりとりを行います。
      ・ユーザーの入力がひらがなの場合は、その単語のひらがなの最後の文字から始まる単語を選ぶ。
      ・ユーザーの入力がカタカナの場合は、その単語のカタカナの最後の文字から始まる単語を選ぶ。
      ・ユーザーの入力が漢字の場合は、その単語の最後の漢字から始まる単語を選ぶ。
      ・あなたの選んだ単語が漢字の場合は、読み仮名も付け加えてください。
      ・一度出た単語は使えない。
      ・最後の文字が「ん」で終わってはいけない。
      ・回答は10文字以内でおこなってください。
    6. 5のルール違反があった場合は違反をしたプレイヤーの負けとなります。「負けました」と表示してください。
    7．必ず回答してください。分からない場合は、「わかりません」と回答してください。
    ユーザー: {user_input}
    """
    response = llm.invoke(prompt)
    return response.content

# メインの処理
st.title("「漢字しりとり」ボット")
st.write("しりとりBot：私は「漢字しりとり」Botです！ しりとりをしましょう！ 単語を入れてください！ ※チャットを終了するには「終了」と入力してください。")
st.write("----------------------")

# チャット履歴をセッション状態で管理
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ユーザーの入力を取得
user_input = st.text_input("ユーザー：")

# 入力がある場合に処理を行う
if user_input:
    if user_input == "終了":
        st.write("チャットを終了します。")
    else:
        # チャット履歴に追加
        st.session_state.chat_history.append(f"ユーザー: {user_input}")

        # 入力を処理
        outa = llm.invoke(f"「{user_input}」の意味を高校生が分かるように簡単に説明してください。")
        st.write(outa.content)
        st.write("----------------------")
        st.write("")

        bot_response = get_response(user_input)
        st.session_state.chat_history.append(f"しりとりbot: {bot_response}")
        
        outb = llm.invoke(f"「{bot_response}」の意味を高校生が分かるように簡単に説明してください。")
        st.write(outb.content)
        st.write("----------------------")
        st.write("")

# チャット履歴を表示
for message in st.session_state.chat_history:
    st.write(message)
# ユーザーの入力を取得
#user_input = st.text_input("ユーザー：")

