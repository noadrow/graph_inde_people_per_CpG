import torch
from transformers import T5Tokenizer, T5Config, T5ForConditionalGeneration

# Define the model path
T5_PATH = 't5-base'  # Options: "t5-small", "t5-base", "t5-large", "t5-3b", "t5-11b"

# Set the device to CUDA if available, otherwise use CPU
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the T5 tokenizer, configuration, and model
t5_tokenizer = T5Tokenizer.from_pretrained(T5_PATH)
t5_config = T5Config.from_pretrained(T5_PATH)
t5_model = T5ForConditionalGeneration.from_pretrained(T5_PATH, config=t5_config).to(DEVICE)

# Input text that instructs the model to guess the output
text = """
prompt 1: what are you reacting to? "I'm reacting to": 
prompt 2: <extra_id_0>
prompt 3: <extra_id_1>
prompt 4: <extra_id_2>
prompt 5: <extra_id_3>
prompt 6: <extra_id_4>
reflect on it
</s>
"""


# Encode the input text
encoded = t5_tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
input_ids = encoded['input_ids'].to(DEVICE)

# Generate output sequences
outputs = t5_model.generate(input_ids=input_ids, num_beams=50, num_return_sequences=50, max_length=100)

# Identify where the <extra_id_0> token is in the original text
_0_index = text.index('<extra_id_0>')
_1_index = text.index('<extra_id_1>')
_2_index = text.index('<extra_id_2>')
_3_index = text.index('<extra_id_3>')
_4_index = text.index('<extra_id_4>')
_result_prefix = text[:_4_index]
_result_suffix = text[_0_index + 100:]  # 12 is the length of <extra_id_0>

def _filter(output):
    _txt = t5_tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return _result_prefix + _txt + _result_suffix

# Filter the outputs to create the final results
results = list(map(_filter, outputs))

# Display the results
for result in results:
    print(result)


# Initialize a memory list to store previous outputs
memory = []

# Encode the input text
encoded = t5_tokenizer.encode_plus(text, add_special_tokens=True, return_tensors='pt')
input_ids = encoded['input_ids'].to(DEVICE)

# Generate output sequences
outputs = t5_model.generate(input_ids=input_ids, num_beams=50, num_return_sequences=50, max_length=100)

# Identify where the <extra_id_0> token is in the original text
_0_index = text.index('<extra_id_0>')
_1_index = text.index('<extra_id_1>')
_2_index = text.index('<extra_id_2>')
_result_prefix = text[:_0_index]
_result_suffix = text[_0_index + 100:]  # 12 is the length of <extra_id_0>

def _filter(output):
    _txt = t5_tokenizer.decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return _result_prefix + _txt + _result_suffix

# Filter the outputs to create the final results
results = list(map(_filter, outputs))

# Update memory with the current result
memory.append(results)

# Display the results
for result in results:
    print(result)

# Example of how to include memory in the next round of input
if len(memory) > 0:
    previous_memory = ' '.join([' '.join(mem) for mem in memory])  # Concatenate all previous results
    new_text = f"{previous_memory} " + text  # Add memory to the beginning of the next input

