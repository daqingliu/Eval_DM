import os
import json
import copy
import torch
from torch.utils.data import DataLoader, Dataset
from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel


class PromptDataset(Dataset):
    def __init__(self, prompts):
        self.prompts = prompts
    def __len__(self):
        return len(self.prompts)
    def __getitem__(self, index):
        return index, self.prompts[index]


if __name__ == "__main__":
    # load data
    prompts = json.load(open('./random.json'))
    dataset = PromptDataset(prompts)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=False)

    # load pipeline
    model_id = "/workspace/models/stable-diffusion-xl-base-1.0"
    base_pipe = StableDiffusionXLPipeline.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16", use_safetensors=True).to("cuda")

    # load finetuned model
    unet_id = "/workspace/models/dpo-sdxl-text2image-v1"
    unet = UNet2DConditionModel.from_pretrained(unet_id, subfolder="unet", torch_dtype=torch.float16)

    dpo_pipe = copy.deepcopy(base_pipe)
    dpo_pipe.unet = unet

    # gpu
    base_pipe = base_pipe.to("cuda")
    dpo_pipe = dpo_pipe.to("cuda")

    # generate
    for batch in dataloader:
        ids, prompts = batch
        generator = torch.manual_seed(0)
        base_images = base_pipe(list(prompts), generator=generator).images
        dpo_images = dpo_pipe(list(prompts), generator=generator).images

        for image, id in zip(base_images, ids):
            image.save(os.path.join('base', f'{id}.jpg'))

        for image, id in zip(dpo_images, ids):
            image.save(os.path.join('dpo', f'{id}.jpg'))