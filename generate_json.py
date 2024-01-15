import os
import random
import json

prompt_txt_path = '/media/jd/cy_personal/aigc_jdt/user_study_data_0522/0522/user_study.txt'

img_path = 'https://raw.githubusercontent.com/daqingliu/Eval_DM/main/dpo_0115'

all_data = []
prompts = []
with open(prompt_txt_path, 'r') as file:
    for line in file:
        line = line.strip()
        prompts.append(line)

q1 = {"issue": "Which image if of higher quality",
      "option": ["I prefer image A", "I am indifferent", "I prefer image B"], "answer": -1}
q2 = {"issue": "Which image matches with the caption better",
      "option": ["I prefer image A", "I am indifferent", "I prefer image B"], "answer": -1}
questions = [q1, q2]

for i in range(len(prompts)):
    data = {}
    data["index"] = i
    data["prompt"] = prompts[i]
    # data["flag"] = False

    random_num = random.randint(0, 1)
    img1_url = os.path.join(img_path, 'our_old', str(i).zfill(5)+'-0.png')
    img2_url = os.path.join(img_path, 'our_new', str(i).zfill(5)+'-0.png')

    if random_num == 1:
        data["reverse"] = True
        data["img1"] = img2_url
        data["img2"] = img1_url
    else:
        data["reverse"] = False
        data["img1"] = img1_url
        data["img2"] = img2_url

    data["question"] = questions

    all_data.append(data)

print(all_data)
with open('user_study_0522.json', 'w') as json_file:
    json.dump(all_data, json_file)
