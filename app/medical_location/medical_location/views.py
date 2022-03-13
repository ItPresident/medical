from django.shortcuts import render


def main_page(request):
    return render(request, 'medical_main/main.html')
