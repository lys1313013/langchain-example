import os
from datasets import load_dataset
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 数据集列表
datasets_map = {
    "DuRetrieval": "C-MTEB/DuRetrieval",
    "T2Retrieval": "C-MTEB/T2Retrieval",
    "MMarcoRetrieval": "C-MTEB/MMarcoRetrieval"
}

output_base_dir = os.path.abspath("data")
os.makedirs(output_base_dir, exist_ok=True)


def download_and_save(dataset_name, repo_id):
    logger.info(f"==================================================")
    logger.info(f"Processing {dataset_name} ({repo_id})...")
    save_path = os.path.join(output_base_dir, dataset_name)

    try:
        # 尝试加载主数据集
        logger.info(f"Downloading main dataset: {repo_id}")
        # 有些数据集可能比较大，这里不指定 split 以下载所有 splits
        ds = load_dataset(repo_id, trust_remote_code=True)

        logger.info(f"Dataset structure for {dataset_name}: {ds}")

        ds.save_to_disk(save_path)
        logger.info(f"Successfully saved {dataset_name} to {save_path}")

        # 尝试加载 qrels
        qrels_repo_id = f"{repo_id}-qrels"
        try:
            logger.info(f"Attempting to download qrels from: {qrels_repo_id}")
            ds_qrels = load_dataset(qrels_repo_id, trust_remote_code=True)

            logger.info(f"Qrels structure for {dataset_name}: {ds_qrels}")

            qrels_save_path = os.path.join(output_base_dir, f"{dataset_name}-qrels")
            ds_qrels.save_to_disk(qrels_save_path)
            logger.info(f"Successfully saved {dataset_name} qrels to {qrels_save_path}")
        except Exception as e:
            logger.warning(
                f"Note: Separate qrels dataset {qrels_repo_id} not found or failed to load. This is normal if qrels are inside the main dataset. Error: {str(e)[:100]}...")

    except Exception as e:
        logger.error(f"Failed to download {dataset_name}: {e}")


if __name__ == "__main__":
    logger.info(f"Starting download to {output_base_dir}")
    for name, repo_id in datasets_map.items():
        download_and_save(name, repo_id)
    logger.info("All tasks completed.")
