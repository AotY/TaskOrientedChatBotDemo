import os

import torch

from util.config_util import read_config
from util.convert_util import ConvertUtil

USE_CUDA = torch.cuda.is_available()

config = read_config("./config/guotie.yaml")
save_dir = config["save_dir"]
batch_size = 1
convert_util = ConvertUtil(config)

def load_model():
    # load model
    if USE_CUDA:
        decoder = torch.load(os.path.join(save_dir, 'decoder-100.pt'))
        encoder = torch.load(os.path.join(save_dir, 'encoder-100.pt'))
    else:
        decoder = torch.load(os.path.join(save_dir, 'decoder-100.pt'), map_location=torch.device('cpu'))
        encoder = torch.load(os.path.join(save_dir, 'encoder-100.pt'), map_location=torch.device('cpu'))
    return encoder, decoder

# load model
encoder, decoder = load_model()

def predict(text):
    test_input_list, vacab_list = convert_util.gen_test_data(text)
    input_vocab, slot_vocab, intent_vocab = vacab_list

    with torch.no_grad():
        input_batch = torch.LongTensor(test_input_list)
        if USE_CUDA:
            input_batch = input_batch.cuda()

        input_mask = torch.cat([torch.BoolTensor(tuple(map(lambda s: s == 0, t.data))).cuda()
                                if USE_CUDA else torch.BoolTensor(tuple(map(lambda s: s == 0, t.data)))
                                for t in input_batch]).view(batch_size, -1)

        print('input_mask: ', input_mask.size()) # [1, 20]

        output, hidden_c = encoder(input_batch, input_mask)
        print('encoder output: ', output.size()) # [1, 20, 128]
        print('encoder hidden_c: ', hidden_c.size()) # [1, 20, 128]

        start_decode = torch.LongTensor([[input_vocab.index("PAD")] * batch_size]).transpose(1, 0)

        if USE_CUDA:
            start_decode = start_decode.cuda()

        slot_score, intent_score = decoder(start_decode, hidden_c, output, input_mask)
        print('slot_score: ', slot_score.size()) # [20, 3]
        print('intent_score: ', intent_score.size()) # [1, 9]

        # calculate intent detection accuracy
        _, max_index = intent_score.max(1)
        intent_test = intent_vocab[max_index[0]]
        print(f'intent: {intent_test}')  #

        # batch, sequence_max_length, tag_length
        slot_score = slot_score.view(batch_size, -1, list(slot_score[1].size())[0])

        # calculate tag detection accuracy
        _, max_tag_index = slot_score.max(2)
        slot_test = []
        for tag in max_tag_index[0]:
            slot_test.append(slot_vocab[tag])
        print('slot_test: ', slot_test)

        return intent_test

if __name__ == '__main__':
    predict("你叫什么名字？")

