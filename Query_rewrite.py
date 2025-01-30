from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from config import AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
import json
import logging

class QueryRewriter:
    """
    Uses Azure OpenAI (GPT-4) to dynamically generate variations of user queries.
    """

    def __init__(self):
        self.llm = AzureChatOpenAI(
            deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            temperature=0.5,
            max_tokens=256
        )

    def generate_variations(self, base_query):
        """
        Uses LLM to dynamically rewrite queries in different variations.
        """
        prompt = PromptTemplate(
            template=f"""
            Given the user query: "{base_query}"

            🔹 **Generate multiple phrasing styles:**
            1. **Original:** Keep the query unchanged.
            2. **Imperative:** Rewrite as a direct command.
            3. **Realistic:** Make it more conversational.
            4. **Metadata-aware:** Add explicit table joins and column names.

            Return the four variations in valid JSON format.
            """
        )
        response = self.llm.predict(prompt)

        try:
            query_variations = json.loads(response)
        except json.JSONDecodeError:
            logging.error(f"Query rewriter failed to parse response. Using fallback variations. Response: {response}")
            query_variations = {
                "Original": base_query,
                "Imperative": f"Show me the results for: {base_query}",
                "Realistic": f"Can you tell me {base_query}?",
                "Metadata": f"Join relevant tables and find: {base_query}"
            }

        return query_variations
