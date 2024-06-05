from tasks import send_request

for i in range(100):
    print('Задача ', i, ' выполнена')
    send_request.apply_async(queue='message', kwargs={'data': 123})