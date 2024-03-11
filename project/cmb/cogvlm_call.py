import io
import requests
import json
import base64
from PIL import Image

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


if __name__ == "__main__":
    get_response(
        image_path="img_v3_028s.jpg",  # TODO fill in the image path
        question="描述这张图.",  # TODO fill in the prompts
    )
