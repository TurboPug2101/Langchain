# LangChain Configuration:

# A Groq language model (ChatGroq) is instantiated using the API key and model name gemma-7b-it.
# A prompt template is created, where the system prompt is to translate text into a specified language, and the user prompt is the text to be translated.
# A parser (StrOutputParser) is defined to handle the output of the model.
# Translation Chain:

# The chain is created by combining the prompt template, the Groq model, and the output parser. This chain will take an input (text and language), pass it through the model, and return the parsed output (the translation).
# FastAPI Server:

# A FastAPI application is created with metadata like title, version, and description.
# The LangChain chain is exposed as an API route via the add_routes function at the endpoint /chain.
# Running the Server:

# If the script is run directly, the FastAPI server will start on localhost:8000 using uvicorn

# The add_routes(app, chain, path="/chain") line connects the LangChain chain to the FastAPI app, making it accessible via an HTTP endpoint.
# The path="/chain" argument specifies the route where the chain will be exposed. This means any request made to localhost:8000/chain will trigger the LangChain translation chain.
# API Handling:

# When a request is made to /chain, the FastAPI app will take the input (likely JSON containing the text and target language), pass it through the LangChain translation chain, and return the translated output.
# The FastAPI app will handle request/response cycles, routing, and any potential errors.

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()


groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="gemma-7b-it",groq_api_key=groq_api_key)

## Prompt Template
system_template="Translate the following into {language}"
prompt_template=ChatPromptTemplate.from_messages(
    [
        ('system',system_template),
        ("user","{text}")
    ]
)

parser=StrOutputParser()

# create chain
chain= prompt_template|model|parser

# App defination
app=FastAPI(title="My Server ",
            version="1.0",
            description="Just an API server using Langchain runnable interfaces")

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)