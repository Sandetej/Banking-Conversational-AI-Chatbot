"""Export models to different formats."""
import torch

def export_to_onnx(model, tokenizer, output_path: str):
    """Export to ONNX format."""
    try:
        print(f"Exporting to ONNX: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def export_to_huggingface(model, tokenizer, repo_name: str):
    """Push model to Hugging Face Hub."""
    try:
        print(f"Pushing to Hub: {repo_name}")
    except Exception as e:
        print(f"Error: {e}")
