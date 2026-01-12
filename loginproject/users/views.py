from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee_login, verification_table
import random, json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

@csrf_exempt
def user_login(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    # Read JSON or form-data
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        data = request.POST

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse(
            {"error": "Email and password required"},
            status=400
        )

    # Find user by email
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401
        )

    # Authenticate using username internally
    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401
        )

    return JsonResponse(
        {"message": "Login successful"},
        status=200
    )





@csrf_exempt
def forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    if not Employee_login.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email not registered"}, status=400)

    otp = random.randint(100000, 999999)
    verification_table.objects.update_or_create(
        email=email,
        defaults={"generated_code": otp}
    )

    print("OTP:", otp)  # debug only

    return JsonResponse({"message": "Verification code sent"})


@csrf_exempt
def reset_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email")
    code = data.get("code")
    new_password = data.get("new_password")

    if not all([email, code, new_password]):
        return JsonResponse({"error": "All fields are required"}, status=400)

    if not verification_table.objects.filter(email=email, generated_code=code).exists():
        return JsonResponse({"error": "Invalid code"}, status=400)

    Employee_login.objects.filter(email=email).update(password=new_password)
    verification_table.objects.filter(email=email).delete()

    return JsonResponse({"message": "Password reset successful"})