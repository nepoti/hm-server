from django.http import JsonResponse
from django.http import HttpResponse

def error_response(error, result):
    return JsonResponse({"status": 0, "result": result, "error": error})

def ok_response(result):
    return JsonResponse({"status": 1, "result": result, "error": 0})

def response(result, error=0):
    return JsonResponse({"status": bool(error), "result": result, "error": error})

username_not_valid = error_response(11, {})
username_already_exist = error_response(12, {})
email_not_valid = error_response(31, {})
email_already_exist = error_response(32, {})
auth_error = error_response(41, {})
user_not_active = error_response(42, {})
task_error = error_response(50, {})


status_ok = ok_response({})
