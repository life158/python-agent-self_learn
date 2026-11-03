import os
from dotenv import load_dotenv
load_dotenv()
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
MODEL_ID=os.getenv("MODEL_ID")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")

def validate_model_settings(model_api_key:str,model_base_url:str,model_id:str):
    missing = []
    if not isinstance(model_api_key, str) or not model_api_key.strip():
            missing.append("MODEL_API_KEY")
    if not isinstance(model_base_url, str) or not model_base_url.strip():
            missing.append("MODEL_BASE_URL")
    if not isinstance(model_id, str) or not model_id.strip():
            missing.append("MODEL_ID")
    if missing:
        raise ValueError(
            f"Missing settings: {', '.join(missing)}")
def validate_embedding_settings(model_api_key:str,model_base_url:str,embedding_model_id:str):
    missing = []
    if not isinstance(model_api_key, str) or not model_api_key.strip():
        missing.append("EMBEDDING_API_KEY")
    if not isinstance(model_base_url, str) or not model_base_url.strip():
        missing.append("EMBEDDING_BASE_URL")
    if not isinstance(embedding_model_id, str) or not embedding_model_id.strip():
        missing.append("EMBEDDING_MODEL_ID")
    if missing:
        raise ValueError(
            f"Missing settings: {', '.join(missing)}")
