# # Load Packages
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model

# # Layout set up
st.set_page_config (layout="wide")

# # Input set up
# Set the length of the sequences for training
Tx = 40

chars = ['\n', ' ', '#', '$', '%', '&', "'", '(', ')', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?', '[', ']', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\xa0', 'ω', '‐', '–', '—', '‘', '’', '“', '”', '•', '…', '⎯', '\uf0b7', '\uf0be', '\uf8e7']

# Create a dictionary that maps each character to its index in the 'chars' list
char_indices = dict((c, i) for i, c in enumerate(chars))

# Create a dictionary that maps each index to its corresponding character in the 'chars' list
indices_char = dict((i, c) for i, c in enumerate(chars))

# Set up the title and input
st.title("Actuarial Standards of Practice (ASOP) Dreaming Model")
st.header("Imagine a world where AI dreams Actuarial Standards of Practice")

link = "https://github.com/DanTCIM/ASOP_RNN"
st.markdown(f"The model is trained using recurrent neural network. The Python code and the documentation of the project in [GitHub]({link}).")

st.markdown("Write the beginning of your ASOP, the ASOP Dreaming Model will complete it. Your input is: ")
usr_input = st.text_input("")

# # Model and Function set up
# Load the model
@st.cache_resource 
def load_keras_model(model_path):
    """Load and return the Keras model from the given path."""
    model = load_model(model_path)
    return model

# Model and Function setup
#model_path = '/Users/dan153/LLM/ASOP_RNN/model/Life_ASOP_rnn_model021.keras'
model_path = 'model/Life_ASOP_rnn_model021.keras'
model = load_keras_model(model_path)
#model = load_model('/Users/dan153/LLM/ASOP_RNN/model/Life_ASOP_rnn_model021.keras')

def sample(preds, temperature=1.0):
    """
    Helper function to sample an index from a probability array.

    Arguments:
    preds (list): The input probability array.
    temperature (float): Controls the randomness of the sampling. Higher values make the sampling more random.

    Returns:
    int: The sampled index.
    """
    
    preds = np.asarray(preds).astype('float64')

    # Apply logarithm to the probability array (temperature being zero will get an error)
    preds = np.log(preds) / max(temperature, 0.000001)
    exp_preds = np.exp(preds)

    # Apply softmax to normalize the array
    preds = exp_preds / np.sum(exp_preds) 

    # Use the softmax probabilities to perform multinomial sampling
    probas = np.random.multinomial(1, preds, 1)

    # Get the sampled index using the probabilities
    out = np.random.choice(range(len(chars)), p = probas.ravel())
    return out

def generate_output(temperature = 1.0, ASOP_length = 500):
    """
    Generates an ASOP based on user input.
    
    Arguments:
    - temperature (float): Controls the randomness of the generated output. Higher values result in more randomness.
    - ASOP_length (int): The desired length of the generated ASOP in characters.
    
    Returns:
    - generated (str): The generated ASOP string.
    """
    
    generated = '' # Initializes an empty string

    sentence = ('{0:0>' + str(Tx) + '}').format(usr_input).lower() # Zero pad the input sentence to make length Tx
    generated += usr_input 

    st.write("\n\nHere is your ASOP: \n\n") 
    # Placeholder for continuous output
    output_placeholder = st.empty()
    
    for i in range(ASOP_length):
        x_pred = np.zeros((1, Tx, len(chars))) # Initialize NumPy array with zeros. len(chars) = 69

        for t, char in enumerate(sentence): # Iterates over each character in the current sentence
            if char != '0':
                x_pred[0, t, char_indices[char]] = 1. # One-hot coding the sentence

        preds = model.predict(x_pred, verbose=0)[0] # Get next character's probability distribution (softmax)
        next_index = sample(preds, temperature = temperature) # Sample an index from the distribution out of len(chars)
        next_char = indices_char[next_index] # Convert index to character

        generated += next_char
                
        # Updates the sentence by removing its first character 
        # and appending the newly generated character, maintaining a fixed length of Tx.        
        sentence = sentence[1:] + next_char 

        # Update the output text dynamically
        output_placeholder.text(generated)
        
# # Model and Function set up
# Let's generate ASOP!
if st.button('Generate ASOP'):
    generate_output(temperature=1.0, ASOP_length=600)
