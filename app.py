from gpt_index import GPTSimpleVectorIndex
import gradio as gr

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    response = index.query(input_text,
                           response_mode='compact')
    return response.response

iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(lines=7,
                                              label='Enter your text'),
                     outputs='text',
                     title='Cutom-trained AI chatbot')

index = GPTSimpleVectorIndex.load_from_disk('index.json')
iface.launch(share=True)