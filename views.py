import redis
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SexualFantasiesForm, PhysicalAppearanceForm, SpecificTraitsForm
from .models import UserProfile

# Redis connection setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Helper function to save user preferences to Redis
def save_preferences_to_redis(user_id, preferences):
    redis_key = f"user_preferences:{user_id}"
    # Save user preferences in Redis with a 48-hour expiration (172800 seconds)
    redis_client.setex(redis_key, 172800, json.dumps(preferences))

    # Also store user in a set categorized by preferences for easy querying
    if preferences.get('sex_orientation'):
        redis_client.sadd(f"sexual_fantasies:{preferences['sex_orientation']}", user_id)
    
    if preferences.get('physical_preference'):
        redis_client.sadd(f"physical_preferences:{preferences['physical_preference']}", user_id)

# Check if user is above 18 and subscribed
@login_required
def check_age_and_subscription(user):
    profile = UserProfile.objects.get(user=user)
    return profile.age >= 18 and profile.is_subscribed

# View to handle submission of both sexual fantasies and physical appearance forms
@login_required
def preferences_view(request):
    if not check_age_and_subscription(request.user):
        return redirect('age_restriction_page')

    # Initialize forms
    sexual_fantasies_form = SexualFantasiesForm()
    physical_appearance_form = PhysicalAppearanceForm()

    if request.method == 'POST':
        # Handle submission for sexual fantasies form
        if 'submit_sexual_fantasies' in request.POST:
            sexual_fantasies_form = SexualFantasiesForm(request.POST)
            if sexual_fantasies_form.is_valid():
                preferences = {
                    'sex_orientation': sexual_fantasies_form.cleaned_data['sex_orientation'],
                    'custom_sexual_fantasy': sexual_fantasies_form.cleaned_data['custom_sexual_fantasy'],
                    'fantasy_description': sexual_fantasies_form.cleaned_data['fantasy_description'],
                }
                save_preferences_to_redis(request.user.id, preferences)
                return redirect('success_page')
        
        # Handle submission for physical appearance form
        if 'submit_physical_appearance' in request.POST:
            physical_appearance_form = PhysicalAppearanceForm(request.POST)
            if physical_appearance_form.is_valid():
                preferences = {
                    'physical_preference': physical_appearance_form.cleaned_data['physical_preference'],
                    'custom_physical_preference': physical_appearance_form.cleaned_data['custom_physical_preference'],
                    'appearance_description': physical_appearance_form.cleaned_data['appearance_description'],
                }
                save_preferences_to_redis(request.user.id, preferences)
                return redirect('success_page')

    return render(request, 'preferences.html', {
        'sexual_fantasies_form': sexual_fantasies_form,
        'physical_appearance_form': physical_appearance_form,
    })

# View to query Redis for users with the same sexual fantasies
@login_required
def matching_fantasies_view(request):
    if not check_age_and_subscription(request.user):
        return redirect('age_restriction_page')

    # Get current user's preferences from Redis
    redis_key = f"user_preferences:{request.user.id}"
    user_preferences = redis_client.get(redis_key)

    if user_preferences:
        user_preferences = json.loads(user_preferences)
        sex_orientation = user_preferences.get('sex_orientation')

        if sex_orientation:
            # Query Redis for other users with the same sexual fantasy
            matching_user_ids = redis_client.smembers(f"sexual_fantasies:{sex_orientation}")
            matching_users = []
            
            for user_id in matching_user_ids:
                # Convert user_id from bytes to int, and fetch user info
                user_id = int(user_id)
                if user_id != request.user.id:  # Exclude the current user
                    user_profile = UserProfile.objects.get(user__id=user_id)
                    matching_users.append(user_profile)

            return render(request, 'matching_fantasies.html', {'matching_users': matching_users})
    
    # If no preferences are found, return an empty response
    return render(request, 'matching_fantasies.html', {'matching_users': []})

