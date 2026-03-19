from django.forms import ClearableFileInput


class ImageFileInput(ClearableFileInput):
    template_name = 'widgets/image_file_input.html'