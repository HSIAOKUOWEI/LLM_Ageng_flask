from collections import OrderedDict
import os
from dotenv import load_dotenv

env_path =r"D:\LLM_application\llm_flask\.env" #請改成自己env的路徑
load_dotenv(dotenv_path=env_path)

# 模型列表
MODEL_LIST_DETAILS = OrderedDict([
    ("Openai", OrderedDict([
        ("gpt-4o-mini", "gpt-4o-mini"),
        ("gpt-4o", "gpt-4o")
    ])),
    ("Google", OrderedDict([
        ("Gemini 1.5 Pro", "gemini-1.5-pro"),
        ("Gemini 1.5 Flash", "gemini-1.5-flash"),
        ("Gemini 1.0 Pro", "gemini-1.0-pro")
    ])),
    ("Groq", OrderedDict([
        ("LLaMA3 8b", "llama3-8b-8192"),
        ("LLaMA3.1 8b", "llama-3.1-8b-instant"),
        ("LLaMA3 70b", "llama3-70b-8192"),
        ("LLaMA3.1 70b", "llama-3.1-70b-versatile"),
        ("LLaMa3 Groq 8b Tool Use", "llama3-groq-8b-8192-tool-use-preview"),
        ("LLaMA3 Groq 70b Tool Use", "llama3-groq-70b-8192-tool-use-preview"),
        ("Mixtral 8x7b", "mixtral-8x7b-32768"),
        ("Gemma 7b", "gemma-7b-it"),
        ("Gemma2 9b", "gemma2-9b-it")
    ])),
    ("Siliconflow", OrderedDict([
    ("Qwen/Qwen2-7B-Instruct (32K)", "Qwen/Qwen2-7B-Instruct"),
    ("Qwen/Qwen2-1.5B-Instruct (32K)", "Qwen/Qwen2-1.5B-Instruct"),
    ("Qwen/Qwen1.5-7B-Chat (32K)", "Qwen/Qwen1.5-7B-Chat"),
    ("THUDM/glm-4-9b-chat (32K)", "THUDM/glm-4-9b-chat"),
    ("THUDM/chatglm3-6b (32K)", "THUDM/chatglm3-6b"),
    ("01-ai/Yi-1.5-9B-Chat-16K (16K)", "01-ai/Yi-1.5-9B-Chat-16K"),
    ("01-ai/Yi-1.5-6B-Chat (4K)", "01-ai/Yi-1.5-6B-Chat"),
    ("internlm/internlm2_5-7b-chat (32K)", "internlm/internlm2_5-7b-chat")
]))

])


def get_model(model_type="Openai", model_name=None, api_key=None, temperature=0.7):
    if model_type == "Openai":
        from langchain_openai import ChatOpenAI
        openai_llm = ChatOpenAI(api_key = api_key or os.getenv("OPENAI_API_KEY"), 
                                model = model_name or "gpt-4o-mini",
                                temperature = temperature)
        return openai_llm
    
    elif model_type == "Google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        google_llm = ChatGoogleGenerativeAI(api_key = api_key or os.getenv("GOOGLE_API_KEY"),
                                            model = model_name or "gemini-1.5-pro",
                                            temperature = temperature)
        return google_llm
    
    elif model_type == "Groq":
        from langchain_groq import ChatGroq
        groq_llm = ChatGroq(api_key = api_key or os.getenv("GROQ_API_KEY"),
                            model = model_name or "llama3-8b-8192",
                            temperature = temperature)
        return groq_llm
    
    elif model_type == "Siliconflow":
        from langchain_openai import ChatOpenAI
        siliconflow_base_url = "https://api.siliconflow.cn/v1"
        siliconflow_llm = ChatOpenAI(api_key = api_key or os.getenv("SILICONFLOW_API_KEY"), 
                                model = model_name or "Qwen/Qwen2-7B-Instruct",
                                temperature = temperature,
                                base_url = siliconflow_base_url)
        return siliconflow_llm
    

if __name__ == "__main__":
    import asyncio
    llm = get_model(api_key="")

    async def main():
        tasks = []
        for i in range(10):
            print(f"Scheduling task {i}")
            tasks.append(asyncio.to_thread(llm.invoke, "hello"))

        # 并发运行所有任务
        results = await asyncio.gather(*tasks)
        
        # 处理结果
        for i, result in enumerate(results):
            print(f"Result of task {i}: {result}")

    asyncio.run(main())