import os
import base64
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.conf import settings

# Define storage path dynamically
MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, "encrypted_images")

# Ensure directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

def home(request):
    """Render the home page."""
    return render(request, 'encryptor/index.html')

def upload_image(request):
    """Handles image upload and displays it on the page."""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage(location=MEDIA_ROOT)
        filename = fs.save(image.name, image)
        file_url = f"{settings.MEDIA_URL}encrypted_images/{filename}"
        return render(request, 'encryptor/index.html', {'file_url': file_url})
    return render(request, 'encryptor/index.html')

def encrypt_image(request):
    """Encrypts the uploaded image using Base64."""
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Save original file
        fs = FileSystemStorage(location=MEDIA_ROOT)
        filename = fs.save(image.name, image)
        file_path = os.path.join(MEDIA_ROOT, filename)

        # Read image content and encode it
        with open(file_path, 'rb') as f:
            image_data = f.read()
            encoded_data = base64.b64encode(image_data).decode('utf-8')

        return JsonResponse({"message": "Image encrypted successfully!", "encrypted_data": encoded_data, "original_filename": filename})
    
    return JsonResponse({"error": "Invalid request!"}, status=400)

def decrypt_image(request):
    """Decrypts the encoded image."""
    if request.method == 'POST' and request.POST.get('encrypted_data') and request.POST.get('original_filename'):
        encoded_data = request.POST['encrypted_data']
        original_filename = request.POST['original_filename']

        try:
            decrypted_data = base64.b64decode(encoded_data)
        except base64.binascii.Error:
            return JsonResponse({"error": "Decryption failed! Invalid data."}, status=400)

        # Save decrypted file
        decrypted_filename = f"decrypted_{original_filename}"
        decrypted_path = os.path.join(MEDIA_ROOT, decrypted_filename)
        with open(decrypted_path, 'wb') as df:
            df.write(decrypted_data)

        decrypted_url = f"{settings.MEDIA_URL}encrypted_images/{decrypted_filename}"
        return JsonResponse({"message": "Image decrypted successfully!", "decrypted_url": decrypted_url})
    
    return JsonResponse({"error": "Invalid request!"}, status=400)

def download_image(request, filename):
    """Allows users to download encrypted or decrypted images."""
    file_path = os.path.join(MEDIA_ROOT, filename)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="image/png")  # Change type if needed
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

    return JsonResponse({"error": "File not found!"}, status=404)
