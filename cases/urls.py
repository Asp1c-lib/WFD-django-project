from django.urls import path
from .views import (
    create_case,
    my_cases,
    case_detail,
    claim_case,
    escalate_case,
    resolve_case,
)

urlpatterns = [
    path('create/', create_case, name='create_case'),
    path('my/', my_cases, name='my_cases'),
    path('<int:pk>/', case_detail, name='case_detail'),

    # suooprt agent actions
    path('<int:pk>/claim/', claim_case, name='claim_case'),
    path('<int:pk>/escalate/', escalate_case, name='escalate_case'),

    # specialists action
    path('<int:pk>/resolve/', resolve_case, name='resolve_case'),
]