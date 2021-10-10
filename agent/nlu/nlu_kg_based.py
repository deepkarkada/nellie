"""A module for Natural Language Understanding using knowledge graphs"""

from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU, TextIU, SegmentedTextIU
from retico.core.dialogue.common import DialogueActIU

import os
import numpy as np 
import torch 
from torch.nn import functional as F, Parameter
from torch.nn.init import xavier_normal_, xavier_uniform_
import math
import json
import pickle
import operator
import transformers
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

class ConvE(torch.nn.Module):
    def __init__(self, num_entities, num_relations):
        super(ConvE, self).__init__()
        self.emb_dim = 300
        self.use_bias = True
        self.feature_map_dropout = 0.2
        self.input_dropout = 0.2
        self.dropout = 0.3
        # Embedding tables for entity and relations with num_uniq_ent in y-dim, emb_dim in x-dim
        self.emb_e = torch.nn.Embedding(num_entities, self.emb_dim, padding_idx=0)
        self.ent_weights_matrix = torch.ones([num_entities, self.emb_dim], dtype=torch.float64)
        self.emb_rel = torch.nn.Embedding(num_relations, self.emb_dim, padding_idx=0)
        self.ne = num_entities
        self.nr = num_relations
        self.inp_drop = torch.nn.Dropout(self.input_dropout)
        self.hidden_drop = torch.nn.Dropout(self.dropout)
        self.feature_map_drop = torch.nn.Dropout2d(self.feature_map_dropout)
        self.loss = torch.nn.BCELoss()

        self.conv1 = torch.nn.Conv2d(1, 32, (3, 3), 1, 0, bias=self.use_bias)
        self.bn0 = torch.nn.BatchNorm2d(1)
        self.bn1 = torch.nn.BatchNorm2d(32)
        self.bn2 = torch.nn.BatchNorm1d(self.emb_dim)
        self.ln0 = torch.nn.LayerNorm(self.emb_dim)
        self.register_parameter('b', Parameter(torch.zeros(num_entities)))
        self.fc = torch.nn.Linear(16128,self.emb_dim)
    
    def init(self):
        # Xavier initialization
        xavier_normal_(self.emb_e.weight.data)
        xavier_normal_(self.emb_rel.weight.data)

        # Pre-trained embeddings initialization
        #self.init_flairemb()
        #self.emb_e.load_state_dict({'weight': self.ent_weights_matrix})
        
    
    def forward(self, e1, rel, print_pred=False):
        batch_size = 1
        e1_embedded= self.emb_e(e1).view(-1, 1, 10, 30)
        rel_embedded = self.emb_rel(rel).view(-1, 1, 10, 30)
        stacked_inputs = torch.cat([e1_embedded, rel_embedded], 2)

        stacked_inputs = self.bn0(stacked_inputs)
        x= self.inp_drop(stacked_inputs)
        x= self.conv1(x)
        x= self.bn1(x)
        x= F.relu(x)
        x = self.feature_map_drop(x)
        x = x.view(batch_size, -1)
        x = self.fc(x)
        x = self.hidden_drop(x)
        # Try Layer norm instead of batch norm
        #x = self.bn2(x)
        x = self.ln0(x)
        x = F.relu(x)
        x = torch.mm(x, self.emb_e.weight.transpose(1,0)) # shape (batch, n_ent)
        x = self.hidden_drop(x)
        x += self.b.expand_as(x)
        pred = torch.nn.functional.softmax(x, dim=1)
        #print(pred.shape)
        return pred

