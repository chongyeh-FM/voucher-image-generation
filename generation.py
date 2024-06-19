import streamlit as st
from openai import OpenAI
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Initialize OpenAI client with the API key
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Function to generate a single image
def generate_image():
    response = client.images.generate(
        model="dall-e-3",
        prompt="Create an enticing full page promotional voucher for a café. The focus of the image should be on the scrumptious food offerings from the café. Display delicate pastries with powdered sugar sprinklings, steaming hot coffee with a perfect crema, and freshly squeezed orange juice with a hint of mint. Ensure the image is tempting and will draw customers into the café. The overall tone should be warm and inviting, showcasing the café as the perfect place for a cosy meal or a quick bite. Do not include text or logos in the design.",
        size="1792x1024",
        quality="hd",
        n=1,
    )
    image_url = response.__dict__.get('data')[0].__dict__.get('url')
    response = requests.get(image_url)
    return Image.open(BytesIO(response.content))

# Function to add text inside a box on an image
def add_text_box(image, text, position, box_size, font_size=30):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Draw rectangle (box)
    box_color = (0, 0, 0, 180)  # semi-transparent black
    draw.rectangle([position, (position[0] + box_size[0], position[1] + box_size[1])], fill=box_color)
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = (position[0] + (box_size[0] - text_width) / 2, position[1] + (box_size[1] - text_height) / 2)
    
    # Draw text
    draw.text(text_position, text, font=font, fill="white")
    return image

# Streamlit app layout
st.title("Promotional Voucher Generator")

# Pre-filled input fields for campaign details
campaign_name = st.text_input("Campaign Name", "Promo 10% off")
duration = st.text_input("Duration", "14 Jun 2024 - 28 Jun 2024")
triggerer = st.text_input("Triggerer", "Making order")
promotion_effect = st.text_input("Promotion Effect", "Bill Discount | 10% off")
conditions = st.text_input("Condition(s)", "No extra conditions")
issue = st.text_input("Issue", "Promotion")

if st.button("Generate Promotional Voucher"):
    with st.spinner('Generating image...'):
        image = generate_image()
        
        # Adding the texts inside boxes to the image
        image = add_text_box(image, f"Campaign Name: {campaign_name}", (396, 10), (1000, 50))  # Center top
        image = add_text_box(image, f"Condition(s): {conditions}", (1292, 864), (500, 50))   # Bottom right adjusted up
        image = add_text_box(image, f"Duration: {duration}", (1292, 914), (500, 50))         # Bottom right adjusted up
        image = add_text_box(image, f"Issue: {issue}", (1292, 10), (500, 50))                # Top right
        image = add_text_box(image, f"Promotion Effect: {promotion_effect}", (646, 837), (600, 50))  # Middle, slightly lower

        image_filename = "promotional_voucher.png"
        image.save(image_filename)
        
        # Display the image and campaign details
        st.image(image, caption="Promotional Voucher", use_column_width=True)
        st.write(f"Image saved as {image_filename}")
        st.write("### Campaign Details")
        st.write(f"**Campaign Name:** {campaign_name}")
        st.write(f"**Duration:** {duration}")
        st.write(f"**Promotion Effect:** {promotion_effect}")
        st.write(f"**Condition(s):** {conditions}")
        st.write(f"**Issue:** {issue}")

# Run the Streamlit app with `streamlit run your_script_name.py`
