import paypalrestsdk
from paypalrestsdk import Payment

from django.conf import settings
from django.http import HttpResponse



def buy(request):
    paypalrestsdk.configure({
        "mode": settings.PAYPAL_MODE,
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET})

    payment = Payment({
        "intent": "sale",

        # ###Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # ###Redirect URLs
        "redirect_urls": {
            "return_url": settings.PAYPAL_RETURN_URL,
            "cancel_url": settings.PAYPAL_CANCEL_URL,
        },

        # ###Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

                             # ### ItemList
                             "item_list": {
                                 "items": [{
                                               "name": "item",
                                               "sku": "item",
                                               "price": "0.10",
                                               "currency": "USD",
                                               "quantity": 1}]},

                             # ###Amount
                             # Let's you specify a payment amount.
                             "amount": {
                                 "total": "0.10",
                                 "currency": "USD"},
                             "description": "This is the payment transaction description."}]})

    # Create Payment and return status
    if payment.create():
    # return HttpResponse("Payment[%s] created successfully" % (payment.id))

     linkler = ""
     for link in payment.links:
           linkler += link.href + "</br>"
           linkler+='Method:'+link.method+"</br>"
           if link.method == "REDIRECT":
            redirect_url = link.href
            #return HttpResponse("Redirect for approval: %s" % (redirect_url))
    else:
        return HttpResponse("Error while creating payment:")
        return HttpResponse(payment.error)

    return HttpResponse(linkler)