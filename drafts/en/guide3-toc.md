# 📦 MacBook Local AI Mastery Guide (Table of Contents)

**Author**: Ted Chang (임창식)  
**Publisher/Planning**: META AI LABS  

---

## Table of Contents

### Chapter 1: Why Local AI?

- Cloud API Problems (Cost, Privacy, Speed)
- Advantages of Local AI: Free, Offline, Unlimited
- Why Apple Silicon (M-Series) Is Special
- Goal of This Guide: Complete AI Assistant with One MacBook

### Chapter 2: First Steps with LM Studio

- Installing LM Studio (Official Site)
- Downloading Your First Model (Qwen 3.5, Gemma 4)
- Running Models and Testing Chat
- Checking Speed: What tok/s Means and Normal Ranges
- Recognizing Limitations: LM Studio's Problems

### Chapter 3: Upgrading to Jan.ai

- Why You Should Migrate from LM Studio to Jan.ai
- Installing Jan.ai and Basic Setup
- Understanding the GGUF Model Folder Structure
  ```bash
  ~/Library/Application Support/Jan/data/llamacpp/models/
  └── <model_name>/
      ├── model.gguf
      ├── mmproj.gguf (optional)
      └── model.yml
  ```
- Complete model.yml Configuration Guide
  - batch_size, ctx_size, n_gpu_layers
- Downloading Models with HuggingFace CLI

### Chapter 4: MLX — Apple Native Optimization

- What Is the MLX Framework? (Apple's Metal Performance Shaders)
- GGUF vs MLX: When to Use Which?
- Installing and Running MLX Models
- vLLM (Mac) vs MLX Comparison
- Real Speed Comparison Chart

### Chapter 5: GGUF Quantization Complete Guide

- What Is Quantization?
- Q2_K, Q3_K, Q4_K, Q5_K, Q6_K, Q8_0 Differences
  - Small Models (Qwen 3B etc.): Recommend Q8_0
  - Medium Models (Gemma 4 12B etc.): Recommend Q4_K_M
  - Large Models (Qwen 35B etc.): Q3_K or Q2_K
- Memory vs Quality Trade-off Table

### Chapter 6: APEX Quantization — Secrets of MoE Models

- Understanding MoE (Mixture of Experts) Architecture
  - Qwen3.6-35B-A3B = Only 3B of 35B Parameters Activated
  - Dense vs MoE Speed Comparison
- What Is APEX (Adaptive Precision for Expert Models)?
- APEX Profile Selection Guide
  - I-Compact (17GB) ⭐ Recommended
  - I-Mini (14GB)
  - I-Balanced (24GB)
  - I-Quality (22GB)

### Chapter 7: Uncensored / Abliterated Model Selection

- Political Censorship Issues with Chinese Models
- The Abliterated (diff-in-means) Method
- Recommended Repositories
  - OpenYourMind
  - mudler APEX GGUF
- Installation and Verification

### Chapter 8: Hermes Agent + Local Model Integration

- Connecting Local Models to Hermes Agent
  ```bash
  hermes config set model.base_url http://localhost:1337/v1
  ```
- Cloud + Local Hybrid Strategy
  - Daily Tasks: DeepSeek V4 Flash (Cloud)
  - Sensitive Tasks: Local Model
  - Image Analysis: Mimo 2.5 (Cloud)
- Automating Model Switching with Profiles

### Chapter 9: A Day in the Life of the Master

- Morning: Email/Report Checks with DeepSeek Flash
- Afternoon: Hermes Agent + AG Collaboration (Cloud)
- Evening: Testing with Jan.ai Local Models
- Night: Cron Job Auto-Execution
- Monthly Cost Report

### Appendix

- A. Recommended Model Specifications Table
- B. Troubleshooting (FAQ)
- C. Useful Command Collection

---

**Estimated Length:** Lite: ~50 pages / Pro: ~80 pages + Configuration File Package
**Estimated Price:** Lite $9.90 / Pro $24.90 (Same as Guide 1)
