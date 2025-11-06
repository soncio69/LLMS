# Questa classe utilizza la libreria Gradio per creare un'interfaccia web
# che consenta di effettuare l'upload di un'immagine ed invocare un modello
# per image segmentation (ad esempio estraendo una persona dall'immagine).


from transformers import pipeline
from PIL import ImageOps, Image
import gradio as gr

# Creates a segmentation model 
model = pipeline("image-segmentation", 
                 model="nvidia/segformer-b0-finetuned-ade-512-512")  

def segmentation(image, label):
    # Converts image from NumPy array to PIL format 
    image = Image.fromarray(image)  
    results = model(image)  # Uses the model for inferencing 
    for result in results:
        if result['label'] == label:
            base_image = image.copy()
            mask_image = result['mask']
            mask_image = ImageOps.invert(mask_image)  # Inverts the mask
            
            # Applies the mask over the original image
            base_image.paste(mask_image, mask=mask_image)  
            return(base_image)

# Per visualizzare gli oggetti che il modello è in grado di identificare
#segmentation.model.config.id2label)

image_input = gr.Image(label = "Image to segmentize")

label = gr.Textbox(label = "Label to look for", placeholder = "Label")
image_output = gr.Image(label = "Image with the mask applied")

gr.Interface(segmentation,
             [image_input, label],
             image_output).launch()