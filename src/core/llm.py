# LLM module - Phi-4 mini or Grok-4 for MSME analytics (browser-compatible design)
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
from openai import OpenAI
import os
import torch

class LLMHandler:
    def __init__(self, model_choice="phi4"):
        """
        Initialize LLM handler with model choice for easy swapping.
        Models: 'phi4' for Phi-4-mini, 'grok4' for future Grok-4 integration
        """
        self.model_choice = model_choice.lower()
        self.model_name = self._get_model_name()
        self.tokenizer = None
        self.model = None
        self.llm = None

        try:
            self._initialize_model()
        except Exception as e:
            print(f"Warning: Model initialization failed: {e}. Will initialize on first use.")

    def _get_model_name(self):
        """Get model name based on choice"""
        if self.model_choice == "phi4":
            # Use phi-3.5-mini for testing until Phi-4 is released
            return "microsoft/Phi-3.5-mini-instruct"
        elif self.model_choice == "grok4":
            # Use Grok-1 via xAI API (Grok-4 not available yet)
            return "grok-1"
        elif self.model_choice == "api":
            # Use API-only mode for lightweight deployment
            return "api-mode"
        else:
            return "microsoft/Phi-3.5-mini-instruct"  # Default fallback

    def _initialize_model(self):
        """Initialize the language model with optimization for edge devices"""
        if self.model_choice == "grok4":
            # Use xAI API for Grok
            self.client = OpenAI(
                api_key=os.getenv("XAI_API_KEY", ""),  # User should set this
                base_url="https://api.x.ai/v1"
            )
            self.llm = "grok_api"  # Placeholder, will handle in generate_response
            return

        # For browser/WebVM deployment, consider using ONNX.js
        # This server-side implementation is for initial development

        # Check for CUDA availability for quantization
        if torch.cuda.is_available():
            # INT8/4-bit quantization for memory efficiency (~2GB usage)
            bnb_config = BitsAndBytesConfig(
                load_in_8bit=True,  # Using 8-bit for better compatibility, can change to 4-bit
                bnb_8bit_compute_dtype="float16",
                bnb_8bit_use_double_quant=True
            )
            device_map = "auto"
            torch_dtype = "float16"
        else:
            # CPU-only: no quantization, use float32 for compatibility
            bnb_config = None
            device_map = None
            torch_dtype = "float32"

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=bnb_config,
            trust_remote_code=True,
            device_map=device_map,
            attn_implementation="eager",  # For smartphone/CPU compatibility
            torch_dtype=torch_dtype
        )

        # Create optimized pipeline for MSME analytics queries
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=256,  # Reduced for <3s response time
            temperature=0.3,  # Lower temperature for factual business analytics
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        self.llm = HuggingFacePipeline(pipeline=self.pipe)

    def generate_response(self, prompt, context=None, language="en"):
        """Generate response with context from RAG and language support"""
        # Initialize if not done
        if self.llm is None:
            try:
                self._initialize_model()
            except Exception as e:
                return f"Model initialization failed: {e}. Please check requirements."

        # Format prompt with instruction for MSME analytics
        system_prompt = "You are an AI assistant specialized in MSME business analytics. Provide concise, accurate insights from the data. Use bullet points for lists and keep responses under 200 words."

        if language == "hi":
            system_prompt += " Respond in Hindi using simple language."

        if context:
            user_prompt = f"Data Context: {context[:1000]}\n\nQuestion: {prompt}"
        else:
            user_prompt = prompt

        # Phi-4/Grok instruction following format
        if self.model_choice in ["phi4", "grok4"]:
            formatted_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_prompt}\n<|assistant|>\n"
        else:
            # Standard format for other models
            formatted_prompt = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"

        try:
            if self.llm == "grok_api":
                # Use xAI API for Grok
                completion = self.client.chat.completions.create(
                    model="grok-beta",  # Fast model
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=256
                )
                response = completion.choices[0].message.content
            else:
                response = self.llm.invoke(formatted_prompt)

                # Clean response
                response = response.replace(formatted_prompt, "").strip()
                if "<|assistant|>" in response:
                    response = response.split("<|assistant|>")[0].strip()

            # Ensure response is concise for mobile
            return response[:500] if len(response) > 500 else response

        except Exception as e:
            return f"Error generating response: {str(e)}. Please try again."

    def get_model_info(self):
        """Get model information for UI display"""
        device_info = "GPU quantized (<3s response)" if torch.cuda.is_available() else "CPU inference (<30s response)"
        return {
            "model": self.model_name,
            "type": self.model_choice.upper(),
            "optimized_for": device_info,
            "features": ["Business insights", "Multilingual (EN/HI)", "Offline-capable"]
        }
