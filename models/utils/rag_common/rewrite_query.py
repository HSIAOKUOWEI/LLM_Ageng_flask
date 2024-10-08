from ...model_list import get_model


def rewrite_prompt(question):
   prompt = f"""
角色：你是一個智能文本分析助手，專注於精確地解析問題並優化檢索效果。
任務：對用戶的原始問題進行解析並作出以下判斷：
1. 判斷原始問題是否包含多個子問題。如果是，請將所有子問題拆解為語義完整且獨立的問題，並按以下格式輸出（根據實際子問題數量自動編號）：
   1. 子問題一
   2. 子問題二
   ...
   n. 子問題n
2. 如果原始問題不包含多個子問題，請生成 {N} 個與原始問題語義相似但描述不同的問題，並按以下格式輸出：
   1. 替代問題一
   2. 替代問題二
   ...
   n. 替代問題n
要求：僅輸出生成的問題或子問題，所有問題或子問題必須按照1., 2., 3.的格式編號輸出，無需提供任何其他附加內容。
原始問題：{question}
"""
   return prompt

async def rewrite(llm=None, question):
        
   if not llm: 
      llm = get_model()
   
   prompt = rewrite_prompt(question=question)
   
   new_questions = await llm.ainvoke(prompt)

   return new_questions

