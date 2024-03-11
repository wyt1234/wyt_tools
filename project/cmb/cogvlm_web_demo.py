"""
This script is a simple web demo of the CogVLM and CogAgent models, designed for easy and quick demonstrations.
For a more sophisticated user interface, users are encouraged to refer to the 'composite_demo',
which is built with a more aesthetically pleasing Streamlit framework.

Usage:
- Use the interface to upload images and enter text prompts to interact with the models.

Requirements:
- Gradio (only 3.x,4.x is not support) and other necessary Python dependencies must be installed.
- Proper model checkpoints should be accessible as specified in the script.

Note: This demo is ideal for a quick showcase of the CogVLM and CogAgent models. For a more comprehensive and interactive
experience, refer to the 'composite_demo'.
"""
import base64
import json

import gradio as gr
import os, sys

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
import torch
import time

DESCRIPTION = '''<h1 style='text-align: center'> <a href="https://github.com/THUDM/CogVLM">CogVLM / CogAgent</a> </h1>'''

NOTES = '<h3> This app is adapted from <a href="https://github.com/THUDM/CogVLM">https://github.com/THUDM/CogVLM</a>. It would be recommended to check out the repo if you want to see the detail of our model, CogVLM & CogAgent. </h3>'

MAINTENANCE_NOTICE1 = 'Hint 1: If the app report "Something went wrong, connection error out", please turn off your proxy and retry.<br>Hint 2: If you upload a large size of image like 10MB, it may take some time to upload and process. Please be patient and wait.'

AGENT_NOTICE = 'Hint 1: To use <strong>Agent</strong> function, please use the <a href="https://github.com/THUDM/CogVLM/blob/main/utils/utils/template.py#L761">prompts for agents</a>.'

GROUNDING_NOTICE = 'Hint 2: To use <strong>Grounding</strong> function, please use the <a href="https://github.com/THUDM/CogVLM/blob/main/utils/utils/template.py#L344">prompts for grounding</a>.'

default_chatbox = [("", "Hi, What do you want to know about this image?")]

model = image_processor = text_processor_infer = None

is_grounding = False


def process_image_without_resize(image_prompt):
    image = Image.open(image_prompt)
    # print(f"height:{image.height}, width:{image.width}")
    timestamp = int(time.time())
    file_ext = os.path.splitext(image_prompt)[1]
    filename_grounding = f"examples/{timestamp}_grounding{file_ext}"
    return image, filename_grounding


requests.packages.urllib3.disable_warnings()
BAD_RESPONSE = "<error></error>"


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')


def get_response(image_path, question):
    base64_img = image_to_base64(image_path)

    url = 'http://180.184.41.237:28080/'
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "inputs": f"##第 1 轮##\\n\\n问：<img_start>data:image/jpeg;base64,{base64_img}<img_end>这张图是什么\\n\\n答：",
        "parameters": {
            "max_new_tokens": 1024,
            "do_sample": False
        },
        "stream": False
    }
    try_times = 0
    while try_times < 3:
        try_times += 1
        try:
            #            response = requests.post(url, headers=headers, stream=True, data=json.dumps(payload), verify=False)
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            print(response.text)
            output = ""
            if response.status_code == 200:

                for line in response.iter_lines():
                    if line:
                        try:
                            decoded_line = line.decode('utf-8').lstrip("data: ")
                            # print(decoded_line)
                            data = json.loads(decoded_line)
                            output += data["choices"][0]["text"]
                        except Exception as e:
                            pass
                print(output)
                return output.strip()
            else:
                print(f"Received bad status code: {response.status_code}")
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something Else:", err)

    return BAD_RESPONSE


