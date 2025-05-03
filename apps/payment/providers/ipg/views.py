from urllib.parse import unquote

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

#
# @csrf_exempt
# def redirect_to_gateway(request):
#     context = {
#         'params': {}
#     }
#     for key, value in request.GET.items():
#         if key == 'url' or key == 'method':
#             context[key] = unquote(value)
#         else:
#             context['params'][key] = unquote(value)
#
#     return render(
#         request, 'payment/providers/ipg/redirect_to_gateway.html', context=context
#     )

@csrf_exempt
def return_from_gateway(request):
    pass
