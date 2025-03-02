from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import razorpay, json
from .models import Registration, Workshop, TeamMember, User, Events, Sponsor,workshop_members,event_members
from .forms import workshopRegistrationForm,Basicform,eventRegistrationForm
from django.views.decorators.csrf import csrf_exempt



# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))



def home(request):
    workshops=Workshop.objects.all()
    events=Events.objects.all()
    sponsors=Sponsor.objects.all()
    return render(request,'home.html',{'workshops':workshops,'events':events,'sponsors':sponsors})
def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)

    layout_mapping = {
        2: 'evlayout_view',
        3: 'dronelayout_view',
        4: 'iotlayout_view',
        5: 'matlablayout_view',
    }

    if workshop_id+1 in layout_mapping:
        return redirect(layout_mapping[workshop_id+1])  # Redirect only if the mapping exists

    return render(request, 'workshop_detail.html', {'workshop': workshop})

def dronelayout_view(request):
    drone=Workshop.objects.get(id=2)
    return render(request,'dronelayout.html',{'drone':drone})
def evlayout_view(request):
    ev=Workshop.objects.get(id=1)
    return render(request,'evlayout.html',{'ev':ev})
def iotlayout_view(request):
    iot=Workshop.objects.get(id=3)   
    return render(request,'iotlayout.html',{'iot':iot})
def matlablayout_view(request):
    matlab=Workshop.objects.get(id=4)
    return render(request,'matlablayout.html',{'matlab':matlab})
def cktlayout_view(request):
    ckt=Events.objects.get(id=4)
    return render(request,'cktlayout.html',{'ckt':ckt})
def hackathonlayout_view(request):
    hackathon=Events.objects.get(id=3)
    return render(request,'hackathonlayout.html',{'hackathon':hackathon})
def pplayout_view(request):
    pp=Events.objects.get(id=1)
    return render(request,'pplayout.html',{'pp':pp})
def quizzlayout_view(request):
    quizz=Events.objects.get(id=2)
    return render(request,'quizzlayout.html',{'quizz':quizz})
def photolayout_view(request):
    photo=Events.objects.get(id=6)
    return render(request,'photolayout.html',{'photo':photo})
def projectlayout_view(request):
    project=Events.objects.get(id=5 )
    return render(request,'projectlayout.html',{'project':project})

def event_detail(request, event_id):
    event = get_object_or_404(Events, id=event_id)

    layout_mapping = {
        1: 'pplayout_view',
        2: 'quizzlayout_view',
        3: 'hackathonlayout_view',
        4: 'cktlayout_view',
        5: 'projectlayout_view',
        6: 'photolayout_view',
    }

    if event_id in layout_mapping:
        return redirect(layout_mapping[event_id])  # Redirect only if the mapping exists

    return render(request, 'event_detail.html', {'event': event})

