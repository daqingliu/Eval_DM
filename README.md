## Human Evaluation on DPO
1. Prepare two models, e.g., SDXL, SDXL_DPO
2. Create `random.json` using the last block of `dpo_compare.ipynb`
3. Run `python dpo_generate.py`, generate a batch of images according to `random.json`
4. Upload this repo to Git (thus each image own an openurl)
5. Run `genearte_json.py` to get `user_study_0115.json`
6. Run `analyse_dpo_result.ipynb` to get the final result!