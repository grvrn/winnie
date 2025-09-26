from django.http import HttpResponse
from sniffer import sniffer

# Create your views here.

def start_sniffer(request):
    sniffer.start_sniffer()
    return HttpResponse("Sniffer started")

def stop_sniffer(request):
    sniffer.stop_sniffer()
    return HttpResponse("Sniffer stopped")