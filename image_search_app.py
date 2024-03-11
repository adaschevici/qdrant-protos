
from transformers import ViTImageProcessor, ViTModel
from qdrant_client import QdrantClient
import streamlit as st
import numpy as np
from PIL import Image
import torch

st.title("Skin Images Search Engine")
st.markdown("Upload images with different skin conditions and you'll get the most similar ones from our database of images.")

if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyTorch install was not "
              "built with MPS enabled.")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ "
              "and/or you do not have an MPS-enabled device on this machine.")

else:
    mps_device = torch.device("mps")

device = mps_device if locals().get("mps_device") else torch.device("cpu")
processor = ViTImageProcessor.from_pretrained("facebook/dino-vits16")
model = ViTModel.from_pretrained("facebook/dino-vits16").to(device)
client = QdrantClient("localhost", port=6333)

search_top_k = st.slider("How many search results do you want to retrieve?", 1, 40, 5)
image_file = st.file_uploader(label="📷 Skin Condition Image file 🔎")

if image_file:
    st.image(image_file)

    image = Image.open(image_file)
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state.mean(dim=1).cpu().numpy()
    st.markdown("## Semantic Search")
    results = client.search(collection_name=my_collection, query_vector=outputs[0], limit=search_top_k)

    for i in range(search_top_k):
        st.header(f"Disease: {results[i].payload['dx']}")
        st.header(f"Image ID: {results[i].payload['image_id']}")
        st.header(f"Location: {results[i].payload['localization']}")
        st.header(f"Gender: {results[i].payload['sex']}")
        st.header(f"Age: {results[i].payload['age']}")
