from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'invoices': [
            {'id': 1, 'client': 'Client A', 'date': '2025-01-01', 'amount': 100.00},
            {'id': 2, 'client': 'Client B', 'date': '2025-01-02', 'amount': 200.00},
        ]
    }
    return render(request, 'index.html', context)
