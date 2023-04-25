# LLM(ChatGPT等)と連携

![](../images/llm.png)

LangChainによってLLMを制御しています。

日本語のプリセットを用いる場合、プリセット名は半角文字ではなく漢字、ひらがな、カタカナ等を用いることを推奨します。(これにより稀に英語で会話が生成される事象を防ぎます)

## APIキーを設定しない場合

ChatGPT GUI版の出力をそのままコピペするだけでも音声への変換が可能です

![](../images/chatgpt_gui.png)

ただしChatGPTの出力を正しく読み込むためにフォーマットを指定することに注意してください。  
以下はミカ, カナ, ケンという名のプリセットを使用する際のプロンプトの一例です。

```
Human: 興味を惹く台本を日本語で書きなさい
The characters are as follows
ミカ, カナ, ケン

Please strictly adhere to the following format:
Character name: Dialogue
```

得られたChatGPTの出力をLLM Outputにコピペして、`Generate`を押下すれば音声が出力されます。(このときGenerate with LLMを選択しないように注意してください)

![](../images/llm_without_api.png)


## APIキーを設定する場合
1. SettingsでAPIキーを入力  
2. プリセットとプロンプトを入力  
3. `Generate with LLM`を押下

プロンプトは[llm/template.py](https://github.com/log1stics/voice-generator-webui/blob/main/llm/template.py)に代入されます。  
最終的なChatGPTへの入力プロンプトはコンソールに緑色で表示されます。

### 上級者、開発者向け
[llm/template.py](https://github.com/log1stics/voice-generator-webui/blob/main/llm/template.py)を編集することで最終的なChatGPTへの入力プロンプトの内容を変更できますが、  
フォーマット通りの出力を得られずテキストの読み込みに失敗する可能性があることに留意してください。

[llm/dialogue_agent.py](https://github.com/log1stics/voice-generator-webui/blob/main/llm/dialogue_agent.py)で読み込み方法を正規表現で制御できます。