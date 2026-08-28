# LLM Task 8 - LangChain Using Logical Inference Engine

## Description

LangChain Project integrated with a Prolog logical inference engine.

## Knowledge Base

NBA Teams, Conferences, Championships, Rules for determining if team has certain properties (ex. historically successful team).

## LangChain + RAG

LangChain grabs relevant facts/rules stored in NBA knowledge base based on query.

## Logical Inference

Prolog attempts to determine True/False answer based on the query. Prints inference trace of facts, rule, and comparison used to determine result.

## Run

```bash
python langchain_logic.py