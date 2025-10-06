# LLM module - Phi-3 mini for MSME analytics
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig

class LLMHandler:
    def __init__(self):
        # Initialize Phi-3 mini model (4-bit quantized)
        self.model_name = "microsoft/Phi-3-mini-4k-instruct"
        
        # 4-bit quantization config
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype="float16"
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            trust_remote_code=True,
            device_map="auto",
            attn_implementation="eager"  # For Colab/T4 compatibility
        )
        
        # Create text generation pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.7
        )
        
        self.llm = HuggingFacePipeline(pipeline=self.pipe)

    def generate_response(self, prompt, context=None):
        # Format prompt for Phi-3 instruction following
        if context:
            formatted_prompt = f"<|system|>\nYou are an AI assistant for MSME analytics. Use the provided context to answer questions about the data. If you cannot answer from the context, say so.\n<|user|>\nContext: {context}\n\nQuestion: {prompt}\n<|assistant|>\n"
        else:
            formatted_prompt = f"<|system|>\nYou are an AI assistant for MSME analytics.\n<|user|>\n{prompt}\n<|assistant|>\n"
        
        response = self.llm.invoke(formatted_prompt)
        # Clean response (remove any <|assistant|> tokens if present)
        return response.replace("<|assistant|>\n", "").strip()
