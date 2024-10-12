import streamlit as st

import os
# Import the Python SDK
import google.generativeai as genai
# Used to securely store your API key
#from google.colab import userdata

#from langchain_google_genai import Genai  # `Genai`モジュールは適切にインポートしてください
import os
import streamlit as st

# GitHub SecretsからAPIキーを取得
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# `GOOGLE_API_KEY`がNoneかどうかをチェック
if GOOGLE_API_KEY is None:
    st.error("GOOGLE_API_KEY is not set. Please check your GitHub Secrets and Streamlit Cloud settings.")
else:
    st.success("GOOGLE_API_KEY is successfully set!")


from langchain_google_genai import ChatGoogleGenerativeAI
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, top_p=0.85)
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, top_p=0.85)

prompt = f"""
    このスレッドではしりとりをします。全ての質問に対しては以下のルールに厳格に従って答えてください。
    1. あなたは、「しりとりBOT」です。
    2. これは、漢字を使ったしりとりをおこなうゲームです。
    3. 高校生のレベルの日本語で答えてください。応答は漢字です。
    4. しりとりの単語は「」で括ってください。
    5. しりとりのルールは以下です。
    　・あなたは、ユーザーの単語を受けて、しりとりを行います。
      ・ユーザーの入力がひらがなの場合は、その単語のひらがなの最後の文字から始まる単語を選ぶ。例えば、ユーザーが「りんご」であれば、最後の文字が「ご」なので、「ごま」と答える。
      ・ユーザーの入力がカタカナの場合は、その単語のカタカナの最後の文字から始まる単語を選ぶ。例えば、ユーザーが「メガネ」であれば、最後の文字が「ネ」なので、「ネコ」と答える。
      ・ユーザーの入力が漢字の場合は、その単語の最後の漢字から始まる単語を選ぶ。例えば、「仮説」であれば、最後の漢字が「説」なので、「設計（せっけい）」と答える。
      ・あなたの選んだ単語が漢字の場合は、読み仮名も付け加えてください。例えば、「仮説（かせつ）」と答える
      ・一度出た単語は使えない。
      ・最後の文字が「ん」で終わってはいけない。
      ・回答は10文字以内でおこなってください。
    6. 5のルール違反があった場合は違反をしたプレイヤーの負けとなります。「負けました」と表示してください。
    7．必ず回答してください。分からない場合は、「わかりません」と回答してください。
    """


# ChatGPTのシステムに渡して
messages = [
    {"role": "system",
     "content": system_prompt}
]


def get_response(user_input):

    user_message = {"role": "user", "content": user_input}
    global messages
    messages.append(user_message)

    # Use the `invoke` method with the entire message history
    response = llm.invoke(messages)

    return response.content

# メインの処理
st.title("「漢字しりとり」ボット")
#user_input = st.text_input("あなたの今の感情を表現してください")
st.write("しりとりBot：私は「漢字しりとり」Botです！　しりとりをしましょう！　単語を入れてください！　※チャットを終了するには「終了」と入力してください。")
st.write("----------------------")


# 入力履歴を保存するためのリストを初期化
chat_history = []

# ユーザーの入力を取得
#user_input = st.text_input("ユーザー：")

# 入力がある場合に処理を行う
while True:
    user_input = st.text_input("ユーザー：")
    if user_input:
        if user_input == "終了":
            st.write("チャットを終了します。")
        else:
            chat_history.append(f"ユーザー: {user_input}")
            st.write(f"ユーザー: {user_input}")
            outa = llm.invoke(f"「{user_input}」の意味を高校生が分かるように簡単に説明してください。")
            st.write(outa.content)
            st.write("----------------------")
            st.write("")
            
            bot_response = get_response(user_input)
            st.write(f"しりとりbot: {bot_response}")
            outb = llm.invoke(f"「{bot_response}」の意味を高校生が分かるように簡単に説明してください。")
            st.write(outb.content)
            st.write("----------------------")
            st.write("")

# チャット履歴を表示
#for message in chat_history:
#    st.write(message)


