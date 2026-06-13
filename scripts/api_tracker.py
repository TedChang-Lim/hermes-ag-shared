#!/usr/bin/env python3
import sys
import argparse

# Define pricing per 1 Million tokens (in USD)
# Source: DeepSeek official pricing (2026-05-31 permanent 75% discount applied)
PRICING = {
    "deepseek-pro": {
        "input_no_cache": 0.435,
        "input_cache_hit": 0.0435,
        "output": 0.87,
        "display_name": "DeepSeek V4 Pro"
    },
    "deepseek-flash": {
        "input_no_cache": 0.14,
        "input_cache_hit": 0.014,
        "output": 0.28,
        "display_name": "DeepSeek V4 Flash"
    },
    "mimo-2.5": {
        "input_no_cache": 0.14,
        "input_cache_hit": 0.014,
        "output": 0.28,
        "display_name": "Mimo 2.5"
    },
    "gpt-4o": {
        "input_no_cache": 5.00,
        "input_cache_hit": 2.50,  # Prompt caching (50% off)
        "output": 15.00,
        "display_name": "OpenAI GPT-4o"
    },
    "claude-3-5-sonnet": {
        "input_no_cache": 3.00,
        "input_cache_hit": 0.30,  # Prompt caching (90% off)
        "output": 15.00,
        "display_name": "Claude 3.5 Sonnet"
    }
}

def calculate_costs(prompt_tokens, completion_tokens, cache_hit_rate):
    results = {}
    for model_id, rates in PRICING.items():
        hit_tokens = prompt_tokens * (cache_hit_rate / 100.0)
        miss_tokens = prompt_tokens * (1.0 - cache_hit_rate / 100.0)
        
        prompt_cost = (hit_tokens * rates["input_cache_hit"] + miss_tokens * rates["input_no_cache"]) / 1_000_000.0
        completion_cost = (completion_tokens * rates["output"]) / 1_000_000.0
        total_cost = prompt_cost + completion_cost
        
        results[model_id] = {
            "prompt_cost": prompt_cost,
            "completion_cost": completion_cost,
            "total_cost": total_cost
        }
    return results

def main():
    print("=" * 62)
    print("      🤖 Ultra-Low-Cost AI Agent Cost Calculator 🤖")
    print("=" * 62)
    
    parser = argparse.ArgumentParser(description="Calculate and compare AI API costs with caching.")
    parser.add_argument("-p", "--prompt", type=int, default=10_000_000, help="Prompt tokens (default: 10M)")
    parser.add_argument("-c", "--completion", type=int, default=2_000_000, help="Completion tokens (default: 2M)")
    parser.add_argument("-r", "--cache-rate", type=float, default=85.0, help="Cache hit rate %% (default: 85%%")
    
    args = parser.parse_args()
    
    prompt = args.prompt
    completion = args.completion
    rate = args.cache_rate
    
    print(f"📊 Inputs:")
    print(f"   • Prompt Tokens    : {prompt:,}")
    print(f"   • Completion Tokens: {completion:,}")
    print(f"   • Cache Hit Rate   : {rate}%")
    print("-" * 62)
    
    results = calculate_costs(prompt, completion, rate)
    
    print(f"{'Model Name':<22} | {'Prompt Cost':<12} | {'Output Cost':<12} | {'Total Cost':<12}")
    print("-" * 62)
    for model_id, rates in PRICING.items():
        res = results[model_id]
        name = rates["display_name"]
        print(f"{name:<22} | ${res['prompt_cost']:<11.4f} | ${res['completion_cost']:<11.4f} | ${res['total_cost']:<11.4f}")
    
    print("=" * 62)
    
    # Savings: DeepSeek V4 Flash vs GPT-4o
    ds_flash_total = results["deepseek-flash"]["total_cost"]
    gpt_total = results["gpt-4o"]["total_cost"]
    savings = gpt_total - ds_flash_total
    percentage = (savings / gpt_total) * 100.0 if gpt_total > 0 else 0
    
    print(f"🔥 DeepSeek V4 Flash vs GPT-4o:")
    print(f"   • GPT-4o cost    : ${gpt_total:,.4f}")
    print(f"   • DS Flash cost  : ${ds_flash_total:,.4f}")
    print(f"   • You save       : ${savings:,.4f} ({percentage:.2f}% cheaper!)")
    print("=" * 62)
    
    # Daily/monthly estimates
    ds_daily = ds_flash_total
    ds_monthly = ds_daily * 30
    gpt_daily = gpt_total
    gpt_monthly = gpt_daily * 30
    yearly_savings = (gpt_monthly - ds_monthly) * 12
    
    print(f"📅 Monthly & Yearly Comparison (at this usage level):")
    print(f"   • DeepSeek Flash: ${ds_monthly:.2f}/month")
    print(f"   • GPT-4o        : ${gpt_monthly:.2f}/month")
    print(f"   • Yearly savings: ${yearly_savings:.2f}")
    print("=" * 62)

if __name__ == "__main__":
    main()
