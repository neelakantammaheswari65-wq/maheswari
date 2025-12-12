from PIL import Image

def encode_message(image_path, secret_message, output_path):
    """Encodes a secret message into an image using LSB Steganography."""
    try:
        # 1. Open the image
        img = Image.open(image_path).convert('RGB')
        
        # Ensure the message is long enough to include a stop delimiter
        # The delimiter is crucial for the decoder to know when to stop reading
        message = secret_message + '####' 
        
        # Convert message to a binary string
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        
        # Calculate the required number of pixels
        req_pixels = len(binary_message)
        
        # Check if the image has enough capacity
        # Each pixel (R, G, B) can hold 3 bits of data.
        if req_pixels > (img.width * img.height * 3):
            print("Error: Message is too long for the selected image.")
            return

        # 2. Iterate through pixels and replace LSBs
        index = 0
        pixels = img.getdata()
        new_pixels = []

        for item in pixels:
            if index < req_pixels:
                # Process the R, G, B components of the pixel
                
                # Convert the R component to binary and replace its LSB
                r_bin = list(format(item[0], '08b'))
                if index < req_pixels:
                    r_bin[-1] = binary_message[index]
                    index += 1
                new_r = int("".join(r_bin), 2)

                # Convert the G component to binary and replace its LSB
                g_bin = list(format(item[1], '08b'))
                if index < req_pixels:
                    g_bin[-1] = binary_message[index]
                    index += 1
                new_g = int("".join(g_bin), 2)
                
                # Convert the B component to binary and replace its LSB
                b_bin = list(format(item[2], '08b'))
                if index < req_pixels:
                    b_bin[-1] = binary_message[index]
                    index += 1
                new_b = int("".join(b_bin), 2)
                
                new_pixels.append((new_r, new_g, new_b))
            else:
                # Keep the remaining pixels unchanged
                new_pixels.append(item)
                
        # 3. Create and save the new steganographic image
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(new_pixels)
        new_img.save(output_path)
        print(f"✅ Encoding successful! Secret image saved to: {output_path}")

    except Exception as e:
        print(f"An error occurred during encoding: {e}")


def decode_message(image_path):
    """Decodes a secret message from an image encoded using LSB Steganography."""
    try:
        # 1. Open the steganographic image
        img = Image.open(image_path)
        pixels = img.getdata()
        
        binary_data = ""
        
        # 2. Extract the LSB from every color component
        for pixel in pixels:
            # Extract LSB from R, G, B components
            for component in pixel:
                # Get the LSB (the last bit)
                lsb = format(component, '08b')[-1]
                binary_data += lsb
                
        # 3. Convert binary data back to characters
        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        decoded_message = ""
        
        for byte in all_bytes:
            char = chr(int(byte, 2))
            decoded_message += char
            
            # Stop decoding when the delimiter is found
            if decoded_message.endswith('####'):
                # Return the message without the delimiter
                return decoded_message[:-4]

        return "Message could not be fully decoded (delimiter not found)."

    except Exception as e:
        print(f"An error occurred during decoding: {e}")
        return None

# --- USAGE EXAMPLE ---

# 1. Setup the inputs
CARRIER_IMAGE = 'original_image.png' 
# NOTE: Use PNG format as JPEG compression can destroy LSB data!
OUTPUT_IMAGE = 'stego_image.png'
BATTLE_PLAN = "The attack will commence at 0300 hours. Objective Alpha must be secured first. Use code word 'NIGHTHAWK'."


# --- START PROCESS ---

# To run this, you need an image file named 'original_image.png' 
# in the same directory, and the 'Pillow' library installed (pip install Pillow).

print("\n--- Encoding the Secret Message ---")
encode_message(CARRIER_IMAGE, BATTLE_PLAN, OUTPUT_IMAGE)

print("\n--- Decoding the Secret Message ---")
revealed_plan = decode_message(OUTPUT_IMAGE)

if revealed_plan:
    print(f"🔓 Revealed Secret Message: {revealed_plan}")

# --- END PROCESS ---