# 修改后的 post 函数
def post(input_text, temperature, top_p, top_k, image_prompt, result_previous, hidden_image, state):
    result_text = [(ele[0], ele[1]) for ele in result_previous]
    for i in range(len(result_text) - 1, -1, -1):
        if result_text[i][0] == "" or result_text[i][0] == None:
            del result_text[i]
    print(f"history {result_text}")

    try:
        response_text = get_response(image_path=image_prompt, question=input_text)  # 使用API进行推理
        if response_text == BAD_RESPONSE:
            raise Exception("Bad response from API")
    except Exception as e:
        print("error message", e)
        result_text.append((input_text, 'Error! Please check the console for more details.'))
        return "", result_text, hidden_image

    result_text.append((input_text, response_text))
    print(result_text)
    print('finished')
    return "", result_text, hidden_image


def clear_fn(value):
    return "", default_chatbox, None


def clear_fn2(value):
    return default_chatbox


def main(args):
    gr.close_all()

    with gr.Blocks(css='style.css') as demo:
        state = gr.State({'args': args})

        gr.Markdown(DESCRIPTION)
        gr.Markdown(NOTES)

        with gr.Row():
            with gr.Column(scale=5):
                with gr.Group():
                    gr.Markdown(AGENT_NOTICE)
                    gr.Markdown(GROUNDING_NOTICE)
                    input_text = gr.Textbox(label='Input Text',
                                            placeholder='Please enter text prompt below and press ENTER.')

                    with gr.Row():
                        run_button = gr.Button('Generate')
                        clear_button = gr.Button('Clear')

                    image_prompt = gr.Image(type="filepath", label="Image Prompt", value=None)

                with gr.Row():
                    temperature = gr.Slider(maximum=1, value=0.8, minimum=0, label='Temperature')
                    top_p = gr.Slider(maximum=1, value=0.4, minimum=0, label='Top P')
                    top_k = gr.Slider(maximum=100, value=10, minimum=1, step=1, label='Top K')

            with gr.Column(scale=5):
                result_text = gr.components.Chatbot(label='Multi-round conversation History',
                                                    value=[("", "Hi, What do you want to know about this image?")],
                                                    height=600)
                hidden_image_hash = gr.Textbox(visible=False)

        gr.Markdown(MAINTENANCE_NOTICE1)

        print(gr.__version__)
        run_button.click(fn=post,
                         inputs=[input_text, temperature, top_p, top_k, image_prompt, result_text, hidden_image_hash,
                                 state],
                         outputs=[input_text, result_text, hidden_image_hash])
        input_text.submit(fn=post,
                          inputs=[input_text, temperature, top_p, top_k, image_prompt, result_text, hidden_image_hash,
                                  state],
                          outputs=[input_text, result_text, hidden_image_hash])
        clear_button.click(fn=clear_fn, inputs=clear_button, outputs=[input_text, result_text, image_prompt])
        image_prompt.upload(fn=clear_fn2, inputs=clear_button, outputs=[result_text])
        image_prompt.clear(fn=clear_fn2, inputs=clear_button, outputs=[result_text])

    # demo.queue(concurrency_count=10)
    demo.launch(debug=True, show_error=True, server_port=7861)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--max_length", type=int, default=2048, help='max length of the total sequence')
    parser.add_argument("--top_p", type=float, default=0.4, help='top p for nucleus sampling')
    parser.add_argument("--top_k", type=int, default=1, help='top k for top k sampling')
    parser.add_argument("--temperature", type=float, default=.8, help='temperature for sampling')
    parser.add_argument("--version", type=str, default="chat", choices=['chat', 'vqa', 'chat_old', 'base'],
                        help='version of language process. if there is \"text_processor_version\" in model_config.json, this option will be overwritten')
    parser.add_argument("--quant", choices=[8, 4], type=int, default=None, help='quantization bits')
    parser.add_argument("--from_pretrained", type=str, default="cogagent-chat", help='pretrained ckpt')
    parser.add_argument("--local_tokenizer", type=str, default="lmsys/vicuna-7b-v1.5", help='tokenizer path')
    parser.add_argument("--fp16", action="store_true")
    parser.add_argument("--bf16", action="store_true")
    parser.add_argument("--stream_chat", action="store_true")
    args = parser.parse_args()
    rank = int(os.environ.get('RANK', 0))
    world_size = int(os.environ.get('WORLD_SIZE', 1))
    args = parser.parse_args()
    main(args)
