# FitnessPlannerAPI/schema.py

def exclude_djoser_endpoints(endpoints, **kwargs):
    """
    Preprocessing hook for drf-spectacular to exclude certain Djoser endpoints.
    """
    excluded_paths = [
        '/auth/users/{id}/',
        '/auth/users/reset_password/',
        '/auth/users/reset_password_confirm/',
        '/auth/users/reset_username/',        
        '/auth/users/reset_username_confirm/',
        '/auth/users/activation/',
        '/auth/users/resend_activation/'  # Assuming you still want to exclude this one
    ]

    # Filter out the endpoints you want to exclude
    endpoints = [endpoint for endpoint in endpoints if endpoint[0] not in excluded_paths]
    
    return endpoints


