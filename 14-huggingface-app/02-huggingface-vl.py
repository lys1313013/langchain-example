from datasets import get_dataset_config_names, load_dataset, tqdm

# 一、检查数据集可用的 Configs
repo_id = "ziyjiang/MMEB_Test_Instruct"
NAME = "Wiki-SS-NQ"
try:
    configs = get_dataset_config_names(repo_id)
    print(f"可用的Configs: {configs}")
except Exception as e:
    print(f"无法获取Configs，可能需要直接加载: {e}")

ds = load_dataset(repo_id, name=NAME, split="test")
df = ds.to_pandas()
tgt_img_paths = []
for _, row in tqdm(df.iterrows(), total=len(df)):
     tgt_img_paths.append(row['tgt_img_path'][0])

print(len(ds))