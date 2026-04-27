from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Case, CaseLog
from accounts.decorators import role_required


# Create your views here.


@login_required
@role_required(['customer'])
def create_case(request):
    if request.method == "POST":
        new_case = Case.objects.create(
            customer=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            category=request.POST['category'],
            priority=request.POST['priority'],
            attachment=request.FILES.get('attachment')
        )

        CaseLog.objects.create(
            case=new_case,
            action="Case created",
            performed_by=request.user
        )

        return redirect('my_cases')

    return render(request, 'cases/new_case.html')


@login_required
@role_required(['customer'])
def my_cases(request):
    cases = Case.objects.filter(customer=request.user)
    return render(request, 'cases/my_cases.html', {'cases': cases})


@login_required
def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, 'cases/case_detail.html', {'case': case})


@login_required
@role_required(['agent'])
def claim_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    case.assigned_agent = request.user
    case.status = "In Progress"
    case.save()

    CaseLog.objects.create(
        case=case,
        action="Case claimed by support agent",
        performed_by=request.user
    )

    return redirect('case_detail', pk=pk)


@login_required
@role_required(['agent'])
def escalate_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    case.status = "Escalated"
    case.save()

    CaseLog.objects.create(
        case=case,
        action="Case escalated to specialist",
        performed_by=request.user
    )

    return redirect('case_detail', pk=pk)


@login_required
@role_required(['specialist'])
def resolve_case(request, pk):
    case = get_object_or_404(Case, pk=pk)

    case.specialist = request.user
    case.status = "Resolved"
    case.save()

    CaseLog.objects.create(
        case=case,
        action="Case resolved by specialist",
        performed_by=request.user
    )

    return redirect('case_detail', pk=pk)