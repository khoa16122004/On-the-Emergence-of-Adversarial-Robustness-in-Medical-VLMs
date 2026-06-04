# On the Emergence of Adversarial Robustness in Medical VLMs

This project explores the robustness of Vision Language Models (VLMs) in the medical domain when facing adversarial attacks. The workflow includes SSL finetuning of medical VLMs, denoised smoothing implementation, and comprehensive adversarial attack experiments.

The our pretrained medical VLMs are available at the following link: [Hugging-face](https://huggingface.co/Woffy/Medical_VLMs_SSL_CL)

---

## 📁 Project Structure Overview

The project follows a two-stage workflow:

1. **Stage 1: Finetuning VLMs with SSL** - Train and prepare robust models
2. **Stage 2: Adversarial Attacks** - Evaluate robustness against adversarial examples

---

## 1. SSL Finetuning for VLMs

### Overview

This stage includes training Vision Language Models with Self-Supervised Learning (SSL) and Adversarial Training (AT) variants. The notebooks provide integrated scripts that automatically import necessary libraries.

### Key Components

#### **src/SSL_CTL.ipynb** - Main Training Script

This notebook contains the primary script for finetuning three medical VLMs:

**Supported Models:**
- **MedCLIP** - Medical-domain CLIP model
- **BioMedCLIP** - Biomedical-focused CLIP variant
- **ENTRepCLIP** - Entropy-based medical CLIP

**Training Modes:**
- `SSL` - Self-Supervised Learning finetuning
- `AT` - Adversarial Training finetuning

**Features:**
- Auto-imports all required libraries and dependencies
- Integrated dataset loading and preprocessing
- Model training with configurable hyperparameters
- Automatic checkpoint saving
- Validation during training

**Usage:**
```bash
# Open and run the notebook
jupyter notebook src/SSL_CTL.ipynb
```

The notebook guides you through:
1. Loading and preparing datasets
2. Initializing models (SSL or AT variants)
3. Configuring training parameters
4. Running the training process
5. Saving trained models

#### **src/DS_CTL.ipynb** - Denoised Smoothing

This notebook contains the re-implemented script for Denoised Smoothing (DS) certification with VLMs.

**Features:**
- Implements certified robustness evaluation
- Uses pre-trained or finetuned VLM models
- Evaluates smoothed predictions under perturbations
- Generates robustness certificates

**Usage:**
```bash
# Open and run the notebook
jupyter notebook src/DS_CTL.ipynb
```

The notebook includes:
1. Loading trained VLM models
2. Configuring smoothing parameters
3. Running denoised smoothing evaluation
4. Analyzing robustness certificates

### Training Workflow

1. **Start with SSL_CTL.ipynb**
   - Choose your target model (MedCLIP, BioMedCLIP, or ENTRepCLIP)
   - Select training mode (SSL or AT)
   - Run the training process
   - Save the trained model

2. **Run DS_CTL.ipynb** (optional)
   - Load the trained model from Step 1
   - Apply denoised smoothing certification
   - Evaluate robustness certificates

3. **Proceed to Stage 2** (Attack experiments)
   - Use trained models from Stage 1
   - Execute attack scripts to evaluate adversarial robustness

---

## 2. Adversarial Attack Experiments


### Key Files

- **main_attack.py** - Main script to perform attacks
- **eval.py** - Evaluate attack results
- **test_clean_performance.py** - Test performance on original data
- **transfer_attack.py** - Transfer attacks between models
- **ds_test.py** - Test denoised smoothing robustness

### Models Tested

- **MedCLIP** - Medical CLIP variant
- **BioMedCLIP** - Biomedical CLIP model
- **ENTRepCLIP** - Entropy-based medical CLIP
- **ViT-B-16, ViT-B-32, ViT-L-14** - Vision Transformer variants
- **RobustMedCLIP** - Adversarially trained MedCLIP

### Running Attacks

Use the main script to perform adversarial attacks. Example command for NES attack on RSNA dataset with MedCLIP:

```bash
python main_attack.py \
    --dataset_name rsna \
    --model_name medclip \
    --attacker_name NES \
    --epsilon 0.03 \
    --norm linf \
    --max_evaluation 10000 \
    --q 100 \
    --batch_q 100 \
    --alpha 0.01 \
    --out_dir attack_results/nes_attack \
    --start_idx 0 \
    --index_path "evaluate_result/medclip_ssl_scratch.txt" \
    --mode post_transform \
    --mode_pretrained ssl
```

### Available Attack Options

**Datasets:**
- `rsna` - Pneumonia detection dataset
- `covid` - COVID-19 detection from chest X-rays
- `mimic` - Chest X-ray abnormality detection
- `entrep` - Medical dataset variant

**Attack Methods:**
- `NES` - Natural Evolutionary Strategies
- `ES_1_Lambda` - Evolutionary Strategy attack
- `PGD` - Projected Gradient Descent
- `CEM` - Class Expectation over Max
- `ESGD` - Evolutionary Stochastic Gradient Descent
- `GridES_1_Lambda` - Grid-based Evolutionary Strategy

**Key Parameters:**
- `--epsilon` / `--eps`: Perturbation budget (default: 8/255)
- `--norm`: Norm for perturbation (`linf`, `l2`)
- `--max_evaluation`: Maximum evaluations for the attack
- `--q`: Query parameter for NES
- `--batch_q`: Batch query size
- `--alpha`: Step size for updates
- `--out_dir`: Output directory for results
- `--index_path`: Path to indices of samples to attack
- `--start_idx`: Starting index for processing
- `--end_idx`: Ending index for processing
- `--mode`: Attack mode (e.g., `post_transform`)
- `--mode_pretrained`: Pretraining mode (`ssl`, `at`, etc.)

### Evaluating Results

Results are saved in the specified `out_dir` or `evaluate_result/` directory. Results include:
- Attack success rates
- Perturbation norms
- Query efficiency metrics
- Per-sample analysis

See `evaluate_result/` folder for example results from different models and datasets.

### Project Structure (attack folder)

```
attack/
├── main_attack.py              # Main attack script
├── eval.py                     # Evaluation script
├── test_clean_performance.py   # Test clean performance
├── transfer_attack.py          # Transfer attack script
├── ds_test.py                  # Denoised smoothing test
├── modules/
│   ├── attack/                 # Attack implementations
│   │   ├── attack.py
│   │   ├── evaluator.py
│   │   └── util.py
│   ├── dataset/                # Dataset loaders
│   │   ├── base.py
│   │   ├── covid.py
│   │   ├── entrep.py
│   │   ├── mimic.py
│   │   ├── rsna.py
│   │   └── factory.py
│   ├── models/                 # Model definitions
│   │   ├── base.py
│   │   ├── biomedclip.py
│   │   ├── entrep.py
│   │   ├── medclip.py
│   │   ├── robustmedclip.py
│   │   ├── vit.py
│   │   ├── vision_model.py
│   │   ├── factory.py
│   │   └── RobustMedCLIP/
│   └── utils/                  # Utilities
│       ├── constants.py
│       ├── helpers.py
│       └── logging_config.py
├── evaluate_result/            # Evaluation results
└── README.md                   # Detailed attack instructions
```

---

## 📋 System Requirements
- A H100 80GB - GPU
- Python 3.8+
- PyTorch 1.10+
- CUDA 11.0+ (if using GPU)
- Jupyter Notebook (for running .ipynb files)
- See `requirements.txt` in each folder for detailed dependencies

---
