import json
import openai  # You must `pip install openai` first

# 🔧 Configure OpenAI API
openai.api_key = "sk-..."  # replace with your key or call local LLM if needed

def read_prompt():
    with open("rule_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_llm(formula, prompt):
    full_prompt = f"""{prompt}

EXCEL FORMULA:
{formula}

Only return the final Stage 2 JSON rule output. No explanation.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        temperature=0
    )
    return response["choices"][0]["message"]["content"]

def main():
    formula = input("Enter Excel formula:\n").strip()
    prompt = read_prompt()

    print("\nGenerating JSON rule...\n")
    output = ask_llm(formula, prompt)

    try:
        json_rule = json.loads(output)
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(json_rule, f, indent=2)
        print("✅ JSON rule written to output.json")
    except json.JSONDecodeError:
        print("❌ Failed to parse LLM output as JSON.")
        print("Raw output:")
        print(output)

if __name__ == "__main__":
    main()
