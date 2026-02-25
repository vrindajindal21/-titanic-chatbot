from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import HuggingFacePipeline
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from data_loader import load_titanic_data, preprocess

df = preprocess(load_titanic_data())

# Create agent
def get_agent():
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512, temperature=0.1)
    llm = HuggingFacePipeline(pipeline=pipe)
    agent = create_pandas_dataframe_agent(llm, df, verbose=True)
    return agent
