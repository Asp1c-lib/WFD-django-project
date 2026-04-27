from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cases.models import Case


# Create your views here.


@login_required
def dashboard_home(request):
    user = request.user

    if user.is_superuser or user.role == 'admin':
        all_cases = Case.objects.all()
        unresolved_cases = Case.objects.exclude(status='Resolved')

        return render(
            request,
            'dashboard/admin_dashboard.html',
            {
                'all_cases': all_cases,
                'unresolved_cases': unresolved_cases
            }
        )

    elif user.role == 'customer':
        cases = Case.objects.filter(customer=user)
        return render(
            request,
            'dashboard/customer_dashboard.html',
            {'cases': cases}
        )

    elif user.role == 'agent':
        open_cases = Case.objects.filter(status='Open')
        my_cases = Case.objects.filter(assigned_agent=user)

        return render(
            request,
            'dashboard/support_agent_dashboard.html',
            {
                'open_cases': open_cases,
                'my_cases': my_cases
            }
        )

    elif user.role == 'specialist':
        escalated_cases = Case.objects.filter(status='Escalated')
        return render(
            request,
            'dashboard/specialist_dashboard.html',
            {'escalated_cases': escalated_cases}
        )

    # fallback (optional safety)
    return render(request, 'dashboard/customer_dashboard.html')