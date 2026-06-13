#!/usr/bin/env python3
import sys
import argparse

# Define pricing per 1 Million tokens (in USD)
PRICING = {
    "deepseek-pro": {
        "input_no_cache": 0.14,
        "input_cache_hit": 0.014,
        "output": 0.28,
        "display_name": "DeepSeek V4 Pro"
    },
    "deepseek-flash": {
        "input_no_cache": 0.055,
        "input_cache_hit": 0.0055,
        "output": 0.219,
        "display_name": "DeepSeek V4 Flash"
    },
    "gpt-4o": {
        "input_no_cache": 5.00,
        "input_cache_hit": 2.50, # Supported via prompt caching (50% off)
        "output": 15.00,
        "display_name": "OpenAI GPT-4o"
    },
    "claude-3-5-sonnet": {
        "input_no_cache": 3.00,
        "input_cache_hit": 0.30, # Prompt caching (90% off write/read hit)
        "output": 15.00,
        "display_name": "Claude 3.5 Sonnet"
    }
}

def calculate_costs(prompt_tokens, completion_tokens, cache_hit_rate):
    results = {}
    for model_id, rates in PRICING.items():
        # Prompt calculation
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
    print("=" * 60)
    print("      🤖 AI Agent Cost & Savings Calculator (DeepSeek vs US Models) 🤖")
    print("=" * 60)
    
    parser = argparse.ArgumentParser(description="Calculate and compare AI API costs with caching.")
    parser.add_argument("-p", "--prompt", type=int, default=10_000_000, help="Prompt tokens (default: 10M)")
    parser.add_argument("-c", "--completion", type=int, default=2_000_000, help="Completion tokens (default: 2M)")
    parser.add_argument("-r", "--cache-rate", type=float, default=85.0, help="Cache hit rate percentage (default: 85%%)")
    
    args = parser.parse_args()
    
    prompt = args.prompt
    completion = args.completion
    rate = args.cache_rate
    
    print(f"📊 Inputs:")
    print(f"   • Prompt Tokens    : {prompt:,}")
    print(f"   • Completion Tokens: {completion:,}")
    print(f"   • Cache Hit Rate   : {rate}%")
    print("-" * 60)
    
    results = calculate_costs(prompt, completion, rate)
    
    # Print comparison
    print(f"{'Model Name':<20} | {'Prompt Cost':<12} | {'Output Cost':<12} | {'Total Cost':<12}")
    print("-" * 60)
    for model_id, rates in PRICING.items():
        res = results[model_id]
        name = rates["display_name"]
        print(f"{name:<20} | ${res['prompt_cost']:<11.2f} | ${res['completion_cost']:<11.2f} | ${res['total_cost']:<11.2f}")
        
    print("=" * 60)
    # Savings calculation compared to GPT-4o
    ds_pro_total = results["deepseek-pro"]["total_cost"]
    gpt_total = results["gpt-4o"]["total_cost"]
    savings = gpt_total - ds_pro_total
    percentage = (savings / gpt_total) * 100.0 if gpt_total > 0 else 0
    
    print(f"🔥 DeepSeek V4 Pro Savings vs GPT-4o:")
    print(f"   • Total Saved : ${savings:,.2f} USD")
    print(f"   • Cost cut by : {percentage:.2f}% cheaper!")
    print("=" * 60)

if __name__ == "__main__":
    main()
