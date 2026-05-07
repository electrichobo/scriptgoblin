from typing import Type, TypeVar

from langchain_ollama import ChatOllama
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def parse_structured(llm: ChatOllama, schema: Type[T], messages: list) -> T:
    return llm.with_structured_output(schema).invoke(messages)
