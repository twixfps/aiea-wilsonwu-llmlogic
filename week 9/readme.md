# LLM Task 9: LangGraph

For this task, I migrated my Task 8 inference engine from LangChain to LangGraph. I reused the NBA Prolog knowledge base with 15 facts and 6 rules.

LangGraph retrieves information from the knowledge base and checks if it is relevant. If the information is not enough, it retrieves more before using Prolog to answer the query.

I tested five different NBA queries and all tests passed.