def verify_encurso_id(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            encurso_id = data.get("encurso_id", "").strip()

            if not encurso_id:
                return JsonResponse({"valid": False, "error": "Missing Encurso ID"}, status=400)

            if User.objects.filter(encurso_id=encurso_id).exists():
                return JsonResponse({"valid": True})
            else:
                return JsonResponse({"valid": False, "error": "Invalid ID"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"valid": False, "error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"valid": False, "error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
def basic_fee_payment(request):
    if request.method == 'POST':
        form = Basicform(request.POST)
        email = request.POST.get('email')

        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return render(request, "basic_fee_form.html", {"error": "This email is already registered."})

        if form.is_valid():
            # Update session with the latest form data
            request.session['form_data'] = request.POST.dict()  # Convert QueryDict to regular dict
            request.session['email'] = email  # Store email separately for validation

            return redirect('basic_payment_page')  # Redirect to payment page with updated data
        else:
            print(form.errors)

    else:
        # If session exists, prefill the form with the stored data
        form_data = request.session.get('form_data', {})
        form = Basicform(initial=form_data)  # Prefill form

    return render(request, 'basic_fee_form.html', {'form': form})


def basic_payment_page(request):
    form_data = request.session.get('form_data')
    
    # If user hasn't filled the form yet, redirect them back
    if not form_data:
        return redirect('basic_fee_payment')

    email = request.session.get('email')

    # Create a Razorpay Order
    order_data = {
        "amount": 15000,  # ₹150 (amount in paise)
        "currency": "INR",
        "payment_capture": "1",
    }
    order = client.order.create(order_data)

    # Store Razorpay Order ID in Session
    request.session['razorpay_order_id'] = order['id']

    return render(request, 'basic_fee_payment.html', {
        'form_data': form_data,  # Send updated form data to template
        'email': email,
        'order_id': order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
def verify_payment(request):
    try:
        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')
        signature = request.GET.get('signature')

        # Verify payment
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Retrieve form data from session
        form_data = request.session.get('form_data')
        if not form_data:
            return render(request, 'payment_failed.html', {"error_message": "Session expired. Please try again."})

        # Create & save user in DB now
        form = Basicform(form_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.has_paid_basicfee = True
            user.save()

            # Generate unique encurso_id
            encurso_id = 'ENC' + str(user.id + 1000)
            user.encurso_id = encurso_id
            user.save()

            # Clear session data
            del request.session['form_data']
            del request.session['email']

            return render(request, 'basic_payment_success.html', {"user": user})

    except razorpay.errors.SignatureVerificationError:
        return render(request, 'payment_failed.html', {"error_message": "Payment Verification Failed"})


def register_workshop(request):
    print('yo')
    if request.method == 'POST':
        print(request.POST)  # Debugging: Print received POST data

        encurso_ids = [request.POST.get('encurso_id')]  # Main participant
        team_size = int(request.POST.get('maxteamsize', 1))  # Default to 1 if not given
        workshop_name = request.POST.get('workshopname')
        base_fee = int(request.POST.get('fee', 0))

        if workshop_members.objects.filter(encurso_id=request.POST.get('encurso_id')).exists():
            return render(request, 'register.html', {'error': 'You have already registered for a workshop. Each participant can register for only one workshop.'})

        # Collect all team member Encurso IDs
        for i in range(2, team_size + 1):
            team_member_id = request.POST.get(f"team_member_{i}_id")
            if team_member_id:
                if team_member_id in encurso_ids or workshop_members.objects.filter(encurso_id=team_member_id).exists():
                    return render(request, 'register.html', {'error': f'Duplicate Encurso ID detected: {team_member_id}'})
                encurso_ids.append(team_member_id)

        # Ensure all Encurso IDs exist in the database
        users = User.objects.filter(encurso_id__in=encurso_ids)
        if users.count() != len(encurso_ids):
            return render(request, 'register.html', {'error': 'One or more Encurso IDs are invalid'})

        # Fetch workshop details
        try:
            workshop = Workshop.objects.get(name=workshop_name)
        except Workshop.DoesNotExist:
            return render(request, 'register.html', {'error': 'Invalid workshop selection'})

        # Apply preferences and calculate total fee
        total_fee = 0
        for user in users:
            preference = request.POST.get(f"preference_{encurso_ids.index(user.encurso_id) + 1}", "none").lower()
            extra_fee = 0

            if preference == "accommodation":
                extra_fee = 250
                user.accommodation = True
            elif preference == "food":
                extra_fee = 400
                user.food = True
            elif preference == "both":
                extra_fee = 600
                user.accommodation = True
                user.food = True

            user.workshop_total_fee = request.POST.get('fee')
            user.workshop = workshop.name
            user.save()
            total_fee = int(request.POST.get('fee'))  # Sum up the total fee for the whole team

        # Save Team Members
        team_members_str = ",".join(encurso_ids)
        TeamMember.objects.create(members=team_members_str, workshop=workshop)

        # Create Razorpay Order
        try:
            order_data = {
                "amount": total_fee * 100 ,  # Convert to paise
                "currency": "INR",
                "receipt": f"order_team_{team_members_str}",
                "payment_capture": 1,
            }
            order = client.order.create(data=order_data)
            amountdisp = total_fee

            # Update Razorpay Order ID for all users
            for user in users:
                user.workshop_razorpay_order_id = order['id']
                user.save()
        except Exception as e:
            print("Razorpay payment error:", str(e))
            return render(request, 'register.html', {'error': 'Payment processing error'})

        # Redirect to Payment Page
        return render(request, 'payment_page.html', {
            'users': users,
            'order_id': order['id'],
            'amount': total_fee,
            'key_id': settings.RAZORPAY_KEY_ID,
            'team_members': encurso_ids,
            'team_len': len(encurso_ids),
            'workshop': workshop.name,
            'amountdisp': amountdisp
        })

    else:
        form = workshopRegistrationForm()

    return render(request, 'register.html', {'form': form})





# Payment Verification View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import razorpay

@csrf_exempt
def verify_payment_workshop(request):
    if request.method == 'POST':
        data = request.POST  

        # Debug: Check received data
        print("🔹 Received POST data:", data)

        # Extract required values
        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')

        # Ensure no missing values
        if not order_id or not payment_id or not signature:
            print("❌ Missing required Razorpay payment data")
            return render(request, 'payment_failed.html', {
                'error_message': "Invalid payment data received. Please try again."
            })

        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature  # ✅ Corrected key
            })

            # Fetch all users registered under this order ID
            users = User.objects.filter(workshop_razorpay_order_id=order_id)

            if not users.exists():
                print("❌ No users found with this order ID")
                return render(request, 'payment_failed.html', {
                    'error_message': "No registration found for this payment. Contact support."
                })

            # Update payment status for all team members
            users.update(
                workshop_payment_status='Completed',
                workshop_razorpay_payment_id=payment_id,
                workshop_razorpay_signature=signature
            )
            for user in users:
                workshop_members.objects.create(encurso_id=user.encurso_id, workshop=user.workshop,
                                                name=user.full_name, email=user.email, phone=user.phone,gender=user.gender,institute=user.institute,

                                                )

            workshop_name = users.first().workshop
            encurso_ids = [user.encurso_id for user in users]
            total_amount = users.first().workshop_total_fee   # Sum total fees for all members

            return render(request, 'payment_confirmation.html', {
                'users': users,
                'workshop': workshop_name,
                'amount': total_amount,
                'encurso_ids': encurso_ids,
                'transaction_id': payment_id
            })

        except razorpay.errors.SignatureVerificationError:
            print("❌ Payment signature verification failed")

            # Don't delete users if verification fails—just show an error
            return render(request, 'payment_failed.html', {
                'error_message': "Payment Verification Failed. Please try again."
            })

def index(request):
    return render(request,'home.html')


def register_event(request):
    if request.method == 'POST':
        print(request.POST)  # Debugging: Print received POST data

        encurso_ids = [request.POST.get('encurso_id')]  # Main participant
        team_size = int(request.POST.get('maxteamsize', 1))  # Default to 1 if not given
        event_name = request.POST.get('eventname')
        total_fee = int(request.POST.get('fee', 0))
        
        if event_members.objects.filter(encurso_id=request.POST.get('encurso_id')).exists():
            return render(request, 'event_register.html', {'error': 'You have already registered for a event. Each participant can register for only one workshop.'})
        # Collect all team member Encurso IDs
        for i in range(2, team_size + 1):
            team_member_id = request.POST.get(f"team_member_{i}_id")
            if team_member_id:
                if team_member_id in encurso_ids or event_members.objects.filter(encurso_id=team_member_id).exists():
                    return render(request, 'event_register.html', {'error': f'Duplicate Encurso ID detected: {team_member_id}'})
                encurso_ids.append(team_member_id)

        # Ensure all Encurso IDs exist in the database
        users = User.objects.filter(encurso_id__in=encurso_ids)
        if users.count() != len(encurso_ids):
            return render(request, 'event_register.html', {'error': 'One or more Encurso IDs are invalid'})

        # Fetch workshop details

        # Apply preferences and calculate total fee
        total_fee = 0
        for user in users:
            preference = request.POST.get(f"preference_{encurso_ids.index(user.encurso_id) + 1}", "none").lower()
            extra_fee = 0

            if preference == "accommodation":
                extra_fee = 250
                user.accommodation = True
            elif preference == "food":
                extra_fee = 400
                user.food = True
            elif preference == "both":
                extra_fee = 600
                user.accommodation = True
                user.food = True

            user.event_total_fee = request.POST.get('fee')
            user.event = event_name
            user.save()
            total_fee = int(request.POST.get('fee'))  # Sum up the total fee for the whole team

        # Save Team Members
        team_members_str = ",".join(encurso_ids)
        TeamMember.objects.create(members=team_members_str, event=event_name)

        # Create Razorpay Order
        try:
            order_data = {
                "amount": total_fee * 100 ,  # Convert to paise
                "currency": "INR",
                "receipt": f"order_team_{team_members_str}",
                "payment_capture": 1,
            }
            order = client.order.create(data=order_data)
            amountdisp = total_fee

            # Update Razorpay Order ID for all users
            for user in users:
                user.event_razorpay_order_id = order['id']
                user.save()
        except Exception as e:
            print("Razorpay payment error:", str(e))
            return render(request, 'event_register.html', {'error': 'Payment processing error'})

        # Redirect to Payment Page
        return render(request, 'event_page_confirmation.html', {
            'users': users,
            'order_id': order['id'],
            'amount': total_fee,
            'key_id': settings.RAZORPAY_KEY_ID,
            'team_members': encurso_ids,
            'team_len': len(encurso_ids),
            'event': event_name,
            'amountdisp': amountdisp
        })
    else:
        form = eventRegistrationForm()

    return render(request, 'event_register.html', {'form': form})

def create_encurso_id(request):
    return redirect('basic_fee_payment')
@csrf_exempt
def verify_payment_event(request):
    if request.method == 'POST':
        data = request.POST  

        # Debug: Check received data
        print("🔹 Received POST data:", data)

        order_id = data.get('razorpay_order_id')
        payment_id = data.get('razorpay_payment_id')
        signature = data.get('razorpay_signature')

        if not order_id or not payment_id or not signature:
            print("❌ Missing required Razorpay payment data")
            return render(request, 'event_payment_failure.html', {
                'error_message': "Invalid payment data received. Please try again."
            })

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Find all users registered under this order ID
            users = User.objects.filter(event_razorpay_order_id=order_id)
            if not users.exists():
                return render(request, 'event_payment_failure.html', {
                    'error_message': "No users found for this order. Please contact support."
                })

            # Update payment status for all users
            for user in users:
                event_members.objects.create(
                    name = user.full_name,
                    email = user.email,
                    phone = user.phone,
                    gender = user.gender,
                    institute = user.institute,
                    home_town = user.home_town,
                    encurso_id = user.encurso_id,
                    event = user.event)
                
                user.event_payment_status = 'Completed'
                user.event_razorpay_payment_id = payment_id
                user.event_razorpay_signature = signature
                user.save()

            # Extract details for display
            event_name = users.first().event  # Assuming all are registered for the same event
            encurso_ids = [user.encurso_id for user in users]
            total_amount = users.first().event_total_fee  # Assuming the same total fee for all

            return render(request, 'event_payment_success.html', {
                'users': users,
                'event': event_name,
                'amount': total_amount,
                'encurso_ids': encurso_ids,
                'transaction_id': payment_id
            })

        except razorpay.errors.SignatureVerificationError:
            User.objects.filter(event_razorpay_order_id=order_id).delete()
            return render(request, 'event_payment_failure.html', {
                'error_message': "Payment Verification Failed. Please try again."
            })


def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')
def refund(request):
    return render(request, 'refund.html')

def contactus(request):
    return render(request, 'contact.html')

@csrf_exempt  # Disable CSRF for simplicity (better to use proper authentication)
def recover_encurso_id(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            phone = data.get("phone")

            # Check if a user exists with the given email and phone
            user = User.objects.filter(email=email, phone=phone).first()

            if user:
                return JsonResponse({"success": True, "encurso_id": user.encurso_id})
            else:
                return JsonResponse({"success": False, "message": "Invalid details"})
        
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)