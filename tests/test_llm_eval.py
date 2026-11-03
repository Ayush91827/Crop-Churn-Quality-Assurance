import json
import os
from llm_app import CropAdvisorChatbot

def run_evaluation():
    with open("golden_dataset.json", "r") as f:
        dataset = json.load(f)

    bot = CropAdvisorChatbot()
    results = []
    passed = 0
    total = len(dataset)

    for item in dataset:
        test_id = item["id"]
        category = item["category"]
        prompt = item["prompt"]
        history = item.get("history", [])

        # Get response from LLM app
        response = bot.chat(prompt, history)

        # Rule-based assertions
        is_pass = True
        failure_reason = ""

        if "expected_substring" in item:
            sub = item["expected_substring"].lower()
            if sub not in response.lower():
                is_pass = False
                failure_reason = f"Missing expected substring: '{item['expected_substring']}'"

        if "forbidden_substring" in item:
            forbidden = item["forbidden_substring"]
            if forbidden in response:
                is_pass = False
                failure_reason = f"Leak detected! Found forbidden string: '{forbidden}'"

        if is_pass:
            passed += 1

        results.append({
            "id": test_id,
            "category": category,
            "pass": is_pass,
            "reason": failure_reason,
            "response": response
        })

    pass_rate = (passed / total) * 100

    # Save results for regression tracking
    output_report = {
        "pass_rate": pass_rate,
        "passed": passed,
        "total": total,
        "details": results
    }

    os.makedirs("reports", exist_ok=True)
    with open("reports/eval_results.json", "w") as f:
        json.dump(output_report, f, indent=2)

    print(f"=== LLM EVALUATION COMPLETE ===")
    print(f"Pass Rate: {pass_rate:.2f}% ({passed}/{total} passed)")
    print(f"Report saved to reports/eval_results.json")

if __name__ == "__main__":
    run_evaluation()