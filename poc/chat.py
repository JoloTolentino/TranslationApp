# ---------------------------------------------------------------#

#  The MarianMT model is a transformer model, built on top of
# *Seq2seq is a family of machine learning approaches used for natural language processing
# Different Seq2Seq models


# ---------------------------------------------------------------#

from transformers import MarianMTModel, MarianTokenizer
import pdb

# Example: English → French
src_lang = "en"
tgt_lang = "hi"
model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"

# Load tokenizer and model
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(
    model_name
)  # transformers.models.marian.modeling_marian.MarianMTModel

# Text to translate
text = "Hello, how are you?"

# Tokenize and translate

tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
translated = model.generate(**tokens)  # returns torch.tensor
translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
