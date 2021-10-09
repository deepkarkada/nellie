"""A module for Natural Language Understanding using knowledge graphs"""

from retico.core import abstract
from retico.core.text.common import SpeechRecognitionIU, TextIU, SegmentedTextIU
from retico.core.dialogue.common import DialogueActIU


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

    def process_iu(self, input_iu):
        current_text = self.get_current_text(input_iu)
        if not current_text:
            return None
        print(f"NLU is processing text: '{current_text}'")

        output_iu = self.create_iu(input_iu)
        output_iu.set_act("TargetDescription", {'ent': 'a boxy head of a dog.', 'rel': 'HasShape_reverse', 'pred_entities': {'Tanzania': 0.06691498229730292, 'Zambia': 0.0001851515592568346, 'Italy': 0.00016547639505501698, 'Ethiopia': 0.00014251661672622513, 'Canada': 0.00013653834412614296, 'Bolivia': 0.0001355487472165435, 'Madagascar': 0.0001299946329469816, 'Uganda': 0.0001272973490682743, 'Mozambique': 0.00012343128061349722, 'Papuanewguinea': 0.00012030888045292746, 'Kenya': 0.0001185569008346497, 'Kazakhstan': 0.00011148258513309954, 'Benin': 0.00010881068524256387, 'Indonesia': 0.00010745342701413822, 'Democratic Republic of the Congo': 0.00010388012631368507, 'Bulgaria': 0.00010091276128591954, 'Ghana': 9.879911417003341e-05, 'Somalia': 8.378844812591889e-05, 'Nigeria': 7.332562983423154e-05, 'Serbia': 7.256045129431391e-05, 'Ireland': 6.764463059422415e-05, 'Rwanda': 6.72815891508098e-05, 'Libya': 6.378716039446841e-05, 'Albania': 5.920747408299777e-05, 'Burundi': 5.8578198016921315e-05, 'Slovakia': 5.828644826082375e-05, 'Nepal': 5.795476722593059e-05, 'South africa': 5.572397859293039e-05, 'Croatia': 5.561246444402941e-05, 'Poland': 5.522584171441654e-05, 'next to ocean': 5.514641051776357e-05, 'Lilongwe': 5.505451740365666e-05, 'Niger': 5.4763223684115004e-05, 'Ivory coast': 5.453218028435508e-05, 'Estonia': 5.419321034698794e-05, 'Angola': 5.299987106042352e-05, 'Namibia': 5.2505752236744696e-05, 'Nairobi': 5.049479408744526e-05, 'Botswana': 4.973060381075387e-05, 'liver': 4.788804350334411e-05, 'Kampala': 4.676862029544126e-05, 'Africa': 4.6566098508104723e-05, 'Finland': 4.600084038794388e-05, 'Germany': 4.454419577188095e-05, 'Greenland': 4.410180469167729e-05, 'Guatemala': 4.331990709671073e-05, 'Chad': 4.317303043840523e-05, 'Fennoscandia': 4.245447858586946e-05, 'Iraq': 4.169064799740955e-05, 'Lesotho': 4.144921070119658e-05, 'Japan': 4.1022893723397203e-05, 'Myanmar': 4.022202562905179e-05, 'hotdog': 3.9842532030466004e-05, 'Malawi': 3.8654864780018726e-05}}, 0.9)
        return output_iu