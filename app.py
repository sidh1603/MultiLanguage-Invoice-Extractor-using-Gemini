import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = api_key)

##model

model = genai.GenerativeModel("gemini-1.5-pro")

def get_response(input,image,prompt):
    response = model.generate_content([input,image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
        if uploaded_file is not None:
             bytes_data = uploaded_file.getvalue()
             images_part = [
                  {
                       "mime_type":uploaded_file.type,
                       "data":bytes_data}
             ]
             return images_part
        else:
             raise FileNotFoundError("No File Uploaded")



st.set_page_config(page_title="Multilanguage Invoice")
st.title("Multilanguage Invoice Demo")

with st.sidebar:
    api_key = st.text_input("Please enter your Gemini Api Key" ,type="password")

input = st.text_input("User Input:" , key="input")
uploaded_file = st.file_uploader("choose the invoice image" , type=["jpg" , "png" , "jpeg","webp"])
submit = st.button("Ask Your Question")
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)



prompt="""
you are an expert in understanding the invoices, and we will upload some invoices and you have
to answer any questions.

"""

submit = st.button("Tell me about the image")
if submit and input:
     image_data = input_image_setup(uploaded_file)
     response = get_response(prompt,image_data,input)
     st.subheader("The Response is...")
     st.write(response)
