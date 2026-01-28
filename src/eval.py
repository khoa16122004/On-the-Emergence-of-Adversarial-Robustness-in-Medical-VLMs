import os
import json
from tqdm import tqdm
import numpy as np
import random
attack_method = "NES"
attack_folder = "nes_attack"
mode_pretrained = "scratch"

# scratch: at
# ssl: scratch
# at: ssl

models = [
    # "medclip",
    #  "entrep",
    #   "biomedclip",
    'rmedclip'
      ]
datasets = [
    # "entrep",
     "rsna"
    ]
epsilons = [
    0.03,
    #  0.05,
    #   0.08,
    #    0.1
       ]
modes = ["pre_transform", "post_transform"]

# base_dir = r"D:\Gradient_based_ES_for_Attack_MedVLM\icml_full"
base_dir = r"C:\Users\ADMIN\Downloads\icml_result_sub"


def eval_attack(dir_path, idxs, attack_method):
    success = 0
    success_iter = 0
    l2 = 0



    for sample_id in idxs:
        info_path = os.path.join(dir_path, str(sample_id), 'info.json')
        history_path = os.path.join(dir_path, str(sample_id), 'history.txt')
        if not os.path.exists(info_path):
            continue

        # print(info_path)
        with open(info_path, "r") as f:
            data = json.load(f)

        if data['clean_pred'] != data['adv_pred'] and data['success_evaluation'] is not None and data['success_evaluation'] < 10001:
        # if data['clean_pred'] != data['adv_pred'] and data['success_evaluation'] is not None:
        # if data['clean_pred'] != data['adv_pred']:
        # if data['success_evaluation'] is not None and data['success_evaluation'] < 10001:

            success += 1

        l2 += data.get('l2', 0)
        # if data.get('l2', 0) == 0:
        #     raise

        if attack_method == "PGD":
            if os.path.exists(history_path):
                with open(history_path, "r") as f:
                    for line in f:
                        step, score = line.strip().split(',')
                        if float(score) < 0:
                            success_iter += int(step)
                            break
        else:
            if data['success_evaluation'] is None:
                success_iter += 10000
            else:
                success_iter += data['success_evaluation']
    
    n = len(idxs)
    print("Len: ", n)
    return {
        "ASR(%)": round(success * 100 / n, 3),
        "L2": round(l2 / n, 2),
        "Query": round(success_iter / n, 2)
    }

results = []

for model in models:
    for dataset in datasets:
        if model == "entrep":
            index_path = rf"evaluate_result\entrepclip_ssl_scratch_at.txt"
        elif model == "rmedclip":
            index_path = r"D:\Gradient_based_ES_for_Attack_MedVLM\evaluate_result\robustbiomedclip_ssl_scratch_at.txt"
        else:
            index_path = rf"evaluate_result\{model}_ssl_scratch_at.txt"



        if not os.path.exists(index_path):
            continue

        for mode in modes:
            for eps in epsilons:
                dir_path = rf"{base_dir}\{attack_folder}\{model}\{mode_pretrained}\{dataset}"
                for result_name in os.listdir(dir_path):
                    if mode not in result_name:
                        continue

                    result_dir = os.path.join(dir_path, result_name)
                    if not os.path.isdir(result_dir):
                        continue

                with open(index_path, 'r') as f:
                    idxs = [int(line.strip()) for line in f.readlines()]
                # print("Len: ", len(os.listdir(result_dir)))
                # idxs = [int(sample_id) for sample_id in os.listdir(result_dir)]

                # first_500 = idxs[:500]
                # last_500  = idxs[-500:]
                # sample_first = random.sample(first_500, 250)
                # sample_last  = random.sample(last_500, 250)
                # idxs = sample_first + sample_last
                

                # print(dir_path)



                metrics = eval_attack(result_dir, idxs, attack_method)

                results.append({
                    "model": model,
                    "dataset": dataset,
                    "mode": mode,
                    "eps": eps,
                    **metrics
                })

                print(
                    f"[{model:10s} | {dataset:6s} | {mode:14s} | eps={eps}] "
                    f"ASR={metrics['ASR(%)']}% | "
                    f"L2={metrics['L2']} | "
                    f"Query={metrics['Query']}"
                )
