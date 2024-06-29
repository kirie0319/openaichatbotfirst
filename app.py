
import streamlit as st
import openai
import re

# ファイルを読み込み
with open('/Users/yuya0407/Desktop/Python/openaichatbot/[LINE] Chat with Minami Otsuki.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# データの抽出と前処理
cleaned_lines = []
for line in lines:
    # 日付や不要な部分を除去
    cleaned_line = re.sub(r'\d{2}:\d{2}[AP]M\s+\w+\s+.*\n', '', line)
    cleaned_lines.append(cleaned_line.strip())

# 前処理されたテキストデータ
cleaned_text = "\n".join(cleaned_lines)


# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは私の彼女です。"}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
