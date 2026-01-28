## Installation

1. Clone the repository and move to the attack folder:
   ```
   cd path/to/repo/attack
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   (Note: Create a `requirements.txt` file with necessary packages like torch, torchvision, tqdm, numpy, PIL, pyyaml, pandas, etc.)
   
3. Download required datasets and place them in the `local_data` directory as specified in `modules/utils/constants.py`.

## Usage

### Running Attacks

Use the main script to perform adversarial attacks. Here's an example command for running a NES attack on the RSNA dataset with MedCLIP model:

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

### Available Options

- `--dataset_name`: Choose from 'rsna', 'covid', 'mimic', 'entrep'
- `--model_name`: Choose from 'medclip', 'biomedclip', 'entrep', 'ViT-B-32', 'ViT-B-16', 'ViT-L-14'
- `--attacker_name`: Specify the attack method (e.g., 'NES', 'ES_1_Lambda', 'PGD', 'CEM', 'ESGD', 'GridES_1_Lambda')
- `--epsilon` or `--eps`: Perturbation budget (default: 8/255)
- `--norm`: Norm for perturbation (e.g., 'linf', 'l2')
- `--max_evaluation`: Maximum number of evaluations for the attack
- `--q`: Query parameter for NES
- `--batch_q`: Batch query size
- `--alpha`: Step size for updates
- `--out_dir`: Output directory for results
- `--index_path`: Path to file with indices of samples to attack
- `--start_idx`: Starting index for processing
- `--end_idx`: Ending index for processing
- `--mode`: Mode for the attack (e.g., 'post_transform')
- `--mode_pretrained`: Pretraining mode (e.g., 'ssl' for self-supervised learning)

### Evaluating Results

Results are saved in the specified `out_dir` or `evaluate_result/` directory. Use the evaluation scripts to analyze attack performance.

## Datasets

- **RSNA**: Pneumonia detection dataset
- **COVID**: COVID-19 detection from chest X-rays
- **MIMIC**: Chest X-ray abnormality detection
- **Entrep**: Entrepreneurship-related dataset (adapted for medical use?)

## Models

- **MedCLIP**: Medical Vision-Language model
- **BioMedCLIP**: Biomedical CLIP model
- **Entrep**: Custom dual-encoder model
- **ViT Variants**: Vision Transformer models (B-16, B-32, L-14)

## Attacks

- **ES_1_Lambda**: Evolutionary Strategy attack
- **PGD**: Projected Gradient Descent
- **CEM**: Class Expectation over Max
- **ESGD**: Evolutionary Stochastic Gradient Descent
- **NES**: Natural Evolutionary Strategies
- **GridES_1_Lambda**: Grid-based Evolutionary Strategy

## Results

Evaluation results are stored in `evaluate_result/` with JSON and text files containing attack success rates, perturbation norms, and other metrics for different models and datasets.

## Project Structure

```
.
├── main_attack.py              # Main attack script
├── modules/
│   ├── attack/                 # Attack implementations
│   ├── dataset/                # Dataset loaders
│   ├── models/                 # Model definitions
│   └── utils/                  # Utilities and constants
├── evaluate_result/            # Evaluation outputs
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
