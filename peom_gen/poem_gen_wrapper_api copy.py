
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

txt = "عمرو بنِ قُمَيئَة: خَليلَيَّ لا تَستَعجِلا أَن"  # sample input to model


class ModelWrapper:
    '''
    Run model predictions locally. 

    load_model: load model checkpoint 
    predict: generates based on input text and poet name  
    '''
    model_path = "./checkpoint-9100"
    context_length = 184

    @staticmethod
    def predict(to_predict, model):
        '''
        Take input + poet
        laod model checkpoint
        generate poem
        '''
        model = AutoModelForCausalLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # make pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
        )

        #add poet name to input
        to_predict = poet + ": " + to_predict

        # generate poem
        generated = pipe(
            to_predict,
            num_return_sequences=1,
            max_length=context_length,
        )

        # return generated poem
        return generated[0]['generated_text'].split(":")[1]

    