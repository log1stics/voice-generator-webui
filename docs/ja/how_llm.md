# LLM(ChatGPT等)と連携
LangChainによってLLMを制御しています。

日本語のプリセットを用いる場合、プリセット名は半角文字ではなく漢字、ひらがな、カタカナ等を用いることを推奨します。(これにより稀に英語で会話が生成される事象を防ぎます)

## APIキーを設定しない場合

ChatGPT GUI版の出力をそのままコピペするだけでも音声への変換が可能です

![](../images/chatgpt_gui.png)

ただしChatGPTの出力を正しく読み込むためにフォーマットを指定することに注意してください。
例えば、ミカ, カナ, ケンという名のプリセットを使用する際は以下のようにプロンプトを与えてください。

```
Human: 興味を惹く台本を日本語で書きなさい
The characters are as follows
ミカ, カナ, ケン

Please strictly adhere to the following format:
Character name: "Dialogue"
```

得られたChatGPTの出力をLLM Outputにコピペして、`Generate`を押下すれば音声が出力されます。(このときGenerate with LLMを選択しないように注意してください)

![](../images/llm_without_api.png)


## APIキーを設定する場合
SettingsでAPIキーを入力  
プリセットとプロンプトを入力  
`Generate with LLM`を押下
