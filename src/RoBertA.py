import joblib
import pandas as pd
import torch
import torch.nn as nn
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import numpy as np
import os

def classify(text):
    # path to model binary files 
    script_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.join(script_directory, ".."))
    binary_files_path = os.path.join(parent_directory, "binary_files")

    # Load the model and tokenizer using the constructed path
    model = RobertaForSequenceClassification.from_pretrained(binary_files_path)
    tokenizer = RobertaTokenizer.from_pretrained(binary_files_path)

    # tokinize text
    inputs = tokenizer(text, return_tensors="pt")

    #predict 
    outputs = model(**inputs)
    predictions = []

    with torch.no_grad():
        logits = outputs.logits
        pred = torch.softmax(logits, dim=1)
        predicted_onehot = torch.zeros_like(pred)
        predicted_onehot.scatter_(1, torch.argmax(pred, dim=1).unsqueeze(1), 1)
        
    # import encoder/decoder and decode predictions
    encoder_path = os.path.join(parent_directory, "binary_files/onehot_encoder.joblib")
    encoder = joblib.load(encoder_path)
    result = encoder.inverse_transform(predicted_onehot)

    return result[0][0]