class WikiData():
    def __init__(self):
        super(WikiData, self).__init__()
        self.ent_path = os.path.join(os.getcwd(), 'nlu/data/wikidata/kg_training_entids_withshapes.txt')
        self.rel_path = os.path.join(os.getcwd(), 'nlu/data/wikidata/kg_training_relids_withshapes.txt')
        self.train_file = os.path.join(os.getcwd(), 'nlu/data/wikidata/e1rel_to_e2_train.json')
        self.test_file = os.path.join(os.getcwd(), 'nlu/data/wikidata/e1rel_to_e2_ranking_test.json')
        self.entity_ids = self.load_data(self.ent_path) 
        self.ids2entities =  self.id2ent(self.ent_path) 
        self.rel_ids =  self.load_data(self.rel_path)
        self.ids2rel =  self.id2rel(self.rel_path) 
        self.train_triples_list = self.convert_triples(self.train_file)
        self.test_triples_list = self.convert_triples(self.test_file)

    def load_data(self, data_path):
        item_dict = {}
        with open(data_path) as df:
            lines = df.readlines()
            for line in lines:
                name, id = line.strip().split('   ')
                item_dict[name] = int(id)
        return item_dict
    
    def id2ent(self, data_path):
        item_dict = {}
        with open(data_path) as df:
            lines = df.readlines()
            for line in lines:
                name, id = line.strip().split('   ')
                item_dict[int(id)] = name
        return item_dict
    
    def id2rel(self, data_path):
        item_dict = {}
        with open(data_path) as df:
            lines = df.readlines()
            for line in lines:
                name, id = line.strip().split('   ')
                item_dict[int(id)] = name
        return item_dict
    
    def convert_triples(self, data_path):
        triples_list = []
        with open(data_path) as df:
            lines = df.readlines()
            for line in lines:
                item_dict = json.loads(line.strip())
                h = item_dict['e1']
                r = item_dict['rel']
                t = item_dict['e2_multi1'].split('\t')
                hrt_list = []
                hrt_list.append(self.entity_ids[h])
                hrt_list.append(self.rel_ids[r])
                t_ents = []
                for t_idx in t:
                    t_ents.append(self.entity_ids[t_idx])
                hrt_list.append(t_ents)
                triples_list.append(hrt_list)
        return triples_list

class KGBasedNLU(abstract.AbstractModule):
    """Currently a dummy NLU Module
    TODO: Incorpoate the knowledge graph
    """

    @staticmethod
    def name():
        return "KG-based NLU Module"

    @staticmethod
    def description():
        return "A Module providing Natural Language Understanding based on knowledge graphs"

    @staticmethod
    def input_ius():
        return [SegmentedTextIU]

    @staticmethod
    def output_iu():
        return DialogueActIU

    def __init__(self, incremental=False, **kwargs):
        super().__init__(**kwargs)
        self.incremental = incremental

    def get_current_text(self, input_iu):
        return input_iu.get_chunks_by_key("Description")[0][1]
    
    def entity_extraction(self, ent_query, entitynames_dict):
        sentence_embedder = SentenceTransformer('all-MiniLM-L6-v2')
        entities_list = list(entitynames_dict.values())
        entities_encoded = sentence_embedder.encode(entities_list, convert_to_tensor=True)
        top_k = 1
        query_embedding = sentence_embedder.encode(ent_query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, entities_encoded)[0]
        top_results = torch.topk(cos_scores, k=top_k)
        # for score, idx in zip(top_results[0], top_results[1]):
        #     print('TOP ENTITIES For ', ent_query, ' -- ' ,entities_list[idx], "(Score: {:.4f})".format(score))
        top_entity = entities_list [top_results[1][0]]
        return top_entity

    def relation_extraction(self, recv_msg):
        model_checkpoint = os.path.join(os.getcwd(), 'nlu/models/checkpoint-500')
        pipe = pipeline("text-classification", tokenizer='distilbert-base-uncased', model=model_checkpoint)

        pred = pipe(recv_msg)
        return pred[0]['label']

    def process_iu(self, input_iu):
        current_text = self.get_current_text(input_iu)
        if not current_text:
            return None
        print(f"NLU is processing text: '{current_text}'")

        data = WikiData()
        num_entities =  len(data.entity_ids)
        num_relations =  len(data.rel_ids)
        top_k = 20

        entitynames_dict = data.ids2entities

        model = ConvE(num_entities, num_relations)
        model.load_state_dict(torch.load('/home/deep/Dialogue/nellie/agent/nlu/models/conve.pt'))
        model.eval()

        rel = self.relation_extraction(current_text)
        new_rel = rel + '_reverse'
        ent = self.entity_extraction(current_text, entitynames_dict)

        h_idx = data.entity_ids[ent]
        r_idx = data.rel_ids[new_rel]

        logits = model.forward(torch.tensor(h_idx), torch.tensor(r_idx), print_pred=False)
        score, pred = torch.topk(logits,top_k,1)
        pred_score = score[0]

        target_dict = {}
        for j, id in enumerate(pred[0].cpu().detach().numpy()): 
            pred_entity = entitynames_dict[id]
            ent_score = pred_score[j].cpu().detach().numpy().tolist()
            target_dict[pred_entity] = ent_score

        max_confidence = max(target_dict.items(), key=operator.itemgetter(1))[0]
        output_iu = self.create_iu(input_iu)
        output_iu.set_act("TargetDescription", {'ent': ent, 'rel': rel, 'pred_entities': target_dict}, max_confidence)
        return output_iu