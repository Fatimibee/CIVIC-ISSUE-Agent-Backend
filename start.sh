python -c "from transformers import CLIPModel; CLIPModel.from_pretrained('openai/clip-vit-base-patch32')"
uvicorn App.app:app --host 0.0.0.0 --port $PORT